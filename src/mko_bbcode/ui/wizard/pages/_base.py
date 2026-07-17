from PySide6.QtWidgets import (
    QWizardPage, QVBoxLayout, QWidget,
    QLineEdit, QPlainTextEdit, QComboBox
)
from PySide6.QtCore import Qt

class BasePage(QWizardPage):
    """
    Base page class.

    Subclasses must implement _build_content(container: QWidget)
    to populate the page layout.
    """

    def __init__(self, title: str, subtitle: str, parent=None):
        """
        Initializes the page with title and subtitle.

        Args:
            title (str): Page title shown in the wizard header.
            subtitle (str): Page subtitle shown below the title.
            parent: Optional parent widget.
        """

        super().__init__(parent)
        self.setTitle(title)
        self.setSubTitle(subtitle)
        self._build_outer()

    def _build_outer(self):
        """
        Builds the outer layout and attaches the content container.
        """

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        self._container = QWidget()
        self._build_content(self._container)
        outer.addWidget(self._container)

    def _build_content(self, container: QWidget):
        """
        Abstract method — subclasses must implement this to build
        their page content inside the given container widget.

        Args:
            container (QWidget): Parent container for the page layout.
        """

        raise NotImplementedError

    def wdata(self) -> dict:
        """
        Returns the shared data dict from the parent wizard.

        Returns:
            dict: wizard.data if available, otherwise an empty dict.
        """

        wiz = self.wizard()
        if wiz and hasattr(wiz, "data"):
            return wiz.data
        return {}

    def _validate_fields(
        self,
        fields: list[QLineEdit | QPlainTextEdit | QComboBox],
    ) -> bool:
        """
        Validates a list of required fields, highlighting empty ones
        with a red border.

        Args:
            fields: List of input widgets to validate.

        Returns:
            bool: True if all fields are filled, False otherwise.
        """

        ok = True
        for f in fields:
            empty = False
            match f:
                case QLineEdit():
                    empty = not f.text().strip()
                case QPlainTextEdit():
                    empty = not f.toPlainText().strip()
                case QComboBox():
                    empty = f.currentIndex() < 0

            if empty:
                f.setStyleSheet("border: 1px solid #E05252;")
                ok = False
            else:
                f.setStyleSheet("")
        return ok