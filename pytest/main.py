import sys
import random
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCore import QUrl
from PySide2.QtWebEngineWidgets import QWebEngineView

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World")
        self.text.setAlignment(QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.button.clicked.connect(self.magic)

        self.view = QWebEngineView()
        self.view.load(QUrl("https://baidu.com"))
        self.view.loadFinished.connect(self.loadFinished)
        self.layout.addWidget(self.view)

    def magic(self):
        self.text.setText(random.choice(self.hello))

    def loadFinished(self, finished):
        print("load finished")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())
