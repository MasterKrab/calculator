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

        self.resize_edge_width = 20
        self.resize_mode = None
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        self.start = event.pos()

        self.resize_mode = set()

        if self.start.x() > self.width() - self.resize_edge_width:
            self.resize_mode.add('right')
        elif self.start.x() < self.resize_edge_width:
            self.resize_mode.add('left')

        if self.start.y() > self.height() - self.resize_edge_width:
            self.resize_mode.add('bottom')
        elif self.start.y() < self.resize_edge_width:
            self.resize_mode.add('top')

    def mouseMoveEvent(self, event):
        end = event.pos()

        x = end.x()
        y = end.y()

        is_left = x < self.resize_edge_width
        is_right = x > self.width() - self.resize_edge_width
        is_top = y < self.resize_edge_width
        is_bottom = y > self.height() - self.resize_edge_width

        if (is_left and is_top) or (is_right and is_bottom):
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        elif (is_left and is_bottom) or (is_right and is_top):
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        elif is_left or is_right:
            self.setCursor(Qt.CursorShape.SizeHorCursor)
        elif is_top or is_bottom:
            self.setCursor(Qt.CursorShape.SizeVerCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

        if not self.resize_mode:
            return

        if "left" in self.resize_mode:
            geometry = self.geometry()

            geometry.setLeft(self.mapToGlobal(end).x())

            if self.maximumWidth() > geometry.width() > self.minimumWidth():
                self.setGeometry(geometry)

        elif "right" in self.resize_mode:
            geometry = self.geometry()
            geometry.setRight(self.mapToGlobal(end).x())
            self.setGeometry(geometry)

        if "top" in self.resize_mode:
            geometry = self.geometry()
            geometry.setTop(self.mapToGlobal(end).y())

            if self.maximumHeight() > geometry.height() > self.minimumHeight():
                self.setGeometry(geometry)
        elif "bottom" in self.resize_mode:
            geometry = self.geometry()
            geometry.setBottom(self.mapToGlobal(end).y())
            self.setGeometry(geometry)

    def mouseReleaseEvent(self, event):
        self.resize_mode = None


app = QApplication([])
QFontDatabase.addApplicationFont("Poppins.ttf")
window = Window()
window.show()
sys.exit(app.exec())
