from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout, QSizePolicy
from display import Display
from utils import replace_operators, evaluate


class Calculator(QWidget):
    def __init__(self, history=None):
        super().__init__()
        self.history = history

        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(50, 50, 50, 0.5);
                border: none;
                font-size: 20px;
            }

            QPushButton:hover {
                background-color: rgba(50, 50, 50, 0.8);
            }

            QPushButton:pressed {
                background-color: rgba(50, 50, 50, 0.9);
            }
        """)

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.display = Display()
        self.layout.addWidget(self.display, 0, 0, 1, 4)

        self.add_buttons()

        self.setLayout(self.layout)

        self.operation = ""
        self.operators = {"+", "-", "*", "/"}
        self.result = ""

    def add_buttons(self):
        button_7 = QPushButton("7", clicked=lambda: self.add_number("7"))
        button_8 = QPushButton("8", clicked=lambda: self.add_number("8"))
        button_9 = QPushButton("9", clicked=lambda: self.add_number("9"))
        button_4 = QPushButton("4", clicked=lambda: self.add_number("4"))
        button_5 = QPushButton("5", clicked=lambda: self.add_number("5"))
        button_6 = QPushButton("6", clicked=lambda: self.add_number("6"))
        button_1 = QPushButton("1", clicked=lambda: self.add_number("1"))
        button_2 = QPushButton("2", clicked=lambda: self.add_number("2"))
        button_3 = QPushButton("3", clicked=lambda: self.add_number("3"))
        button_0 = QPushButton("0", clicked=lambda: self.add_number("0"))

        button_clear = QPushButton("Clear", clicked=self.clear)
        button_delete = QPushButton("DEL", clicked=self.delete)

        button_add = QPushButton("+", clicked=lambda: self.add_operator("+"))
        button_subtract = QPushButton("-", clicked=lambda: self.add_operator("-"))
        button_multiply = QPushButton("×", clicked=lambda: self.add_operator("*"))
        button_divide = QPushButton("÷", clicked=lambda: self.add_operator("/"))
        button_equal = QPushButton("=", clicked=self.calculate)
        button_point = QPushButton(".", clicked=self.add_point)

        button_7.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button_8.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button_9.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button_4.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button_5.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button_6.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button_1.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button_2.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button_3.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button_0.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        button_clear.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button_delete.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button_add.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button_subtract.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button_multiply.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button_divide.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button_equal.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button_point.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layout.addWidget(button_7, 1, 0)
        self.layout.addWidget(button_8, 1, 1)
        self.layout.addWidget(button_9, 1, 2)
        self.layout.addWidget(button_4, 2, 0)
        self.layout.addWidget(button_5, 2, 1)
        self.layout.addWidget(button_6, 2, 2)
        self.layout.addWidget(button_1, 3, 0)
        self.layout.addWidget(button_2, 3, 1)
        self.layout.addWidget(button_3, 3, 2)
        self.layout.addWidget(button_0, 4, 1)

        self.layout.addWidget(button_point, 4, 0)
        self.layout.addWidget(button_clear, 5, 0, 1, 2)
        self.layout.addWidget(button_delete, 1, 3)
        self.layout.addWidget(button_add, 2, 3)
        self.layout.addWidget(button_subtract, 3, 3)
        self.layout.addWidget(button_multiply, 4, 3)
        self.layout.addWidget(button_divide, 4, 2)
        self.layout.addWidget(button_equal, 5, 2, 1, 2)

    def print_operation(self):
        self.display.top.setText(f"Ans: {self.result}" if self.result else "")

        self.display.bottom.setStyleSheet("color: #fff")
        self.display.bottom.setText(replace_operators(self.operation))

    def print_error(self, error="Error"):
        self.display.bottom.setStyleSheet("color: #f00")
        self.display.bottom.setText(error)

    def add_number(self, number):
        self.operation += number
        self.print_operation()

    def add_point(self):
        if not self.operation or "." not in self.operation[-1]:
            self.operation += "."
            self.print_operation()

    def add_operator(self, operator):
        if not self.operation:
            text = self.display.bottom.text()

            if text and "Error" not in text:
                self.operation = f"{text}{operator}"
        elif self.operation[-1] in self.operators:
            self.operation = self.operation[:-1] + operator
        else:
            self.operation += operator

        self.print_operation()

    def calculate(self):
        if not self.operation:
            return

        try:
            self.result = evaluate(self.operation)

            if self.history:
                self.history.add_operation(self.operation, self.result)

            self.display.top.setText(replace_operators(self.operation))
            self.display.bottom.setText(self.result)
        except ZeroDivisionError:
            self.print_error("Error, Cannot divide by zero")
        except (SyntaxError, ValueError) as error:
            print(self.operation, error)
            self.print_error("Syntax Error")
        except Exception:
            self.print_error()
        finally:
            self.operation = ""

    def clear(self):
        self.operation = ""
        self.display.top.setText("")
        self.display.bottom.setText("")

    def delete(self):
        self.operation = self.operation[:-1]
        self.display.bottom.setText(self.display.bottom.text()[:-1])
