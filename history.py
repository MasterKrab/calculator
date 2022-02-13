from PyQt6.QtWidgets import QWidget, QScrollArea, QLabel, QPushButton, QGridLayout, QVBoxLayout, QSizePolicy
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
import json


class History(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()

        title = QLabel("History")
        title.setFont(QFont("Poppins", 15))

        delete = QPushButton(clicked=self.delete_all)
        delete.setIcon(QIcon("trash.svg"))
        delete.setStyleSheet("border: none")
        delete.setFixedSize(20, 20)

        self.layout.addWidget(title)
        self.layout.addWidget(delete, 0, 1)

        self.setFixedWidth(300)

        self.add_history_items()

        self.setLayout(self.layout)

    def add_operation(self, operation, result, save=True):
        normalized_operation = operation

        for i in range(1, len(operation) // 25 + 1):
            position = i * 25
            normalized_operation = f"{normalized_operation[:position]}\n{normalized_operation[position:]}"

        normalized_result = result

        for i in range(1, len(result) // 17 + 1):
            position = i * 17
            normalized_result = f"{normalized_result[:position]}\n{normalized_result[position:]}"

        item = HistoryItem(normalized_operation, normalized_result)
        self.items.scroll_layout.insertWidget(0, item)

        if not save:
            return

        with open("history.json", "r+") as file:
            history = json.load(file)
            history["items"].append({"operation": normalized_operation, "result": normalized_result})
            file.seek(0)
            json.dump(history, file)

    def add_history_items(self):
        self.items = HistoryItems()
        self.layout.addWidget(self.items, 1, 0, 1, 2)

        with open("history.json", "r+") as file:
            try:
                history = json.load(file)["items"]

                for item in history:
                    self.add_operation(item["operation"], item["result"], False)
            except json.decoder.JSONDecodeError:
                json.dump({"items": []}, file)

    def delete_all(self):
        self.layout.removeWidget(self.items)
        self.items.deleteLater()

        with open("history.json", "w") as file:
            json.dump({"items": []}, file)

        self.add_history_items()


class HistoryItems(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setStyleSheet("background-color: transparent")
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("border: none")
        scroll.verticalScrollBar().setStyleSheet("QScrollBar:vertical {width: 10px; background: #fff;}"
                                                 "QScrollBar::handle {background: #111;}")
        self.layout.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scroll_content = QWidget(scroll)

        self.scroll_layout = QVBoxLayout(scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(0)
        scroll_content.setLayout(self.scroll_layout)

        scroll.setWidget(scroll_content)
        self.setLayout(self.layout)


class HistoryItem(QWidget):
    def __init__(self, operation, result):
        super().__init__()
        self.layout = QVBoxLayout()

        self.operation = QLabel(f"{operation} =")
        self.operation.setFont(QFont("Poppins", 12))
        self.operation.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.operation.setStyleSheet("color: #a1a1a1")

        self.result = QLabel(result)
        self.result.setFont(QFont("Poppins", 18))
        self.result.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.layout.addWidget(self.operation)
        self.layout.addWidget(self.result)

        self.setLayout(self.layout)
