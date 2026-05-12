from PySide6.QtWidgets import QLabel

from .models import LeftFormInput, MovieFormData, RightFormInput


class RedTextLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("color: red;")


def build_movie_form_data(left: LeftFormInput, right: RightFormInput) -> MovieFormData:
    return MovieFormData(
        quality=left.quality,
        title_br=left.title_br,
        title=left.title,
        synopsis=left.synopsis,
        cast=left.cast,
        imdb_url=left.imdb_url,
        genre=left.genre,
        director=left.director,
        country=left.country,
        audio_language=left.audio_language,
        year=left.year,
        duration=left.duration,
        subtitles=left.subtitles,
        poster=right.poster,
        screenshots=right.screenshots,
        awards=right.awards,
        trivia=right.trivia,
        review=right.review,
    )
