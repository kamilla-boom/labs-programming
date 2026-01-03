from PyQt5 import uic #, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton, QCheckBox, QHBoxLayout, QDialog, \
    QLabel, QLineEdit
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QPen, QMovie
from PyQt5.QtCore import Qt
from os import startfile
#import sys

class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Change weather now")
        layout = QHBoxLayout()

        self.labelgif = QLabel()
        layout.addWidget(self.labelgif)

        self.sun_gif_path = "C:/Programming/test_project/sun.gif"
        self.snow_gif_path = "C:/Programming/test_project/snow.gif"
        self.rain_gif_path = "C:/Programming/test_project/rain.gif"

        self.movie = QMovie(self.sun_gif_path)
        self.movie1 = QMovie(self.snow_gif_path)
        self.movie2 = QMovie(self.rain_gif_path)

        self.labelgif.setMovie(self.movie)
        self.movie.start()

        self.checkbox1 = QCheckBox("Снег")
        self.checkbox2 = QCheckBox("Дождь")
        layout.addWidget(self.checkbox1)
        layout.addWidget(self.checkbox2)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

        self.checkbox1.stateChanged.connect(self.update_weather)
        self.checkbox2.stateChanged.connect(self.update_weather)

    def update_weather(self):
        if self.checkbox1.isChecked():
            self.checkbox2.setEnabled(False)
            self.labelgif.setMovie(self.movie1)
            self.movie.stop()
            self.movie2.stop()
            self.movie1.start()
        elif self.checkbox2.isChecked():
            self.checkbox1.setEnabled(False)
            self.labelgif.setMovie(self.movie2)
            self.movie.stop()
            self.movie1.stop()
            self.movie2.start()
        else:
            self.checkbox1.setEnabled(True)
            self.checkbox2.setEnabled(True)
            self.labelgif.setMovie(self.movie)
            self.movie1.stop()
            self.movie2.stop()
            self.movie.start()


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("calc.ui", self)

        self.cw = self.centralWidget()

        self.btn_print_result.clicked.connect(self.print_result)
        self.btn_delete.clicked.connect(self.delete)
        self.btn_zero.clicked.connect(lambda:self.write_calculator(self.btn_zero.text()))
        self.btn_one.clicked.connect(lambda:self.write_calculator(self.btn_one.text()))
        self.btn_two.clicked.connect(lambda:self.write_calculator(self.btn_two.text()))
        self.btn_three.clicked.connect(lambda:self.write_calculator(self.btn_three.text()))
        self.btn_four.clicked.connect(lambda:self.write_calculator(self.btn_four.text()))
        self.btn_five.clicked.connect(lambda:self.write_calculator(self.btn_five.text()))
        self.btn_six.clicked.connect(lambda:self.write_calculator(self.btn_six.text()))
        self.btn_seven.clicked.connect(lambda:self.write_calculator(self.btn_seven.text()))
        self.btn_eight.clicked.connect(lambda:self.write_calculator(self.btn_eight.text()))
        self.btn_nine.clicked.connect(lambda:self.write_calculator(self.btn_nine.text()))
        self.btn_division.clicked.connect(lambda:self.write_calculator(self.btn_division.text()))
        self.btn_multiplication.clicked.connect(lambda:self.write_calculator(self.btn_multiplication.text()))
        self.btn_plus.clicked.connect(lambda:self.write_calculator(self.btn_plus.text()))
        self.btn_minus.clicked.connect(lambda:self.write_calculator(self.btn_minus.text()))

        self.lightaction.triggered.connect(self.light)
        self.darkaction.triggered.connect(self.dark)

        self.btn_saveInfo.clicked.connect(self.save_info)
        self.btn_openInfo.clicked.connect(self.open_info)

        self.horizontalSliderCourse.valueChanged.connect(self.spinboxCourse.setValue)
        self.spinboxCourse.valueChanged.connect(self.horizontalSliderCourse.setValue)

        self.horizontalSliderCourse.setRange(1, 7)
        self.spinboxCourse.setRange(1, 7)

        self.comboboxDirection.addItems(["PRO","MO","EP"])

        self.pixmap2 = QPixmap("C:/Programming/test_project/2.jpg")
        self.pixmap1 = QPixmap("C:/Programming/test_project/1.jpg")
        self.label_picture1.setPixmap(self.pixmap1)
        self.label_picture1.setScaledContents(True)
        self.current_picture = 1
        self.label_picture1.mousePressEvent = self.change_picture

        self.widget_btn.mousePressEvent = self.dynamic_btn
        self.btn_counter = 1

        self.points = []
        self.widget_btn.paintEvent = self.paint_widget_btn

        self.openwindow_btn.clicked.connect(self.open_window)
        # toPlain для TextEdit

        self.Slider.setRange(0,100)
        self.Slider.valueChanged.connect(lambda: self.label.setText(f"Текущее значение:{self.Slider.value()}"))

        self.lineEdit_2.textChanged.connect(self.change_checkBox)

    def change_checkBox(self):
        text = self.lineEdit_2.text()
        if text == "":
            self.checkBox_2.setChecked(False)
        else:
            self.checkBox_2.setChecked(True)

    def lineEdit_changed(self):
        if self.checkBox.isChecked() == True:
            self.lineEdit.setEchoMode(QLineEdit.Password)
        else:
            self.lineEdit.setEchoMode(QLineEdit.Normal)

    def write_calculator(self, symbol):
        if self.label_result.text() == "0":
            self.label_result.setText(symbol)
        else:
            self.label_result.setText(self.label_result.text() + symbol)

    def print_result(self):
        res = eval(self.label_result.text())
        self.label_result.setText(str(res))
    def delete(self):
        self.label_result.setText("0")

    def light(self):
        self.cw.setStyleSheet("background-color: rgb(230, 230, 230)")
    def dark(self):
        self.cw.setStyleSheet("background-color: rgb(50, 50, 50)")

    def save_info(self):
        print("Сохраняю данные...")
        lines = [str(self.lineeditFIO.text()), str(self.spinboxCourse.text()), str(self.comboboxDirection.currentText())]
        with open("C:/Programming/test_project/Save.txt", "w", encoding="utf-8") as file:
            file.write("; ".join(lines))
    def open_info(self):
        startfile("C:/Programming/test_project/Save.txt")

    def change_picture(self, event):
        if self.current_picture == 1:
            self.label_picture1.setPixmap(self.pixmap2)
            self.current_picture = 2
        else:
            self.label_picture1.setPixmap(self.pixmap1)
            self.current_picture = 1

    def paint_widget_btn(self, event):
        painter = QPainter(self.widget_btn)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(QBrush(Qt.red))

        for x, y in self.points:
            painter.drawEllipse(x-5, y-5, 10, 10)

    def dynamic_btn(self, event):
        if event.button() == Qt.LeftButton:
            x, y = event.pos().x(), event.pos().y()

            self.points.append((x, y))
            self.widget_btn.update()
            btn = QPushButton(f"Кнопка {self.btn_counter}", self.widget_btn)
            btn.move(x - 20, y - 10)
            btn.show()

            btn.clicked.connect(btn.deleteLater)

            self.btn_counter += 1

    def open_window(self):
        dialog = MyDialog()
        dialog.exec_()




