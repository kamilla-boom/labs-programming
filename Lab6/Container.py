class Container:

    def __init__(self, factory):
        self._shapes = []
        self.factory = factory

    def add(self, shape):
        self._shapes.append(shape)

    def get_shapes(self):
        return self._shapes

    def clear_selection(self):
        for shape in self._shapes:
            shape.set_selected(False)

    def remove_selected(self):
        self._shapes = [shape for shape in self._shapes if not shape.is_selected()]

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

    def load(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            count = int(f.readline())
            self._shapes.clear()

            for _ in range(count):
                shape = self.load_shape(f)
                self._shapes.append(shape)

    def load_shape(self, stream):
        type_shape = stream.readline().strip()
        shape = self.factory.create_shape(type_shape)
        shape.load(stream, self.factory)
        return shape
