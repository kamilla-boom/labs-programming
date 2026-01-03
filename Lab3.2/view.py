from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow


class View(QMainWindow):
    def __init__(self, model):
        super().__init__()
        uic.loadUi("mvc.ui", self)

        self.spinBoxA.setRange(0, 100)
        self.spinBoxB.setRange(0, 100)
        self.spinBoxC.setRange(0, 100)

        self.sliderA.setRange(0, 100)
        self.sliderB.setRange(0, 100)
        self.sliderC.setRange(0, 100)

        self.model = model
        self.model.subscribe(self.update_widget)

        self.connect_signals()
        self.update_widget()

    def connect_signals(self):
        self.lineA.editingFinished.connect(self.lineupdate_a)
        self.lineB.editingFinished.connect(self.lineupdate_b)
        self.lineC.editingFinished.connect(self.lineupdate_c)

        self.spinBoxA.valueChanged.connect(lambda a: self.model.set_a(a))
        self.spinBoxB.valueChanged.connect(lambda b: self.model.set_b(b))
        self.spinBoxC.valueChanged.connect(lambda c: self.model.set_c(c))

        self.sliderA.valueChanged.connect(lambda a: self.model.set_a(a))
        self.sliderB.valueChanged.connect(lambda b: self.model.set_b(b))
        self.sliderC.valueChanged.connect(lambda c: self.model.set_c(c))

    def lineupdate_a(self):
        text = self.lineA.text()
        if not text.isdigit():
            self.lineA.setText(str(self.model.get_a()))
            return
        self.model.set_a(int(text))

    def lineupdate_b(self):
        text = self.lineB.text()
        if not text.isdigit():
            self.lineB.setText(str(self.model.get_b()))
            return
        self.model.set_b(int(text))

    def lineupdate_c(self):
        text = self.lineC.text()
        if not text.isdigit():
            self.lineC.setText(str(self.model.get_c()))
            return
        self.model.set_c(int(text))

    def update_widget(self):

        a = self.model.get_a()
        b = self.model.get_b()
        c = self.model.get_c()

        self.lineA.setText(str(a))
        self.lineB.setText(str(b))
        self.lineC.setText(str(c))

        self.spinBoxA.setValue(a)
        self.spinBoxB.setValue(b)
        self.spinBoxC.setValue(c)

        self.sliderA.setValue(a)
        self.sliderB.setValue(b)
        self.sliderC.setValue(c)






