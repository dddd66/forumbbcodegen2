from PySide6.QtWidgets import (
    QVBoxLayout, QFormLayout,
    QPlainTextEdit, QWidget
)
from mko_bbcode.ui.wizard.style import optional_label, hint_label, section_group
from mko_bbcode.ui.wizard.pages._base import BasePage

class ExtrasPage(BasePage):
    """
    Page 6 of the wizard: optional extras.

    Collects awards, trivia, and review text. All fields are optional;
    empty sections are omitted from the generated BBCode.
    """

    def __init__(self, parent=None):
        """
        Initializes the page with title and subtitle.

        Args:
            parent: Optional parent widget.
        """

        super().__init__(
            title="Extras",
            subtitle="Campos opcionais, deixe em branco se não quiser incluir.",
            parent=parent,
        )

    def _build_content(self, c: QWidget):
        """
        Builds the page layout with awards, trivia, and review
        text areas inside a single group.

        Args:
            c (QWidget): Container widget provided by the base class.
        """

        lay = QVBoxLayout(c)
        lay.setContentsMargins(32, 24, 32, 24)
        lay.setSpacing(20)

        grp = section_group("Conteúdo adicional")
        form = QFormLayout(grp)
        form.setSpacing(14)
        form.setContentsMargins(12, 16, 12, 12)

        self.awards_input = QPlainTextEdit()
        self.awards_input.setMinimumHeight(80)
        form.addRow(optional_label("Premiações"), self.awards_input)

        self.trivia_input = QPlainTextEdit()
        self.trivia_input.setMinimumHeight(80)
        form.addRow(optional_label("Curiosidades"), self.trivia_input)

        self.review_input = QPlainTextEdit()
        self.review_input.setMinimumHeight(80)
        form.addRow(optional_label("Crítica"), self.review_input)

        lay.addWidget(grp)
        lay.addWidget(hint_label(
            "Estes campos são completamente opcionais. "
            "Se deixados em branco, as seções correspondentes "
            "não aparecerão no BBCode gerado."
        ))
        lay.addStretch()

    def isComplete(self) -> bool:
        """
        Always returns True, all fields on this page are optional.

        Returns:
            bool: Always True.
        """

        return True

    def validatePage(self) -> bool:
        """
        Saves optional field values to wizard.data.

        Returns:
            bool: Always True.
        """
        
        d = self.wdata()
        d["awards"] = self.awards_input.toPlainText().strip()
        d["trivia"] = self.trivia_input.toPlainText().strip()
        d["review"] = self.review_input.toPlainText().strip()
        return True
