from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QFont


class TopBar(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setFixedHeight(50)
        self.setMouseTracking(True)

        self.layout = QHBoxLayout()

        title = QLabel("Calculator")
        title.setFont(QFont("Poppins", 18))

        button_close = QPushButton("×", clicked=self.parent.close)
        button_close.setFont(QFont("Poppins", 20))
        button_close.setFixedSize(20, 20)
        button_close.setStyleSheet("border: none;")

        self.layout.addWidget(title)
        self.layout.addWidget(button_close)
        self.setLayout(self.layout)

        self.start = None
        self.is_pressed = False

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.is_pressed = True

    def mouseMoveEvent(self, event):
        if not self.is_pressed:
            return

        end = self.mapToGlobal(event.pos())
        delta = end - self.start
        self.parent.move(self.parent.pos() + delta)

        self.start = end

    def mouseReleaseEvent(self, event):
        self.is_pressed = False
