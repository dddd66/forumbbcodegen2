from PySide6.QtWidgets import (
    QVBoxLayout, QFormLayout, QHBoxLayout,
    QLineEdit, QRadioButton, QButtonGroup,
    QLabel, QWidget, QFrame
)
from PySide6.QtCore import Qt
from mko_bbcode.ui.wizard.pages._base import BasePage
from mko_bbcode.ui.wizard.style import required_label, hint_label, section_group

class ImagesPage(BasePage):
    """
    Page 5 of the wizard: poster and screenshots.

    Poster URL is required. Screenshots accept 4, 6, or 8 URLs
    selected via radio buttons.
    """

    def __init__(self, parent=None):
        """
        Initializes the page with title and subtitle.

        Args:
            parent: Optional parent widget.
        """

        super().__init__(
            title="Imagens",
            subtitle="Insira as URLs do poster e dos screenshots.",
            parent=parent,
        )

    def showEvent(self, event):
        """
        Applies initial visibility when the page is first shown.
        """

        super().showEvent(event)
        self._update_visible(self._shown)

    def _build_content(self, c: QWidget):
        """
        Builds the page layout with poster input and a dynamic
        screenshot form controlled by radio buttons.

        Args:
            c (QWidget): Container widget provided by the base class.
        """

        lay = QVBoxLayout(c)
        lay.setContentsMargins(32, 24, 32, 24)
        lay.setSpacing(20)

        grp_poster = section_group("Poster")
        form_poster = QFormLayout(grp_poster)
        form_poster.setSpacing(10)
        form_poster.setContentsMargins(12, 16, 12, 12)

        self.cover_input = QLineEdit()
        self.cover_input.setPlaceholderText("https://…/poster.png")
        self.cover_input.setMinimumHeight(32)
        self.cover_input.textChanged.connect(self.completeChanged)
        form_poster.addRow(required_label("URL do Poster"), self.cover_input)

        lay.addWidget(grp_poster)

        grp_ss = section_group("Screenshots")
        lay_ss = QVBoxLayout(grp_ss)
        lay_ss.setSpacing(12)
        lay_ss.setContentsMargins(12, 16, 12, 12)

        count_row = QHBoxLayout()
        count_row.addWidget(QLabel("Quantidade:"))
        count_row.setSpacing(16)

        self._ss_group = QButtonGroup()
        for n in (4, 6, 8):
            rb = QRadioButton(str(n))
            if n == 4:
                rb.setChecked(True)
            self._ss_group.addButton(rb, n)
            count_row.addWidget(rb)
        count_row.addStretch()
        lay_ss.addLayout(count_row)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        lay_ss.addWidget(line)

        self._ss_form = QVBoxLayout()
        self._ss_form.setSpacing(8)
        self._ss_inputs: list[QLineEdit] = []
        self._ss_rows: list[QWidget] = []

        for i in range(8):
            row_widget = QWidget()
            row_lay = QHBoxLayout(row_widget)
            row_lay.setContentsMargins(0, 0, 0, 0)
            row_lay.setSpacing(8)
            row_lay.addWidget(QLabel(f"Screenshot {i+1}:"))
            inp = QLineEdit()
            inp.setPlaceholderText(f"https://…/screenshot_{i+1}.jpg")
            inp.setMinimumHeight(30)
            row_lay.addWidget(inp)
            self._ss_inputs.append(inp)
            self._ss_rows.append(row_widget)
            self._ss_form.addWidget(row_widget)

        lay_ss.addLayout(self._ss_form)
        lay.addWidget(grp_ss)
        lay.addWidget(hint_label("Preencha as URLs das imagens hospedadas (Imgur, imgbb, etc.)."))
        lay.addStretch()

        self._shown = 4
        self._update_visible(4)
        self._ss_group.idClicked.connect(self._update_visible)

    def _update_visible(self, count: int):
        """
        Shows or hides screenshot input rows based on the selected count.

        Args:
            count (int): Number of screenshot inputs to display (4, 6, or 8).
        """

        self._shown = count
        for i, row in enumerate(self._ss_rows):
            row.setVisible(i < count)

    def isComplete(self) -> bool:
        """
        Returns True if the poster URL field is filled.

        Returns:
            bool: True when cover_input has a non-empty value.
        """

        return bool(self.cover_input.text().strip())

    def validatePage(self) -> bool:
        """
        Validates the poster field and saves poster and screenshots
        to wizard.data.

        Returns:
            bool: True if validation passes and data is saved.
        """

        ok = self._validate_fields([self.cover_input])
        if ok:
            d = self.wdata()
            d["poster"] = self.cover_input.text().strip()
            d["screenshots"] = [
                self._ss_inputs[i].text().strip()
                for i in range(self._shown)
                if self._ss_inputs[i].text().strip()
            ]
        return ok