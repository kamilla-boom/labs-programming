from PyQt5.QtGui import QPen, QColor
from PyQt5.QtCore import QPointF
import math

class Arrow:

    def __init__(self, source, target):
        self.source = source
        self.target = target
        self._selected = False

    def draw(self, painter):

        x1, y1 = self.source.get_position()
        x2, y2 = self.target.get_position()

        pen = QPen(QColor("red") if self._selected else QColor("black"))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(x1, y1, x2, y2)

    def set_selected(self, value):
        self._selected = value

    def is_selected(self):
        return self._selected

    def get_points(self):

        x1, y1 = self.source.get_position()
        x2, y2 = self.target.get_position()

        return QPointF(x1, y1), QPointF(x2, y2)

    def contains_point(self, pos):

        if self.source is None or self.target is None:
            return False

        x1, y1 = self.source.get_position()
        x2, y2 = self.target.get_position()

        px, py = pos.x(), pos.y()

        # отклонение
        dx = x2 - x1
        dy = y2 - y1

        length_sq = dx*dx + dy*dy

        if length_sq == 0:
            return False

        t = ((px - x1)*dx + (py - y1)*dy) / length_sq #
        t = max(0, min(1, t))

        proj_x = x1 + t*dx  # x перпендикуляра стрелке
        proj_y = y1 + t*dy  # y

        dist = math.hypot(px - proj_x, py - proj_y)  # гипотенуза

        return dist <= 5


