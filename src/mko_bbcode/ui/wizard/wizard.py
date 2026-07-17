from mko_bbcode.ui.wizard.pages import (
    FilePage, InfoPage, DetailsPage,
    TechnicalPage, ImagesPage, ExtrasPage, PreviewPage,
)
from PySide6.QtWidgets import QWizard, QLabel, QHBoxLayout, QWidget
from mko_bbcode.ui.wizard.style import WIZARD_QSS
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class MKOWizard(QWizard):

    PAGE_FILE      = 10
    PAGE_INFO      = 20
    PAGE_DETAILS   = 30
    PAGE_TECHNICAL = 40
    PAGE_IMAGES    = 50
    PAGE_EXTRAS    = 60
    PAGE_PREVIEW   = 70

    def __init__(self, parent=None):
        super().__init__(parent)

        self.data: dict = {}

        self.setWindowTitle("MKO: Gerador de BBCode")
        self.setFixedSize(820, 620)
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)

        self.setOption(QWizard.WizardOption.NoBackButtonOnStartPage, True)
        self.setOption(QWizard.WizardOption.HaveHelpButton, False)
        self.setOption(QWizard.WizardOption.NoCancelButtonOnLastPage, True)

        self.setStyleSheet(WIZARD_QSS)

        self._setup_pages()
        self._setup_button_layout()
    
    def _setup_pages(self):
        self.setPage(self.PAGE_FILE, FilePage(self))
        self.setPage(self.PAGE_INFO, InfoPage(self))
        self.setPage(self.PAGE_DETAILS, DetailsPage(self))
        self.setPage(self.PAGE_TECHNICAL, TechnicalPage(self))
        self.setPage(self.PAGE_IMAGES, ImagesPage(self))
        self.setPage(self.PAGE_EXTRAS, ExtrasPage(self))
        self.setPage(self.PAGE_PREVIEW, PreviewPage(self))
        self.setStartId(self.PAGE_FILE)

    def _setup_button_layout(self):
        self.setButtonLayout([
            QWizard.WizardButton.Stretch,
            QWizard.WizardButton.BackButton,
            QWizard.WizardButton.NextButton,
            QWizard.WizardButton.FinishButton,
            QWizard.WizardButton.CancelButton,
        ])

        self.setButtonText(QWizard.WizardButton.BackButton, "Voltar")
        self.setButtonText(QWizard.WizardButton.NextButton, "Seguir")
        self.setButtonText(QWizard.WizardButton.CancelButton, "Cancelar")
        self.setButtonText(QWizard.WizardButton.FinishButton, "Finalizar")