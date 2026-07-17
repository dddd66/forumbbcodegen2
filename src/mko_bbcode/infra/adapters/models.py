from dataclasses import dataclass

@dataclass
class FetchResult:
    """
    Data class for adapters Fetch title query results.
    """

    title_pt: str
    title_original: str
    synopsis: str
    directors: str
    cast: str
    poster: str
    genres: str
    year: str
    countries: str