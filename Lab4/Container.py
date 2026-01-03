class Container:

    def __init__(self):
        self._shapes = []

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