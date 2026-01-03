from Arrow import Arrow

class Container:

    def __init__(self, factory):
        self._shapes = []
        self.factory = factory
        self._arrows = []
        self._observes = []

    def subscribe(self, observer):
        self._observes.append(observer)

    def uved_observers(self, event):

        for observer in self._observes:
            observer.update(event)

    def add_arrow(self, arrow):
        self._arrows.append(arrow)
        self.uved_observers("structure")

    def get_arrows(self):
        return self._arrows

    def get_arrow_at_point(self, pos):
        for arrow in reversed(self._arrows):
            if arrow.contains_point(pos):
                return arrow
        return None

    def add(self, shape):
        self._shapes.append(shape)
        self.uved_observers("structure")

    def get_shapes(self):
        return self._shapes

    def clear_selection(self):
        for shape in self._shapes:
            shape.set_selected(False)
        for arrow in self._arrows:
            arrow.set_selected(False)
        self.uved_observers("selection")

    def select_shape(self, shape, value = True):
        shape.set_selected(value)
        self.uved_observers("selection")

    def select_arrow(self, arrow, value = True):
        arrow.set_selected(value)
        arrow.source.set_selected(value)
        arrow.target.set_selected(value)

        self.uved_observers("selection")

    def get_selected(self):
        return [s for s in self._shapes if s.is_selected()]

    def remove_selected(self):

        removed_shapes = {s for s in self._shapes if s.is_selected()}

        for arrow in self._arrows:
            if arrow.source in removed_shapes or arrow.target in removed_shapes:
                self._arrows.remove(arrow)

        for shape in removed_shapes:
            self._shapes.remove(shape)

        self.uved_observers("structure")

    def get_shape_at_point(self, pos):
        for shape in reversed(self._shapes):
            if shape.contains_point(pos):
                return shape
        return None

    def save(self, filename):
        with open(filename, "w") as f:
            f.write(f"{len(self._shapes)}\n")
            for shape in self._shapes:
                shape.save(f)

            f.write(f"{len(self._arrows)}\n")
            for arrow in self._arrows:
                src_index = self._shapes.index(arrow.source)
                tgt_index = self._shapes.index(arrow.target)
                f.write(f"{src_index} {tgt_index}\n")

    def load(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            count = int(f.readline())
            self._shapes.clear()
            self._arrows.clear()

            for _ in range(count):
                shape = self.load_shape(f)
                self._shapes.append(shape)

            arrows_count = int(f.readline())
            for _ in range(arrows_count):
                src_idx, tgt_idx = map(int, f.readline().split())
                source = self._shapes[src_idx]
                target = self._shapes[tgt_idx]
                self._arrows.append(Arrow(source, target))

        self.uved_observers("structure")

    def load_shape(self, stream):
        type_shape = stream.readline().strip()
        shape = self.factory.create_shape(type_shape)
        shape.load(stream, self.factory)
        return shape

    def delete_shapes(self):
        self._shapes.clear()
        self._arrows.clear()
        self.uved_observers("structure")

    def move_shapes(self, dx, dy, canvas_rect):
        moved = set()

        def move_shape(shape):
            if shape in moved:
                return

            old_x, old_y = shape.get_position()
            shape.move(dx, dy, canvas_rect)

            if not shape.check_bounds(canvas_rect):
                shape.set_position(old_x, old_y)
                return

            moved.add(shape)

            for arrow in self._arrows:
                if arrow.source is shape:
                    move_shape(arrow.target)

        for shape in self._shapes:
            if shape.is_selected():
                move_shape(shape)

        self.uved_observers("selection")

    def resize_shapes(self, delta, canvas_rect):

        for shape in self._shapes:
            if shape.is_selected():
                shape.resize(delta)
                if not shape.check_bounds(canvas_rect):
                    shape.resize(-delta)

        self.uved_observers("selection")

    def set_selection(self, shapes):
        for s in self._shapes:
            s.set_selected(False)

        for s in shapes:
            s.set_selected(True)

        self.uved_observers("selection")