from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QGroupBox, QFileDialog, QWidget
)
from mko_bbcode.ui.wizard.pages._base import BasePage
from mko_bbcode.ui.wizard.style import hint_label
from mko_bbcode.utils.minfo import MediaInfo
from PySide6.QtGui import QPalette
from PySide6.QtCore import Qt
from pathlib import Path
import os


class FilePage(BasePage):
    """
    Page 1 of the wizard: video file selection.

    Runs MediaInfo on the selected file and stores the raw metadata
    dict in wizard.data["metadata"] for use in subsequent pages
    and BBCode generation.
    """

    def __init__(self, parent=None):
        """
        Initializes the page with title and subtitle.

        Args:
            parent: Optional parent widget.
        """

        super().__init__(
            title="Selecionar arquivo",
            subtitle="Escolha o arquivo de vídeo do release. Containers aceitos: MKV e AVI.",
            parent=parent,
        )

    def _build_content(self, c: QWidget):
        """
        Builds the page layout with a file selector and a
        read-only metadata panel shown after a file is loaded.

        Args:
            c (QWidget): Container widget provided by the base class.
        """

        lay = QVBoxLayout(c)
        lay.setContentsMargins(32, 24, 32, 24)
        lay.setSpacing(20)

        grp = QGroupBox("Arquivo de vídeo")
        grp_lay = QVBoxLayout(grp)
        grp_lay.setSpacing(10)

        row = QHBoxLayout()
        self.input_path = QLineEdit()
        self.input_path.setPlaceholderText("Nenhum arquivo selecionado…")
        self.input_path.setReadOnly(True)
        self.input_path.setMinimumHeight(34)
        self.input_path.textChanged.connect(self.completeChanged)

        self.btn_browse = QPushButton("📂  Procurar…")
        self.btn_browse.setMinimumHeight(34)
        self.btn_browse.setFixedWidth(130)
        self.btn_browse.clicked.connect(self._browse)

        row.addWidget(self.input_path)
        row.addWidget(self.btn_browse)
        grp_lay.addLayout(row)

        self.lbl_file_info = QLabel()
        self.lbl_file_info.setStyleSheet("font-size: 11px;")
        self.lbl_file_info.setForegroundRole(QPalette.ColorRole.PlaceholderText)
        grp_lay.addWidget(self.lbl_file_info)

        lay.addWidget(grp)

        def _ro(placeholder="—"):
            w = QLineEdit(placeholder)
            w.setReadOnly(True)
            return w

        self.meta_resolution  = _ro()
        self.meta_vcodec      = _ro()
        self.meta_vbitrate    = _ro()
        self.meta_acodec      = _ro()
        self.meta_abitrate    = _ro()
        self.meta_container   = _ro()
        self.meta_fps         = _ro()
        self.meta_aspect      = _ro()
        self.meta_size        = _ro()
        self.meta_release     = _ro()

        lay.addWidget(hint_label(
            "Os dados técnicos (MediaInfo) são detectados automaticamente e "
            "serão incluídos no BBCode. Você não precisa preenchê-los."
        ))
        lay.addStretch()

        self.registerField("arquivo_path*", self.input_path)

    def _browse(self):
        """
        Opens a file dialog and triggers metadata loading
        when the user confirms a file selection.
        """

        path, _ = QFileDialog.getOpenFileName(
            self, "Selecionar arquivo de vídeo",
            os.path.expanduser("~"),
            "Vídeo (*.mkv *.avi);;MKV (*.mkv);;AVI (*.avi)",
        )
        if not path:
            return

        self.input_path.setText(path)
        size_mb = os.path.getsize(path) / (1024 * 1024)
        nome = os.path.basename(path)
        ext  = os.path.splitext(nome)[1].upper().lstrip(".")
        self.lbl_file_info.setText(f"📄  {nome}   ·   {ext}   ·   {size_mb:.1f} MB")

        self._load_metadata(path)

    def _load_metadata(self, path: str):
        """
        Runs MediaInfo on the given path and populates wizard.data
        with the raw metadata dict. Hides the panel if parsing fails.

        Args:
            path (str): Absolute path to the video file.
        """

        try:
            meta: dict | None = MediaInfo.from_path(Path(path))
        except Exception:
            meta = None

        d = self.wdata()
        d["metadata"] = meta
        d["arquivo_path"] = path

        if meta and meta.get("duration_ms"):
            d["duration"] = str(round(float(meta["duration_ms"]) / 60_000))

        if meta:
            self.meta_resolution.setText(str(meta.get("video_width", "")) + " x " + str(meta.get("video_height", "")) or "—")
            self.meta_vcodec.setText(meta.get("video_format")    or "—")
            self.meta_vbitrate.setText(str(meta.get("video_bit_rate") or "—"))
            self.meta_acodec.setText(meta.get("audio_format")    or "—")
            self.meta_abitrate.setText(str(meta.get("audio_bit_rate") or "—"))
            self.meta_container.setText(meta.get("container")    or "—")
            self.meta_fps.setText(meta.get("video_frame_rate")   or "—")
            dar = meta.get("video_dar")
            self.meta_aspect.setText((dar[0] if isinstance(dar, list) else dar) or "—")
            self.meta_size.setText(str(meta.get("file_size", "—")))
            self.meta_release.setText(meta.get("release")        or "—")

    def isComplete(self) -> bool:
        """
        Returns True if a valid MKV or AVI file has been selected.

        Returns:
            bool: True when the path field is not empty and the
                  file extension is .mkv or .avi.
        """
        
        p = self.input_path.text()
        return bool(p) and p.lower().endswith((".mkv", ".avi"))

    def initializePage(self):
        """
        Focuses the path field when the page is entered.
        """

        self.input_path.setFocus()
