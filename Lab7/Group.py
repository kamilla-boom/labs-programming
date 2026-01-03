from PyQt5.QtGui import QPen, QColor
from PyQt5.QtCore import Qt
from Shape import Shape

class Group(Shape):

    def __init__(self, x = 0, y = 0, shapes = None):
        super().__init__(x ,y)
        self._shapes = shapes or []

    def get_child(self):
        return self._shapes

    def draw(self, painter):

        for shape in self._shapes:
            shape.draw(painter)

        if self.is_selected():

            bounds = self.get_bounds()
            pen = QPen(QColor("black"))
            pen.setStyle(Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(bounds)

    def get_bounds(self):

        rect = self._shapes[0].get_bounds()
        for shape in self._shapes[1:]:
            rect = rect.united(shape.get_bounds())

        return rect

    def move(self, dx, dy, canvas_rect = None, notify=False):
        if canvas_rect is not None:
            bounds = self.get_bounds()
            moved = bounds.translated(dx, dy)

            if not canvas_rect.contains(moved):
                return

        for shape in self._shapes:
            shape.move(dx, dy)

    def contains_point(self, pos):
        for shape in self._shapes:
            if shape.contains_point(pos):
                return True
        return False

    def save(self, stream):
        stream.write("Group\n")
        stream.write(f"{len(self._shapes)}\n")
        for shape in self._shapes:
            shape.save(stream)

    def load(self, stream, factory):

        self._shapes = []

        count = int(stream.readline())

        for _ in range(count):
            type_shape = stream.readline().strip()
            shape = factory.create_shape(type_shape)
            shape.load(stream, factory)
            self._shapes.append(shape)

    def set_color(self, color):
        for shape in self._shapes:
            shape.set_color(color)

    def resize(self, delta):
        for shape in self._shapes:
            shape.resize(delta)

    def type_shape(self):
        return "Group"

    def get_position(self):

        xs = []
        ys = []

        for shape in self._shapes:
            cx, cy = shape.get_position()
            xs.append(cx)
            ys.append(cy)

        return sum(xs) // len(xs), sum(ys) // len(ys)