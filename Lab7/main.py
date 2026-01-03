from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog, QWidget, QMessageBox, QFileDialog, QVBoxLayout, QPushButton
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtCore import Qt, QRect

from Circle import Circle
from Square import Square
from Triangle import Triangle
from Container import Container
from Group import Group
from Factory import Factory
from Arrow import Arrow
from ShapesTree import ShapesTree


class Canvas(QWidget):
    def __init__(self, container):
        super().__init__()

        self.container = container
        self.container.subscribe(self)

        self.current_shape_type = None
        self.current_color = QColor("gray")

        self.setFocusPolicy(Qt.StrongFocus)

        self.arrow_mode = False
        self.arrow_source = None
        self.btn = None
        self.container.clear_selection()

    def activate_create_arrow(self):
        if self.arrow_mode:
            self.arrow_mode = False
            self.setCursor(Qt.ArrowCursor)

            self.container.clear_selection()
            return

        if len(self.container.get_shapes()) < 2:
            QMessageBox.warning(self, "Error", "Create at least two figures")
            return

        self.arrow_mode = True
        self.arrow_source = None
        self.setCursor(Qt.CrossCursor)

        self.container.clear_selection()


    def update(self, event = None):
        self.repaint()

    def set_shape_color(self, color):
        selected_shapes = [s for s in self.container.get_shapes() if s.is_selected()]

        if selected_shapes:
            for shape in selected_shapes:
                shape.set_color(color)
        self.current_color = color

    def set_shape_type(self, shape_type):
        self.current_shape_type = shape_type

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.container.clear_selection()
            self.arrow_mode = False
            self.arrow_source = None
            self.setCursor(Qt.ArrowCursor)
            return

        elif event.button() == Qt.LeftButton:
            pos = event.pos()
            ctrl_pressed = QApplication.keyboardModifiers() & Qt.ControlModifier

            arrow = self.container.get_arrow_at_point(pos)

            if arrow:
                if ctrl_pressed:
                    self.container.select_arrow(arrow, not arrow.is_selected())
                else:
                    self.container.clear_selection()
                    self.container.select_arrow(arrow, True)
                return

            if self.arrow_mode:
                shape = self.container.get_shape_at_point(pos)
                if shape is None:
                    return

                if self.arrow_source is None:
                    self.arrow_source = shape
                    self.container.clear_selection()
                    shape.set_selected(True)
                    return

                if shape is self.arrow_source:
                    return

                arrow = Arrow(self.arrow_source, shape)
                self.container.add_arrow(arrow)

                self.arrow_source = None
                self.arrow_mode = False
                self.setCursor(Qt.ArrowCursor)
                self.container.clear_selection()
                return

            shape = self.container.get_shape_at_point(pos)

            if shape is None:
                if not ctrl_pressed:
                    self.container.clear_selection()

                if self.current_shape_type is None:
                    QMessageBox.information(self, "Warning", "No shape selected")
                    return

                if self.current_shape_type == "circle":
                    shape = Circle(pos.x(), pos.y(), color=self.current_color)
                elif self.current_shape_type == "square":
                    shape = Square(pos.x(), pos.y(), color=self.current_color)
                elif self.current_shape_type == "triangle":
                    shape = Triangle(pos.x(), pos.y(), color=self.current_color)

                canvas_rect = QRect(0, 0, self.width(), self.height())
                if not shape.check_bounds(canvas_rect):
                    return

                self.container.add(shape)
                self.container.select_shape(shape, True)

            else:
                if ctrl_pressed:
                    self.container.select_shape(shape, not shape.is_selected())
                else:
                    self.container.clear_selection()
                    self.container.select_shape(shape, True)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.container.remove_selected()

        elif event.key() == Qt.Key_Plus:
            self.container.resize_shapes(5, self.rect())

        elif event.key() == Qt.Key_Minus:
            self.container.resize_shapes(-5, self.rect())

        elif event.key() == Qt.Key_Left:
            self.container.move_shapes(-3, 0, self.rect())

        elif event.key() == Qt.Key_Right:
            self.container.move_shapes(3, 0, self.rect())

        elif event.key() == Qt.Key_Up:
            self.container.move_shapes(0, -3, self.rect())

        elif event.key() == Qt.Key_Down:
            self.container.move_shapes(0, 3, self.rect())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for shape in self.container.get_shapes():
            shape.draw(painter)

        for arrow in self.container.get_arrows():
            arrow.draw(painter)


    def group_selected_shapes(self):
        selected_shapes = []

        for shape in self.container.get_shapes():
            if shape.is_selected():
                selected_shapes.append(shape)
                self.container.select_shape(shape, False)

        if not selected_shapes:
            return

        for shape in selected_shapes:
            self.container.get_shapes().remove(shape)

        group = Group(shapes = selected_shapes)
        self.container.clear_selection()
        self.container.select_shape(group, True)
        self.container.add(group)


    def ungroup_selected_shapes(self):
        selected_groups = []
        for g in self.container.get_shapes():
            if g.is_selected() and isinstance(g, Group):
                selected_groups.append(g)

        for g in selected_groups:
            self.container.get_shapes().remove(g)

            for child in g.get_child():
                self.container.select_shape(child, False)
                self.container.add(child)


    def delete_all_shapes(self):
            self.container.delete_shapes()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("shapes3.ui", self)

        self.factory = Factory()
        self.container = Container(self.factory)
        self.canvas = Canvas(self.container)
        self.create_arrow_button()

        layout = QVBoxLayout(self.canvasPlaceholder)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)

        self.tree = ShapesTree(self.treeWidget, self.container)

        self.actionCircle.triggered.connect(lambda:self.canvas.set_shape_type("circle"))
        self.actionSquare.triggered.connect(lambda:self.canvas.set_shape_type("square"))
        self.actionTriangle.triggered.connect(lambda:self.canvas.set_shape_type("triangle"))

        self.actionColor.triggered.connect(self.show_color_dialog)
        self.actionSave.triggered.connect(self.show_save_dialog)
        self.actionLoad.triggered.connect(self.show_load_dialog)
        self.actionGroup.triggered.connect(self.canvas.group_selected_shapes)
        self.actionUngroup.triggered.connect(self.canvas.ungroup_selected_shapes)
        self.actionDelete.triggered.connect(self.canvas.delete_all_shapes)

    def create_arrow_button(self):

        self.btn = QPushButton("Create →", self.canvas)
        self.btn.setFixedSize(70, 30)
        self.btn.move(10, 10)
        self.btn.clicked.connect(self.canvas.activate_create_arrow)

        self.btn.raise_()

    def show_color_dialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.canvas.set_shape_color(color)

    def show_save_dialog(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Сохранить проект", "", "Text files (*.txt)")
        if filename:
            self.canvas.container.save(filename)

    def show_load_dialog(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Загрузить проект", "", "Text files (*.txt)")
        if filename:
            self.canvas.container.load(filename)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()