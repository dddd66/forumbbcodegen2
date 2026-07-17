from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel,
    QWidget, QApplication, QFrame
)
from PySide6.QtGui import QFont, QColor, QTextCharFormat, QSyntaxHighlighter
from PySide6.QtCore import Qt, QRegularExpression
from mko_bbcode.ui.wizard.pages._base import BasePage
from mko_bbcode.core.bbcode import BBCode
from mko_bbcode.core.models import MovieFormData

class BBCodeHighlighter(QSyntaxHighlighter):
    """
    Syntax highlighter for BBCode tags and URLs in the preview editor.
    """

    def __init__(self, document):
        """
        Initializes highlight rules for tags and URLs.

        Args:
            document: QTextDocument to attach the highlighter to.
        """

        super().__init__(document)

        tag_fmt = QTextCharFormat()
        tag_fmt.setForeground(QColor("#4A90D9"))
        tag_fmt.setFontWeight(700)

        url_fmt = QTextCharFormat()
        url_fmt.setForeground(QColor("#A6E3A1"))

        self._rules = [
            (QRegularExpression(r"\[/?[^\]]+\]"), tag_fmt),
            (QRegularExpression(r"https?://\S+"),  url_fmt),
        ]

    def highlightBlock(self, text: str):
        """
        Applies highlight rules to a single block of text.

        Args:
            text (str): The text block to highlight.
        """

        for pattern, fmt in self._rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                m = it.next()
                self.setFormat(m.capturedStart(), m.capturedLength(), fmt)


def _build_bbcode(d: dict) -> str:
    """
    Assembles the BBCode string from wizard.data using BBCode.new().

    Args:
        d (dict): The shared wizard data dict.

    Returns:
        str: The generated BBCode string.
    """
    
    screenshots = d.get("screenshots", [])

    form = MovieFormData(
        title_br = d.get("title_br") or d.get("title", ""),
        title          = d.get("title", ""),
        imdb_url       = d.get("imdb_url", ""),
        year           = d.get("year", ""),
        country        = d.get("country", ""),
        genre          = d.get("genre", ""),
        synopsis       = d.get("synopsis", ""),
        director       = d.get("director", ""),
        cast           = d.get("cast", ""),
        audio_language = d.get("audio_language", ""),
        duration       = d.get("duration", ""),
        quality        = d.get("quality", ""),
        subtitles      = d.get("subtitles", ""),
        poster         = d.get("poster", ""),
        screenshots    = ",".join(s for s in screenshots if s),
        awards         = d.get("awards", ""),
        trivia         = d.get("trivia", ""),
        review         = d.get("review", ""),
    )

    meta: dict | None = d.get("metadata")
    if meta is None:
        m_info = {
            "release": "", "container": "", "file_size": 0,
            "duration_ms": None,
            "video_format": "", "video_bit_rate": None,
            "video_width": 0, "video_height": 0,
            "video_par": None, "video_dar": None, "video_frame_rate": None,
            "audio_format": "", "audio_format_raw": None,
            "audio_profile": None, "audio_bit_rate": None,
            "audio_languages": [],
        }
    else:
        m_info = meta

    return BBCode.new(form, m_info)


class PreviewPage(BasePage):
    """
    Page 7 of the wizard: BBCode preview.

    Displays the generated BBCode in a read-only editor with syntax
    highlighting and a one-click copy button.
    """

    def __init__(self, parent=None):
        """
        Initializes the page with title and subtitle.

        Args:
            parent: Optional parent widget.
        """

        super().__init__(
            title="BBCode gerado",
            subtitle="Revise o código abaixo e copie para a área de transferência.",
            parent=parent,
        )

    def _build_content(self, c: QWidget):
        """
        Builds the page layout with a summary label, BBCode editor,
        and copy button.

        Args:
            c (QWidget): Container widget provided by the base class.
        """

        lay = QVBoxLayout(c)
        lay.setContentsMargins(32, 20, 32, 20)
        lay.setSpacing(14)

        self.lbl_summary = QLabel()
        self.lbl_summary.setTextFormat(Qt.TextFormat.RichText)
        self.lbl_summary.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_summary.setStyleSheet(
            "font-size: 13px; padding: 8px;"
            "background: palette(alternateBase); border-radius: 6px;"
        )
        lay.addWidget(self.lbl_summary)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        lay.addWidget(sep)

        self.editor = QTextEdit()
        self.editor.setReadOnly(True)
        self.editor.setAcceptRichText(False)
        f = QFont("Courier New", 10)
        f.setStyleHint(QFont.StyleHint.Monospace)
        self.editor.setFont(f)
        self.editor.setMinimumHeight(340)
        self.editor.setStyleSheet(
            "QTextEdit {"
            "  border: 1px solid palette(mid);"
            "  border-radius: 6px;"
            "  padding: 10px;"
            "}"
        )
        self._highlighter = BBCodeHighlighter(self.editor.document())
        lay.addWidget(self.editor, stretch=1)

        btn_row = QHBoxLayout()
        btn_row.addStretch()

        self.btn_copy = QPushButton("📋  Copiar BBCode")
        self.btn_copy.setMinimumHeight(38)
        self.btn_copy.setMinimumWidth(160)
        self.btn_copy.setStyleSheet(
            "QPushButton {"
            "  background-color: #4A90D9;"
            "  color: white;"
            "  border: none;"
            "  border-radius: 4px;"
            "  font-weight: bold;"
            "  font-size: 13px;"
            "  padding: 6px 20px;"
            "}"
            "QPushButton:hover { background-color: #6AAFE6; }"
            "QPushButton:pressed { background-color: #3070B9; }"
        )
        self.btn_copy.clicked.connect(self._copy)

        self.lbl_copied = QLabel("✅  Copiado!")
        self.lbl_copied.setStyleSheet("color: green; font-size: 12px;")
        self.lbl_copied.setVisible(False)

        btn_row.addWidget(self.lbl_copied)
        btn_row.addWidget(self.btn_copy)
        lay.addLayout(btn_row)

    def initializePage(self):
        """
        Generates the BBCode and populates the editor when the page
        is entered.
        """

        d = self.wdata()

        title_br = d.get("title_br") or d.get("title", "")
        year     = d.get("year", "")
        self.lbl_summary.setText(
            f"<b>{title_br}</b>"
            + (f"  <span style='color: gray'>({year})</span>" if year else "")
        )

        self.lbl_copied.setVisible(False)
        self.editor.setPlainText(_build_bbcode(d))

    def _copy(self):
        """
        Copies the editor content to the system clipboard.
        """

        QApplication.clipboard().setText(self.editor.toPlainText())
        self.lbl_copied.setVisible(True)

    def isComplete(self) -> bool:
        """
        Always returns True, this is the last page.

        Returns:
            bool: Always True.
        """

        return True
