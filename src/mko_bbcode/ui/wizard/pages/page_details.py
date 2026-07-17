from PySide6.QtWidgets import (
    QVBoxLayout, QFormLayout, QHBoxLayout,
    QLineEdit, QPlainTextEdit, QLabel, QWidget
)
from mko_bbcode.ui.wizard.style import required_label, optional_label, section_group
from mko_bbcode.ui.wizard.pages._base import BasePage

class DetailsPage(BasePage):
    """
    Page 3 of the wizard: work details.

    Collects synopsis, director, cast, audio language.
    """

    def __init__(self, parent=None):
        """
        Initializes the page with title and subtitle.

        Args:
            parent: Optional parent widget.
        """

        super().__init__(
            title="Detalhes da obra",
            subtitle="Sinopse, elenco e informações de produção.",
            parent=parent,
        )

    def _build_content(self, c: QWidget):
        """
        Builds the page layout with synopsis, production, and
        audio field groups.

        Args:
            c (QWidget): Container widget provided by the base class.
        """

        lay = QVBoxLayout(c)
        lay.setContentsMargins(32, 24, 32, 24)
        lay.setSpacing(20)

        grp_syn = section_group("Sinopse")
        form_syn = QFormLayout(grp_syn)
        form_syn.setSpacing(8)
        form_syn.setContentsMargins(12, 16, 12, 12)

        self.synopsis_input = QPlainTextEdit()
        self.synopsis_input.setPlaceholderText("Descreva o enredo do filme…")
        self.synopsis_input.setMinimumHeight(100)
        self.synopsis_input.textChanged.connect(self.completeChanged)
        form_syn.addRow(required_label("Sinopse"), self.synopsis_input)

        lay.addWidget(grp_syn)

        grp_prod = section_group("Produção")
        form_prod = QFormLayout(grp_prod)
        form_prod.setSpacing(10)
        form_prod.setContentsMargins(12, 16, 12, 12)

        self.director_input = QLineEdit()
        self.director_input.setMinimumHeight(32)
        self.director_input.textChanged.connect(self.completeChanged)
        form_prod.addRow(required_label("Direção"), self.director_input)

        self.cast_input = QPlainTextEdit()
        self.cast_input.setMinimumHeight(70)
        form_prod.addRow(optional_label("Elenco"), self.cast_input)

        lay.addWidget(grp_prod)

        lay.addStretch()

    def isComplete(self) -> bool:
        """
        Returns True if all required fields are filled.

        Returns:
            bool: True when synopsis, director and audio language
                  are all non-empty.
        """

        return all([
            self.synopsis_input.toPlainText().strip(),
            self.director_input.text().strip(),
        ])

    def validatePage(self) -> bool:
        """
        Validates required fields and saves values to wizard.data.

        Returns:
            bool: True if validation passes and data is saved.
        """

        ok = self._validate_fields([
            self.synopsis_input,
            self.director_input,
        ])
        if ok:
            d = self.wdata()
            d["synopsis"] = self.synopsis_input.toPlainText().strip()
            d["director"] = self.director_input.text().strip()
            d["cast"] = self.cast_input.toPlainText().strip()
        return ok
