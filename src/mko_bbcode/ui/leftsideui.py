import re

from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QWidget,
)

from bbcodegen.imdb_api import FetchIMDB

from ..helpers import RedTextLabel
from ..models import LeftFormInput, MovieMetadata


class CreateLeftWidget(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QFormLayout(self)
        self._busy = False

        self.name_br_label = RedTextLabel("Nome no Brasil:")
        self.name_br_input = QLineEdit()
        main_layout.addRow(self.name_br_label, self.name_br_input)

        self.original_title_label = RedTextLabel("Nome Original:")
        self.original_title_input = QLineEdit()
        main_layout.addRow(self.original_title_label, self.original_title_input)

        self.synopsis_label = RedTextLabel("Sinopse:")
        self.synopsis_input = QPlainTextEdit()
        # self.synopsis_input.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
        main_layout.addRow(self.synopsis_label, self.synopsis_input)

        self.cast_label = QLabel("Elenco:")
        self.cast_input = QPlainTextEdit()
        # self.cast_input.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
        main_layout.addRow(self.cast_label, self.cast_input)

        self.imdb_container = QWidget()
        self.imdb_layout = QHBoxLayout(self.imdb_container)
        self.imdb_label = RedTextLabel("IMDB:")
        self.imdb_input = QLineEdit()
        self.imdb_fetch_info_button = QPushButton("Obter dados")
        self.imdb_layout.setContentsMargins(0, 0, 0, 0)
        self.imdb_layout.addWidget(self.imdb_input)
        self.imdb_layout.addWidget(self.imdb_fetch_info_button)
        main_layout.addRow(self.imdb_label, self.imdb_container)

        self.vsplit_below: CreateVsplitPanelBelowUpperLeft = CreateVsplitPanelBelowUpperLeft()
        self.vsplit_below.setContentsMargins(0, 0, 0, 0)
        main_layout.addRow(self.vsplit_below)

        self.imdb_fetch_info_button.clicked.connect(self.fetch_imdb_data)
        self.bottom_left = CreateBottomLeft()
        main_layout.addRow(self.bottom_left)

        self.buttons = CreateBottomButtons()
        main_layout.addRow(self.buttons)

        self.setLayout(main_layout)

    def _on_imdb_error_arrival(self, data):
        self.imdb_fetch_info_button.setEnabled(True)
        self._busy = False

    def _on_data_arrival(self, data):
        self.imdb_fetch_info_button.setEnabled(True)
        self._busy = False
        if not data:
            return
        title: str = str(data.get("originalTitle", ""))
        if not title:
            title = str(data.get("primaryTitle", ""))
        self.original_title_input.setText(title)

        directors: list[str] = []
        if data.get("directors"):
            for director in data["directors"]:
                directors.append(director.get("displayName", ""))
        directors_f: str = ", ".join(directors)
        self.vsplit_below.director_input.setText(directors_f)

        cast_stars: list[str] = []
        if data.get("stars"):
            for star in data["stars"]:
                cast_stars.append(star.get("displayName", ""))
        cast_stars_f: str = ", ".join(cast_stars)

        year: str = str(data.get("startYear", ""))
        self.vsplit_below.year_input.setText(year)

        self.cast_input.setPlainText(cast_stars_f)

    def fetch_imdb_data(self) -> None:
        if self._busy:
            return
        imdb_id = self.imdb_input.text()
        imdb_id = re.findall(r"tt[0-9]{7}", imdb_id)
        imdb_id = "".join(imdb_id)
        if not imdb_id:
            return
        self._busy = True

        self.fetcher = FetchIMDB(imdb_id=imdb_id)
        self.imdb_fetch_info_button.setEnabled(False)
        self.fetcher.arrived_data.connect(self._on_data_arrival)
        self.fetcher.error_occurred.connect(self._on_imdb_error_arrival)

    def get_data(self) -> LeftFormInput:
        lfi: dict[str, str] = {
            "title_br": self.name_br_input.text(),
            "title": self.original_title_input.text(),
            "synopsis": self.synopsis_input.toPlainText(),
            "cast": self.cast_input.toPlainText(),
            "imdb_url": self.imdb_input.text(),
            "genre": self.vsplit_below.genre_input.text(),
            "director": self.vsplit_below.director_input.text(),
            "country": self.vsplit_below.country_of_origin_input.text(),
            "audio_language": self.vsplit_below.audio_language_input.text(),
            "year": str(self.vsplit_below.year_input.text()),
            "duration": self.vsplit_below.duration_input.text(),
            "subtitles": self.bottom_left.subtitles_picker.currentText(),
            "quality": self.bottom_left.quality_picker.currentText(),
        }
        return LeftFormInput(**lfi)

    def get_metadata(self) -> MovieMetadata:
        # TODO: needs to be refactored
        return MovieMetadata(
            video_codec=self.bottom_left.vcodec_input.text(),
            video_bitrate=self.bottom_left.vbitrate_input.text(),
            audio_codec=self.bottom_left.acodec_input.text(),
            audio_bitrate=self.bottom_left.abitrate_input.text(),
            frame_rate=self.bottom_left.frame_rate_input.text(),
            size=self.bottom_left.size_input.text(),
            release=self.bottom_left.release_input.text(),
            resolution=self.bottom_left.resolution_input.text(),
            container=self.bottom_left.container_picker.currentText(),
            aspect_ratio=self.bottom_left.aspect_ratio_input.text(),
        )


class CreateBottomButtons(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QHBoxLayout(self)

        self.generate_code_button = QPushButton("Gerar Código")
        self.clear_fields_button = QPushButton("Limpar Campos")

        main_layout.addWidget(self.generate_code_button)
        main_layout.addWidget(self.clear_fields_button)


class CreateVsplitPanelBelowUpperLeft(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 11, 0, 11)
        left_side_panel = QWidget()
        left_side_layout = QFormLayout(left_side_panel)
        left_side_layout.setContentsMargins(0, 11, 11, 0)

        self.country_of_origin_label = RedTextLabel("País de Origem:")
        self.country_of_origin_input = QLineEdit()
        left_side_layout.addRow(self.country_of_origin_label, self.country_of_origin_input)

        self.genre_label = RedTextLabel("Gênero:")
        self.genre_input = QLineEdit()
        left_side_layout.addRow(self.genre_label, self.genre_input)

        self.audio_language_label = RedTextLabel("Idioma do Áudio:")
        self.audio_language_input = QLineEdit()
        left_side_layout.addRow(self.audio_language_label, self.audio_language_input)

        right_side_panel = QWidget()
        right_side_layout = QFormLayout(right_side_panel)
        self.director_label = RedTextLabel("Diretor:")
        self.director_input = QLineEdit()
        right_side_layout.addRow(self.director_label, self.director_input)

        self.duration_label = RedTextLabel("Duração:")
        duration_container = QWidget()
        duration_layout = QHBoxLayout(duration_container)
        duration_layout.setContentsMargins(0, 0, 0, 0)
        self.duration_input = QLineEdit()
        duration_layout.addWidget(self.duration_input)
        duration_layout.addWidget(QLabel("minutos"))
        right_side_layout.addRow(self.duration_label, duration_container)

        self.year_label = RedTextLabel("Ano:")
        self.year_input = QLineEdit()
        right_side_layout.addRow(self.year_label, self.year_input)

        main_layout.addWidget(left_side_panel)
        main_layout.addWidget(right_side_panel)
        main_layout.setContentsMargins(0, 0, 0, 0)

    def on_imdb_data_arrival_vsplit(self, data):
        directors: list[str] = []
        if data.get("directors"):
            for director in data["directors"]:
                directors.append(director.get("displayName", ""))
        directors_f: str = ", ".join(directors)
        self.director_input.setText(directors_f)
        year: str = str(data.get("startYear", ""))
        self.year_input.setText(year)


class CreateBottomLeft(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QFormLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.pick_file_button = QPushButton("Escolher arquivo")
        self.release_selected = QLineEdit()
        self.release_selected.setReadOnly(True)
        main_layout.addRow(self.pick_file_button, self.release_selected)

        self.quality_label = RedTextLabel("Qualidade:")
        self.quality_picker = QComboBox()
        qualidades: list[str] = [
            "Blu-Ray Full",
            "BDRemux",
            "BDRip",
            "DVD Full",
            "DVDRip",
            "HDTVRip",
            "TVRip",
            "VHSRip",
            "WEB-DL",
            "WEBRip",
            "Outro",
        ]
        self.quality_picker.addItems(qualidades)
        self.quality_picker.setCurrentIndex(-1)
        main_layout.addRow(self.quality_label, self.quality_picker)

        self.vcodec_label = RedTextLabel("Video Codec")
        self.vcodec_input = QLineEdit()
        main_layout.addRow(self.vcodec_label, self.vcodec_input)

        self.vbitrate_label = RedTextLabel("Video Bitrate")
        self.vbitrate_input = QLineEdit()
        main_layout.addRow(self.vbitrate_label, self.vbitrate_input)

        self.acodec_label = RedTextLabel("Áudio Codec")
        self.acodec_input = QLineEdit()
        main_layout.addRow(self.acodec_label, self.acodec_input)

        self.abitrate_label = RedTextLabel("Áudio Bitrate")
        self.abitrate_input = QLineEdit()
        main_layout.addRow(self.abitrate_label, self.abitrate_input)

        self.container_label = RedTextLabel("Container:")
        self.container_picker = QComboBox()
        container_options: list[str] = ["mkv", "avi"]
        self.container_picker.addItems(container_options)
        self.container_picker.setCurrentIndex(-1)
        main_layout.addRow(self.container_label, self.container_picker)

        self.resolution_label = RedTextLabel("Resolução:")
        self.resolution_input = QLineEdit()
        main_layout.addRow(self.resolution_label, self.resolution_input)

        self.aspect_ratio_label = RedTextLabel("Formato da Tela:")
        self.aspect_ratio_input = QLineEdit()
        main_layout.addRow(self.aspect_ratio_label, self.aspect_ratio_input)

        self.frame_rate_label = RedTextLabel("Frame rate:")
        self.frame_rate_input = QLineEdit()
        main_layout.addRow(self.frame_rate_label, self.frame_rate_input)

        self.size_label = RedTextLabel("Tamanho:")
        self.size_input = QLineEdit()
        main_layout.addRow(self.size_label, self.size_input)

        self.subtitles_label = RedTextLabel("Legendas:")
        self.subtitles_picker = QComboBox()
        subtitles_options: list[str] = ["Anexas", "Fixas", "Sem legenda", "No torrent"]
        self.subtitles_picker.addItems(subtitles_options)
        self.subtitles_picker.setCurrentIndex(-1)
        main_layout.addRow(self.subtitles_label, self.subtitles_picker)

        self.release_label = RedTextLabel("Release:")
        self.release_input = QLineEdit()
        main_layout.addRow(self.release_label, self.release_input)
