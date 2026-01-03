from PyQt5.QtCore import QRect, QPoint
from PyQt5.QtGui import QPen, QBrush, QPolygon, QColor
from PyQt5.QtCore import Qt
from Shape import Shape

class Triangle(Shape):
    def __init__(self, x = 0, y = 0, size = 80, color = None):
        super().__init__(x, y, color)
        self._size = size
        self._height = int(self._size * 0.866)

    def get_vertices(self):
        return [
            QPoint(self._x, self._y - self._height // 2),
            QPoint(self._x - self._size // 2, self._y + self._height // 2),
            QPoint(self._x + self._size // 2, self._y + self._height // 2)
        ]

    def draw(self, painter):
        if self._selected:
            painter.setPen(QPen(Qt.red, 2))
            painter.setBrush(QBrush(self._color))
        else:
            painter.setPen(QPen(Qt.black, 2))
            painter.setBrush(QBrush(self._color))

        vertices = self.get_vertices()
        painter.drawPolygon(*vertices)

    def contains_point(self, pos):
        triangle = QPolygon(self.get_vertices())

        return triangle.containsPoint(pos, Qt.OddEvenFill)

    def get_bounds(self):
        return QRect(self._x - self._size // 2,
                     self._y - self._height // 2,
                     self._size, self._height)

    def resize(self, delta):
        new_size = self._size + delta
        if new_size >= 20:
            self._size = new_size
            self._height = int(self._size * 0.866)
        return new_size >= 20

    def save(self, stream):
        r, g, b = self._color.red(), self._color.green(), self._color.blue()
        stream.write("Triangle\n")
        stream.write(f"{self._x} {self._y} {self._size} {r} {g} {b}\n")

    def load(self, stream, factory = None):
        self._x, self._y, self._size, r, g, b = map(int, stream.readline().split())
        self._color = QColor(r, g, b)