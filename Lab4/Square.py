from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt
from Shape import Shape

class Square(Shape):

    def __init__(self, x, y, size = 80, color = None):
        super().__init__(x, y, color)
        self._size = size

    def draw(self, painter):
        if self._selected:
            painter.setPen(QPen(Qt.red, 2))
            painter.setBrush(QBrush(self._color))
        else:
            painter.setPen(QPen(Qt.black, 2))
            painter.setBrush(QBrush(self._color))
        half = self._size // 2
        painter.drawRect(self._x - half, self._y - half,
                         self._size, self._size)

    def contains_point(self, pos):
        half = self._size // 2
        left = self._x - half
        right = self._x + half
        top = self._y - half
        bottom = self._y + half

        return left <= pos.x() <= right and top <= pos.y() <= bottom
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    def get_bounds(self):
        half = self._size // 2

        return QRect(self._x - half, self._y - half,
                     self._size, self._size)

    def resize(self, delta):
        new_size = self._size + delta
        if new_size >= 20:
            self._size = new_size
        return new_size >= 20

