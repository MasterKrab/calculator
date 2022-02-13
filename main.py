from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QSizePolicy
from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtCore import Qt
from styles import STYLESHEET
from top_bar import TopBar
from history import History
from calculator import Calculator
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet(STYLESHEET)
        self.setMinimumSize(750, 450)
        self.setMaximumSize(1000, 650)
        self.resize(800, 500)

        self.setFont(QFont("Poppins", 14))

        self.layout = QGridLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        self.top_bar = TopBar(self)

        self.history = History()

        self.calculator = Calculator(self.history)
        self.calculator.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layout.addWidget(self.top_bar, 0, 0, 1, 2)
        self.layout.addWidget(self.calculator, 1, 0)
        self.layout.addWidget(self.history, 1, 1)
        self.setLayout(self.layout)

    def mousePressEvent(self, event):
        position = event.pos()

        self.start = position

        self.is_resizing = position.x() > self.width() - 20 or position.y() > self.height() - 20

    def mouseMoveEvent(self, event):
        if not self.is_resizing:
            return

        position = event.pos()

        delta = position - self.start
        self.start = position

        self.resize(self.width() + delta.x(), self.height() + delta.y())

    def mouseReleaseEvent(self, event):
        self.is_resizing = False


app = QApplication([])
QFontDatabase.addApplicationFont("Poppins.ttf")
window = Window()
window.show()
sys.exit(app.exec())
