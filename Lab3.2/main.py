from PyQt5.QtWidgets import QApplication
from view import View
from model import Model

if __name__ == "__main__":

    model = Model()
    app = QApplication([])
    window = View(model)
    window.show()
    app.exec_()