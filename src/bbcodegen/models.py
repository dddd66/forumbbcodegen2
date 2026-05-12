from dataclasses import dataclass


@dataclass
class MovieMetadata:
    container: str
    resolution: str
    aspect_ratio: str
    video_bitrate: str
    video_codec: str
    frame_rate: str
    size: str
    release: str
    audio_codec: str = "-"
    audio_bitrate: str = "-"


@dataclass
class MovieFormData:
    quality: str
    title_br: str
    title: str
    synopsis: str
    cast: str
    country: str
    director: str
    genre: str
    year: str
    duration: str
    subtitles: str
    poster: str
    screenshots: str
    awards: str
    trivia: str
    review: str
    imdb_url: str = "-"
    audio_language: str = "-"


@dataclass
class LeftFormInput:
    quality: str
    title_br: str
    title: str
    synopsis: str
    cast: str
    country: str
    director: str
    genre: str
    year: str
    duration: str
    subtitles: str
    imdb_url: str = "-"
    audio_language: str = "-"


@dataclass
class RightFormInput:
    poster: str
    screenshots: str
    awards: str
    trivia: str
    review: str


@dataclass
class FullFilmData:
    form_data: MovieFormData
    form_metadata: MovieMetadata
