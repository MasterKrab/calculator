from PyQt6.QtWidgets import QToolBar, QWidget, QLabel, QSizePolicy
from PyQt6.QtGui import QFont


class TopBar(QToolBar):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setMovable(False)
        self.setStyleSheet("""
            QToolBar {
                border: none;
            }
            
            QToolButton {
                padding: 0;
                border: none;
                width: 20px;
            }
        """)

        title = QLabel("Calculator")
        title.setFont(QFont("Poppins", 18))
        self.addWidget(title)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.addWidget(spacer)

        minimize_button = self.addAction("-")
        minimize_button.setToolTip("Minimize")
        minimize_button.triggered.connect(self.parent.showMinimized)
        minimize_button.setFont(QFont("Poppins", 18))

        button_close = self.addAction("×")
        button_close.setToolTip("Close")
        button_close.triggered.connect(self.parent.close)
        button_close.setFont(QFont("Poppins", 20))

        self.start = None
        self.is_pressed = False

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())

    def mouseMoveEvent(self, event):
        end = self.mapToGlobal(event.pos())
        delta = end - self.start
        self.parent.move(self.parent.pos() + delta)

        self.start = end
