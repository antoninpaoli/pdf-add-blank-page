from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QSpinBox, QRadioButton, QCheckBox, QPushButton
from PyQt5.QtCore import Qt
from .core import add_blank_page
from .strategies import EndOfFilePageStrategy, BetweenPageStrategy

import sys
import os

class DropLabel(QLabel):
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        pos = event.pos()
        text = event.mimeData().text()
        self.setText(text)
        event.acceptProposedAction()


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Chépa')
        self.button = None
        self.file = None
        self.isTransparent = None
        self.EndOfFilePageStrategy: QRadioButton = None
        self.BetweenPageStrategy: QRadioButton = None
        self.nbBlankPage: QSpinBox = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.addLayout(self.dropLabel())
        layout.addWidget(QLabel('______________________________________________________________________________________'))
        layout.addLayout(self.parameters())
        layout.addWidget(QLabel('______________________________________________________________________________________'))
        layout.addLayout(self.spinBox())
        layout.addWidget(QLabel('______________________________________________________________________________________'))
        layout.addWidget(self.pushButton())
        self.setLayout(layout)

    def dropLabel(self):
        layoutDL = QVBoxLayout()
        layoutDL.addWidget(QLabel('Image :'))
        self.file = DropLabel("DROP YOUR DOCUMENT HERE", self)
        self.file.setStyleSheet(' QLabel { background-color: rgb(0,0,128); color: white; font-family: courier; } ')
        layoutDL.addWidget(self.file)
        return layoutDL

    def spinBox(self):
        layoutSB = QVBoxLayout()
        layoutSB.addWidget(QLabel('Nombre de pages blanche :'))
        self.nbBlankPage = QSpinBox()
        layoutSB.addWidget(self.nbBlankPage)
        return layoutSB

    def parameters(self):
        layoutP = QHBoxLayout()
        layoutP.addWidget(QLabel('Paramètres :'))
        self.EndOfFilePageStrategy = QRadioButton("ajouter les pages à la fin")
        layoutP.addWidget(self.EndOfFilePageStrategy)
        self.BetweenPageStrategy = QRadioButton("ajouter les pages au milieu")
        layoutP.addWidget(self.BetweenPageStrategy)
        self.isTransparent = QCheckBox("transparence")
        layoutP.addWidget(self.isTransparent)
        return layoutP

    def pushButton(self):
        self.button = QPushButton("Créer le pdf")
        self.button.clicked.connect(self.btnstate)
        return self.button

    def btnstate(self):
        if(self.EndOfFilePageStrategy.isChecked()):
            strategy = BetweenPageStrategy(int(self.nbBlankPage.text()), 0.7)
        else:
            strategy = EndOfFilePageStrategy(int(self.nbBlankPage.text()))
        add_blank_page(self.file.text().replace('file:///', ''), strategy)


def ui():
    app = QApplication(sys.argv)
    myApp = MyApp()
    myApp.resize(800, 400)
    myApp.show()
    sys.exit(app.exec_())
