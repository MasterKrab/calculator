from PyQt6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QSizePolicy
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class Display(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QLineEdit {
                background-color: transparent;
                border: none;
                color: #a1a1a1;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.top = QLineEdit()
        self.top.setReadOnly(True)
        self.top.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.top.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.top.setFont(QFont("Poppins", 14))

        self.bottom = QLineEdit()
        self.bottom.setPlaceholderText("0")
        self.bottom.setReadOnly(True)
        self.bottom.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.bottom.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.bottom.setFont(QFont("Poppins", 20))

        layout.addWidget(self.top)
        layout.addWidget(self.bottom)

        self.setLayout(layout)
        self.setGeometry(0, 0, 300, 300)
