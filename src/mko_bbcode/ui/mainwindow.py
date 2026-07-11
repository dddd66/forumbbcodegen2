from pathlib import Path, PurePath

import PySide6.QtGui
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)

from mko_bbcode.helpers import build_movie_form_data

from ..bbcode import generate_bb_code
from mko_bbcode.utils import MediaInfo, MediaMetadata
from ..models import LeftFormInput, MovieFormData, RightFormInput
from .leftsideui import CreateLeftWidget
from .rightsideui import CreateRightWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gerador de Códigos")
        window_size: tuple[int, int] = (900, 900)
        self.resize(*window_size)
        self.clipboard = QApplication.clipboard()

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        left_layout = QVBoxLayout()
        self.left_side = CreateLeftWidget()
        left_layout.addWidget(self.left_side)
        self.left_side.bottom_left.pick_file_button.clicked.connect(self._on_file_picker_clicked)
        self.left_side.buttons.clear_fields_button.clicked.connect(self._on_clear_button_clicked)
        self.left_side.buttons.generate_code_button.clicked.connect(self._on_generate_clicked)

        right_layout = QVBoxLayout()
        self.right_side = CreateRightWidget()
        right_layout.addWidget(self.right_side)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

    def _on_generate_clicked(self):
        error_msg: str = "Preencha todos os campos em vermelho."
        error_dialog = QMessageBox(icon=QMessageBox.Icon.Warning)
        success_dialog = QMessageBox(icon=QMessageBox.Icon.Information)
        success_msg: str = "Copiado para a área de transferência."

        left: LeftFormInput = self.left_side.get_data()
        right: RightFormInput = self.right_side.get_data()

        # TODO: separate input validation into its own function
        required_fields: list[QLineEdit | QPlainTextEdit | QComboBox] = [
            self.left_side.name_br_input,
            self.left_side.original_title_input,
            self.left_side.synopsis_input,
            self.left_side.imdb_input,
            self.left_side.vsplit_below.country_of_origin_input,
            self.left_side.vsplit_below.genre_input,
            self.left_side.vsplit_below.audio_language_input,
            self.left_side.vsplit_below.director_input,
            self.left_side.vsplit_below.duration_input,
            self.left_side.vsplit_below.year_input,
            self.left_side.bottom_left.vcodec_input,
            self.left_side.bottom_left.vbitrate_input,
            self.left_side.bottom_left.acodec_input,
            self.left_side.bottom_left.abitrate_input,
            self.left_side.bottom_left.resolution_input,
            self.left_side.bottom_left.aspect_ratio_input,
            self.left_side.bottom_left.size_input,
            self.left_side.bottom_left.container_picker,
            self.left_side.bottom_left.release_input,
            self.left_side.bottom_left.quality_picker,
            self.left_side.bottom_left.subtitles_picker,
            self.left_side.bottom_left.release_selected,
            self.right_side.cover_input,
        ]

        if len(right.screenshots.split(",")) < self.right_side.screenshot_shown:
            error_dialog.warning(self, "Erro", error_msg)
            return
        for field in required_fields:
            match field:
                case QLineEdit():
                    if field.text().strip("\n") == "":
                        error_dialog.warning(self, "Error", error_msg)
                        return
                case QPlainTextEdit():
                    if field.toPlainText().strip("\n") == "":
                        error_dialog.warning(self, "Error", error_msg)
                        return
                case QComboBox():
                    if field.currentIndex() == -1:
                        print(f"field: {field}, idx: {field.currentIndex}")
                        error_dialog.warning(self, "Error", error_msg)
                        return
        movie_data: MovieFormData = build_movie_form_data(left, right)
        movie_metadata: MediaMetadata = self.left_side.get_metadata()

        # copy to clipboard
        bbcode: str = generate_bb_code(movie_data, movie_metadata)
        self.clipboard.setText(bbcode, PySide6.QtGui.QClipboard.Mode.Clipboard)
        success_dialog.information(self, "Sucesso", success_msg)

    def _on_clear_button_clicked(self):
        fields: list[QLineEdit | QPlainTextEdit | QComboBox] = [
            self.left_side.name_br_input,
            self.left_side.original_title_input,
            self.left_side.synopsis_input,
            self.left_side.cast_input,
            self.left_side.imdb_input,
            self.left_side.vsplit_below.country_of_origin_input,
            self.left_side.vsplit_below.genre_input,
            self.left_side.vsplit_below.audio_language_input,
            self.left_side.vsplit_below.director_input,
            self.left_side.vsplit_below.duration_input,
            self.left_side.vsplit_below.year_input,
            self.left_side.bottom_left.vcodec_input,
            self.left_side.bottom_left.vbitrate_input,
            self.left_side.bottom_left.acodec_input,
            self.left_side.bottom_left.abitrate_input,
            self.left_side.bottom_left.resolution_input,
            self.left_side.bottom_left.aspect_ratio_input,
            self.left_side.bottom_left.aspect_ratio_input,
            self.left_side.bottom_left.frame_rate_input,
            self.left_side.bottom_left.quality_picker,
            self.left_side.bottom_left.subtitles_picker,
            self.left_side.bottom_left.size_input,
            self.left_side.bottom_left.container_picker,
            self.left_side.bottom_left.release_input,
            self.left_side.bottom_left.release_selected,
            self.right_side.cover_input,
            self.right_side.bottom_right.awards_input,
            self.right_side.bottom_right.trivia_input,
            self.right_side.bottom_right.review_input,
        ]
        for field in fields:
            match field:
                case QLineEdit():
                    field.setText("")
                case QPlainTextEdit():
                    field.setPlainText("")
                case QComboBox():
                    field.setCurrentIndex(-1)
        for screen in self.right_side.screenshot_input_list:
            screen.setText("")

    def _on_file_picker_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Selecionar arquivo", "", "Videos (*.mkv *.avi)"
        )

        if file_path:
            release_p: Path = Path(file_path)
            metadata: MediaMetadata | None = MediaInfo.from_path(release_p)
            if not metadata:
                return
            self.left_side.bottom_left.vcodec_input.setText(metadata.video_codec)
            self.left_side.bottom_left.vbitrate_input.setText(metadata.video_bitrate)
            self.left_side.bottom_left.acodec_input.setText(metadata.audio_codec)
            self.left_side.bottom_left.abitrate_input.setText(metadata.audio_bitrate)
            if metadata.container == "mkv":
                self.left_side.bottom_left.container_picker.setCurrentIndex(0)
            else:
                self.left_side.bottom_left.container_picker.setCurrentIndex(1)
            self.left_side.bottom_left.resolution_input.setText(metadata.resolution)
            self.left_side.bottom_left.aspect_ratio_input.setText(metadata.aspect_ratio)
            self.left_side.bottom_left.frame_rate_input.setText(metadata.frame_rate)
            self.left_side.bottom_left.size_input.setText(metadata.size)
            self.left_side.bottom_left.release_input.setText(metadata.release)
            self.left_side.bottom_left.release_selected.setText(str(PurePath(file_path)))
