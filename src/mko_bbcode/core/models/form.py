from dataclasses import dataclass

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