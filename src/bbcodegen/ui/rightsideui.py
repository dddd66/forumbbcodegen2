from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QRadioButton,
    QWidget,
)

from ..helpers import RedTextLabel
from ..models import RightFormInput


class CreateRightWidget(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QFormLayout(self)
        self.screenshot_shown = 4

        self.cover_label = RedTextLabel("Poster:")
        self.cover_input = QLineEdit()
        main_layout.addRow(self.cover_label, self.cover_input)
        screenshot_display = self.create_screenshot_display()
        main_layout.addRow(screenshot_display)
        screenshot_changer = self.create_screenshot_changer()
        main_layout.addRow(screenshot_changer)
        self.bottom_right = CreateBottomRight()
        main_layout.addRow(self.bottom_right)

        self.setLayout(main_layout)

    def create_screenshot_display(self) -> QWidget:
        main_widget = QWidget()
        self.screenshot_display_lines = QFormLayout(main_widget)
        self.screenshot_display_lines.setContentsMargins(0, 0, 0, 0)

        self.screenshot_input_list: list[QLineEdit] = []
        for idx in range(8):
            label = RedTextLabel(f"Screenshot {idx + 1}")
            line = QLineEdit()
            self.screenshot_input_list.append(line)
            self.screenshot_display_lines.addRow(label, line)
        for idx in range(4):
            self.screenshot_display_lines.setRowVisible(4 + idx, False)

        return main_widget

    def change_screenshot_count(self, change_to: int) -> None:
        self.screenshot_shown = change_to
        for idx in range(8):
            self.screenshot_display_lines.setRowVisible(idx, idx < change_to)

    def create_screenshot_changer(self) -> QWidget:
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.screenshot_group = QButtonGroup()

        btn4 = QRadioButton("4")
        btn6 = QRadioButton("6")
        btn8 = QRadioButton("8")

        btn4.setChecked(True)

        self.screenshot_group.addButton(btn4, 4)
        self.screenshot_group.addButton(btn6, 6)
        self.screenshot_group.addButton(btn8, 8)
        main_layout.addWidget(btn4)
        main_layout.addWidget(btn6)
        main_layout.addWidget(btn8)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.screenshot_group.idClicked.connect(self.change_screenshot_count)
        return main_widget

    def get_data(self) -> RightFormInput:
        screenshot_list: list[str] = []
        for idx in range(self.screenshot_shown):
            line: str = self.screenshot_input_list[idx].text()
            if line.strip():
                screenshot_list.append(line)
        bottom_right_data = self.bottom_right.get_data()
        upper_right_data = {
            "poster": self.cover_input.text(),
            "screenshots": ",".join(screenshot_list),
        }
        return RightFormInput(**(bottom_right_data | upper_right_data))


class CreateBottomRight(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QFormLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.awards_label = QLabel("Premiações:")
        self.awards_input = QPlainTextEdit()
        main_layout.addRow(self.awards_label, self.awards_input)

        self.trivia_label = QLabel("Curiosidade:")
        self.trivia_input = QPlainTextEdit()
        main_layout.addRow(self.trivia_label, self.trivia_input)

        self.review_label = QLabel("Crítica:")
        self.review_input = QPlainTextEdit()
        main_layout.addRow(self.review_label, self.review_input)

        self.setLayout(main_layout)

    def get_data(self) -> dict[str, str]:
        return {
            "awards": self.awards_input.toPlainText(),
            "trivia": self.trivia_input.toPlainText(),
            "review": self.review_input.toPlainText(),
        }
