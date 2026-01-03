from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt
from Shape import Shape

class Circle(Shape):

    def __init__(self, x, y, radius = 40, color = None):
        super().__init__(x, y, color)
        self._radius = radius

    def contains_point(self, pos):
        dx = pos.x() - self._x
        dy = pos.y() - self._y
        return dx * dx + dy * dy <= self._radius * self._radius   # √(dx² + dy²)

    def draw(self, painter):
        if self._selected:
            painter.setPen(QPen(Qt.red, 2))
            painter.setBrush(QBrush(self._color))
        else:
            painter.setPen(QPen(Qt.black, 2))
            painter.setBrush(QBrush(self._color))

        painter.drawEllipse(self._x - self._radius,
                            self._y - self._radius,
                            self._radius * 2,
                            self._radius * 2)

    def get_bounds(self):
        return QRect(self._x - self._radius,
                    self._y - self._radius,
                    self._radius * 2,
                    self._radius * 2)

    def resize(self, delta):
        new_radius = self._radius + delta
        if new_radius >= 10:
            self._radius = new_radius
        return new_radius >= 10
