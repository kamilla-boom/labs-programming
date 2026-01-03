from abc import ABC, abstractmethod
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtCore import Qt

class IShape(ABC):
    @abstractmethod
    def draw(self, painter): pass

    @abstractmethod
    def contains_point(self, pos): pass

    @abstractmethod
    def set_selected(self, selected): pass

    @abstractmethod
    def is_selected(self): pass

class Circle(IShape):
    def __init__(self, x, y, radius=40):
        self.__x = x
        self.__y = y
        self.__radius = radius
        self.__selected = False

    def contains_point(self, pos):
        dx = pos.x() - self.__x
        dy = pos.y() - self.__y
        return dx * dx + dy * dy <= self.__radius * self.__radius   # √(dx² + dy²)

    def set_selected(self, selected):
        self.__selected = selected

    def is_selected(self):
        return self.__selected

    def draw(self, painter):
        if self.__selected:
            painter.setPen(QPen(Qt.red, 3))
            painter.setBrush(QBrush(QColor("#FFC0CB")))
        else:
            painter.setPen(QPen(Qt.gray, 1))
            painter.setBrush(QBrush(QColor("#FFFFFF")))

        painter.drawEllipse(self.__x - self.__radius,
                            self.__y - self.__radius,
                            self.__radius * 2,
                            self.__radius * 2)


class Container:
    def __init__(self):
        self.__shapes = []
        self.__current_index = 0

    def add(self, shape):
        self.__shapes.append(shape)

    def get_shapes(self):
        return self.__shapes

    def clear_selection(self):
        for shape in self.__shapes:
            shape.set_selected(False)

    def remove_selected(self):
        self.__shapes = [shape for shape in self.__shapes if not shape.is_selected()]

    def get_shape_at_point(self, pos):
        for shape in reversed(self.__shapes):
            if shape.contains_point(pos):
                return shape
        return None

    def first(self):
        self.__current_index = 0

    def next(self):
        self.__current_index += 1

    def is_end(self):
        return self.__current_index >= len(self.__shapes)

    def get_object(self):
        if not self.is_end():
            return self.__shapes[self.__current_index]
        return None

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.container = Container()
        self.setFocusPolicy(Qt.StrongFocus)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            ctrl_pressed = QApplication.keyboardModifiers() & Qt.ControlModifier


            shape = self.container.get_shape_at_point(pos)

            if shape is None:
                if not ctrl_pressed:
                    self.container.clear_selection()
                new_circle = Circle(pos.x(), pos.y())
                new_circle.set_selected(True)
                self.container.add(new_circle)
            else:
                if ctrl_pressed:
                    shape.set_selected(not shape.is_selected())
                else:
                    self.container.clear_selection()
                    shape.set_selected(True)

            self.update()
            self.setFocus()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.container.remove_selected()
            self.update()
        else:
            super().keyPressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        self.container.first()
        while not self.container.is_end():
            shape = self.container.get_object()
            shape.draw(painter)
            self.container.next()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Кружочки")
        self.resize(800, 600)
        self.setStyleSheet("background-color: rgb(16, 184, 150);")

        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
    