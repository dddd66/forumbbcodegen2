from PySide6.QtWidgets import (
    QVBoxLayout, QFormLayout,
    QComboBox, QLineEdit, QWidget
)
from mko_bbcode.ui.wizard.style import required_label, hint_label, section_group
from mko_bbcode.ui.wizard.pages._base import BasePage

_QUALIDADES = [
    "Blu-Ray", "BDRemux", "BDRip",
    "DVD Full", "DVDRip", "HDTVRip", "TVRip",
    "VHSRip", "WEB-DL", "WEBRip", "Outro",
]
_LEGENDAS   = ["Anexas", "Fixas", "Sem legenda", "Embutidas"]

class TechnicalPage(BasePage):
    """
    Page 4 of the wizard: release technical data.

    Collects source and subtitles from the user.
    Remaining fields (codec, bitrate, resolution, etc.) are read
    from the raw MediaInfo dict stored in wizard.data["metadata"].
    """

    def __init__(self, parent=None):
        """
        Initializes the page with title and subtitle.

        Args:
            parent: Optional parent widget.
        """

        super().__init__(
            title="Dados técnicos",
            subtitle="Fonte do release e legendas.",
            parent=parent,
        )

    def _build_content(self, c: QWidget):
        """
        Builds the page layout with release pickers and a read-only
        MediaInfo panel populated when the page is entered.

        Args:
            c (QWidget): Container widget provided by the base class.
        """
        
        lay = QVBoxLayout(c)
        lay.setContentsMargins(32, 24, 32, 24)
        lay.setSpacing(20)

        grp_rel = section_group("Release")
        form_rel = QFormLayout(grp_rel)
        form_rel.setSpacing(10)
        form_rel.setContentsMargins(12, 16, 12, 12)

        self.quality_picker = QComboBox()
        self.quality_picker.addItems(_QUALIDADES)
        self.quality_picker.setCurrentIndex(-1)
        self.quality_picker.setPlaceholderText("Selecione a fonte…")
        self.quality_picker.currentIndexChanged.connect(self.completeChanged)
        form_rel.addRow(required_label("Fonte"), self.quality_picker)

        self.subtitles_picker = QComboBox()
        self.subtitles_picker.addItems(_LEGENDAS)
        self.subtitles_picker.setCurrentIndex(-1)
        self.subtitles_picker.setPlaceholderText("Selecione…")
        self.subtitles_picker.currentIndexChanged.connect(self.completeChanged)
        form_rel.addRow(required_label("Legendas"), self.subtitles_picker)

        lay.addWidget(grp_rel)

        lay.addStretch()

    def isComplete(self) -> bool:
        """
        Returns True if all three required pickers have a selection.

        Returns:
            bool: True when quality, subtitles, and container are set.
        """

        return (
            self.quality_picker.currentIndex() >= 0
            and self.subtitles_picker.currentIndex() >= 0
        )

    def validatePage(self) -> bool:
        """
        Validates required pickers and saves values to wizard.data.

        Returns:
            bool: True if validation passes and data is saved.
        """

        ok = self._validate_fields([
            self.quality_picker,
            self.subtitles_picker,
        ])
        if ok:
            d = self.wdata()
            d["quality"]   = self.quality_picker.currentText()
            d["subtitles"] = self.subtitles_picker.currentText()
        return ok