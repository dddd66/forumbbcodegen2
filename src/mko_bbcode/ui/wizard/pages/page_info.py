from PySide6.QtWidgets import (
    QVBoxLayout, QFormLayout, QHBoxLayout,
    QLineEdit, QWidget, QLabel
)
from PySide6.QtCore import Qt
from mko_bbcode.ui.wizard.pages._base import BasePage
from mko_bbcode.ui.wizard.style import required_label, optional_label, hint_label, section_group


class InfoPage(BasePage):
    """
    Page 2 of the wizard: work identification.

    Collects the Brazilian title, original title, IMDB URL,
    release year, country of origin, and genre.
    """

    def __init__(self, parent=None):
        """
        Initializes the page with title and subtitle.

        Args:
            parent: Optional parent widget.
        """

        super().__init__(
            title="Identificação da obra",
            subtitle="Preencha os dados principais do filme ou série.",
            parent=parent,
        )

    def _build_content(self, c: QWidget):
        """
        Builds the page layout with title, reference, and
        classification field groups.

        Args:
            c (QWidget): Container widget provided by the base class.
        """

        lay = QVBoxLayout(c)
        lay.setContentsMargins(32, 24, 32, 24)
        lay.setSpacing(20)

        grp_titles = section_group("Títulos")
        form_titles = QFormLayout(grp_titles)
        form_titles.setSpacing(10)
        form_titles.setContentsMargins(12, 16, 12, 12)

        self.name_br_input = QLineEdit()
        self.name_br_input.setMinimumHeight(32)
        self.name_br_input.textChanged.connect(self.completeChanged)
        form_titles.addRow(optional_label("Nome no Brasil"), self.name_br_input)
        self.name_br_input.setPlaceholderText("Opcional: deixar em branco caso não exista.")

        self.original_title_input = QLineEdit()
        self.original_title_input.setMinimumHeight(32)
        self.original_title_input.textChanged.connect(self.completeChanged)
        form_titles.addRow(required_label("Nome Original"), self.original_title_input)

        lay.addWidget(grp_titles)

        grp_ref = section_group("Referência")
        form_ref = QFormLayout(grp_ref)
        form_ref.setSpacing(10)
        form_ref.setContentsMargins(12, 16, 12, 12)

        self.imdb_input = QLineEdit()
        self.imdb_input.setMinimumHeight(32)
        form_ref.addRow(optional_label("URL do IMDB"), self.imdb_input)
        self.imdb_input.setPlaceholderText("Opcional: deixar em branco caso não exista.")

        lay.addWidget(grp_ref)

        grp_class = section_group("Classificação")
        form_class = QFormLayout(grp_class)
        form_class.setSpacing(10)
        form_class.setContentsMargins(12, 16, 12, 12)

        row_ap = QHBoxLayout()
        row_ap.setSpacing(20)

        col_ano = QVBoxLayout()
        col_ano.addWidget(required_label("Ano"))
        self.year_input = QLineEdit()
        self.year_input.setMaxLength(4)
        self.year_input.setMinimumHeight(32)
        self.year_input.textChanged.connect(self.completeChanged)
        col_ano.addWidget(self.year_input)

        col_pais = QVBoxLayout()
        col_pais.addWidget(required_label("País(es) de Origem"))
        self.country_input = QLineEdit()
        self.country_input.setMinimumHeight(32)
        self.country_input.textChanged.connect(self.completeChanged)
        col_pais.addWidget(self.country_input)

        row_ap.addLayout(col_ano)
        row_ap.addLayout(col_pais)
        form_class.addRow(row_ap)

        self.genre_input = QLineEdit()
        self.genre_input.setMinimumHeight(32)
        self.genre_input.textChanged.connect(self.completeChanged)
        form_class.addRow(required_label("Gênero(s)"), self.genre_input)

        lay.addWidget(grp_class)
        lay.addStretch()

    def isComplete(self) -> bool:
        """
        Returns True if all required fields are filled.

        Returns:
            bool: True when title, original title, year, country
                  and genre are all non-empty.
        """
        
        return all([
            self.original_title_input.text().strip(),
            self.year_input.text().strip(),
            self.country_input.text().strip(),
            self.genre_input.text().strip(),
        ])

    def validatePage(self) -> bool:
        """
        Validates required fields and saves values to wizard.data.

        Returns:
            bool: True if validation passes and data is saved.
        """

        ok = self._validate_fields([
            self.original_title_input,
            self.year_input,
            self.country_input,
            self.genre_input,
        ])
        if ok:
            d = self.wdata()
            d["title"]    = self.original_title_input.text().strip()
            d["imdb_url"] = self.imdb_input.text().strip()
            d["year"]     = self.year_input.text().strip()
            d["country"]  = self.country_input.text().strip()
            d["genre"]    = self.genre_input.text().strip()
            d["title_br"] = self.name_br_input.text().strip()
        return ok
