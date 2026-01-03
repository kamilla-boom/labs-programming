from abc import ABC, abstractmethod

class Shape(ABC):

    def __init__(self, x, y, color = None):
        self._x = x
        self._y = y
        self._color = color
        self._selected = False

    def set_selected(self, selected):
        self._selected = selected
    def is_selected(self):
        return self._selected

    def set_color(self, color):
        self._color = color

    def move(self, dx, dy):
        self._x += dx
        self._y += dy

    def set_position(self, x, y):
        self._x = x
        self._y = y
    def get_position(self):
        return self._x, self._y

    def check_bounds(self, canvas_rect):
        bounds = self.get_bounds()
        return canvas_rect.contains(bounds)

    @abstractmethod
    def get_bounds(self): pass

    @abstractmethod
    def draw(self, painter): pass

    @abstractmethod
    def contains_point(self, pos): pass

    @abstractmethod
    def resize(self, delta): pass