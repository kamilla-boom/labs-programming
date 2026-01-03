from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog, QWidget, QMessageBox
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtCore import Qt, QRect
from Circle import Circle
from Square import Square
from Triangle import Triangle
from Container import Container


class Canvas(QWidget):
    def __init__(self):
        super().__init__()

        self.container = Container()
        self.current_shape_type = None
        self.current_color = QColor("gray")

        self.setFocusPolicy(Qt.StrongFocus)
        self.setStyleSheet("background-color: white;")

    def set_shape_color(self, color):
        selected_shapes = [s for s in self.container.get_shapes() if s.is_selected()]

        if selected_shapes:
            for shape in selected_shapes:
                shape.set_color(color)
        self.current_color = color

        self.update()
    def set_shape_type(self, shape_type):
        self.current_shape_type = shape_type

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.container.clear_selection()
            self.update()

        elif event.button() == Qt.LeftButton:
            pos = event.pos()
            ctrl_pressed = QApplication.keyboardModifiers() & Qt.ControlModifier

            shape = self.container.get_shape_at_point(pos)

            if shape is None:

                if not ctrl_pressed:
                    self.container.clear_selection()
                if self.current_shape_type is None:
                    QMessageBox.information(self, "Warning", "No shape selected")
                    return
                else:
                    if self.current_shape_type == "circle":
                        shape = Circle(pos.x(), pos.y(), color=self.current_color)
                    elif self.current_shape_type == "square":
                        shape = Square(pos.x(), pos.y(), color=self.current_color)
                    elif self.current_shape_type == "triangle":
                        shape = Triangle(pos.x(), pos.y(), color=self.current_color)

                canvas_rect = QRect(0, 0, self.width(), self.height())

                if not shape.check_bounds(canvas_rect):
                    return

                shape.set_selected(True)
                self.container.add(shape)

            else:
                if ctrl_pressed:
                    shape.set_selected(not shape.is_selected())

                else:
                    self.container.clear_selection()
                    shape.set_selected(True)

            self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.container.remove_selected()
            self.update()

        elif event.key() == Qt.Key_Plus:
            self.resize_selected_shapes(5)
            self.update()

        elif event.key() == Qt.Key_Minus:
            self.resize_selected_shapes(-5)
            self.update()

        elif event.key() == Qt.Key_Left:
            self.move_selected_shapes(-3, 0)
            self.update()

        elif event.key() == Qt.Key_Right:
            self.move_selected_shapes(3, 0)
            self.update()

        elif event.key() == Qt.Key_Up:
            self.move_selected_shapes(0, -3)
            self.update()

        elif event.key() == Qt.Key_Down:
            self.move_selected_shapes(0, 3)
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for shape in self.container.get_shapes():
            shape.draw(painter)

    def resize_selected_shapes(self, delta):
        canvas_rect = QRect(0, 0, self.width(), self.height())

        for shape in self.container.get_shapes():
            if shape.is_selected():
                if shape.resize(delta):
                    if not shape.check_bounds(canvas_rect):
                        shape.resize(-delta)

    def move_selected_shapes(self, dx, dy):
        canvas_rect = QRect(0, 0, self.width(), self.height())
        for shape in self.container.get_shapes():
            if shape.is_selected():
                old_x, old_y = shape.get_position()
                shape.move(dx, dy)

                if  not shape.check_bounds(canvas_rect):
                    shape.set_position(old_x, old_y)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("shapes.ui", self)

        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)

        self.actionCircle.triggered.connect(lambda:self.canvas.set_shape_type("circle"))
        self.actionSquare.triggered.connect(lambda:self.canvas.set_shape_type("square"))
        self.actionTriangle.triggered.connect(lambda:self.canvas.set_shape_type("triangle"))

        self.actionColor.triggered.connect(self.show_color_dialog)

    def show_color_dialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.canvas.set_shape_color(color)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()