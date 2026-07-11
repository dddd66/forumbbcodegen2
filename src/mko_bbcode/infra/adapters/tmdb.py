from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PySide6.QtCore import QObject, QUrl, Signal
from mko_bbcode.core.models import FetchResult
from typing import Any
import urllib.parse
import json


class TMDB(QObject):
    """
    Qt adapter for the TMDB API methods.
    """

    IMAGE_URL: str = "https://image.tmdb.org/t/p/original"
    BASE_URL: str = "https://api.themoviedb.org/3"

    arrived_data: Signal = Signal(FetchResult)
    error_occurred: Signal = Signal(str)

    def __init__(self, token: str, parent: QObject | None = None):
        """
        Initialize a TMDB adapter object.

        Args:
            token (str):
                A TMDB API bearer token.

            parent (QObject | None):
                Optional Qt parent object.

        Attributes:
            _manager (QNetworkAccessManager):
                Qt HTTP session manager.

            _token (str):
                Stored bearer token for authenticated requests.
        """

        super().__init__(parent)

        self._token: str = token
        self._manager: QNetworkAccessManager = QNetworkAccessManager(self)

    def __make_request(self, url: str) -> QNetworkReply:
        """
        Builds and dispatches an authenticated GET request.

        Args:
            url (str):
                The full URL to request.

        Returns:
            QNetworkReply:
                The reply object for the dispatched request.
        """

        request: QNetworkRequest = QNetworkRequest()
        request.setUrl(QUrl(url))
        request.setRawHeader(b"Accept", b"application/json")
        request.setRawHeader(b"Authorization", f"Bearer {self._token}".encode())

        return self._manager.get(request)

    def __parse_reply(self, reply: QNetworkReply) -> Any:
        """
        Validates and parses a finished network reply into a JSON object.

        Args:
            reply (QNetworkReply):
                The finished network reply.

        Returns:
            Any:
                The parsed JSON response.

        Raises:
            RuntimeError:
                If the reply contains a network error or a non-200 status code.
        """

        status_code: int = reply.attribute(
            QNetworkRequest.Attribute.HttpStatusCodeAttribute
        )

        if reply.error() != QNetworkReply.NetworkError.NoError:
            raise RuntimeError(reply.errorString())

        if status_code != 200:
            raise RuntimeError(f"Unexpected status code: {status_code}")

        return json.loads(bytes(reply.readAll().data()).decode("utf-8"))

    def Fetch(self, tmdb_id: str | int) -> None:
        """
        Fetches title details from TMDB by its ID.

        GET https://api.themoviedb.org/3/movie/{tmdb_id}
        GET https://api.themoviedb.org/3/tv/{tmdb_id}

        Args:
            tmdb_id (str | int):
                The TMDB title ID.
        """

        media_type: str = "movie"

        if media_type == "movie":
            url: str = (
                TMDB.BASE_URL
                + f"/movie/{tmdb_id}?append_to_response=credits&language=pt-BR"
            )
        else:
            url: str = TMDB.BASE_URL + f"/tv/{tmdb_id}?language=pt-BR"

        reply: QNetworkReply = self.__make_request(url)

        reply.finished.connect(
            lambda: self.__process_fetch(reply, media_type)
        )

    def __process_fetch(self, reply: QNetworkReply) -> None:
        """
        Processes the fetch reply and emits arrived_data or error_occurred.

        Args:
            reply (QNetworkReply):
                The finished network reply.
        """

        media_type: str = "movie"

        try:
            j_resp: Any = self.__parse_reply(reply)

            if media_type == "movie":
                title_original: str = j_resp.get("original_title") or ""
                title_pt: str = j_resp.get("title") or title_original

                synopsis: str = j_resp.get("overview") or ""

                credits: dict = j_resp.get("credits", {})

                directors: str = ", ".join(
                    m.get("name", "")
                    for m in credits.get("crew", [])
                    if m.get("job") == "Director" and m.get("name")
                )

                cast: str = ", ".join(
                    m.get("name", "")
                    for m in credits.get("cast", [])
                    if m.get("name")
                )

                poster_path: str = j_resp.get("poster_path") or ""
                poster: str = TMDB.IMAGE_URL + poster_path if poster_path else ""

                genres: str = ", ".join(
                    g.get("name", "")
                    for g in j_resp.get("genres", [])
                    if g.get("name")
                )

                year: str = (j_resp.get("release_date") or "")[:4]

                countries: str = ", ".join(
                    c.get("name", "")
                    for c in j_resp.get("production_countries", [])
                    if c.get("name")
                )

            else:
                title_original: str = j_resp.get("original_name") or ""
                title_pt: str = j_resp.get("name") or title_original

                synopsis: str = j_resp.get("overview") or ""

                # tv endpoint doesn't bundle credits, directors not available
                directors: str = ""

                cast: str = ", ".join(
                    m.get("name", "")
                    for m in j_resp.get("created_by", [])
                    if m.get("name")
                )

                poster_path: str = j_resp.get("poster_path") or ""
                poster: str = TMDB.IMAGE_URL + poster_path if poster_path else ""

                genres: str = ", ".join(
                    g.get("name", "")
                    for g in j_resp.get("genres", [])
                    if g.get("name")
                )

                year: str = (j_resp.get("first_air_date") or "")[:4]

                countries: str = ", ".join(
                    j_resp.get("origin_country", [])
                )

            self.arrived_data.emit(
                FetchResult(
                    title_pt       = title_pt,
                    title_original = title_original,
                    synopsis       = synopsis,
                    directors      = directors,
                    cast           = cast,
                    poster         = poster,
                    genres         = genres,
                    year           = year,
                    countries      = countries,
                )
            )

        except Exception as e:
            self.error_occurred.emit(str(e))

        finally:
            reply.deleteLater()

    def Search(self, query: str) -> None:
        """
        Searches TMDB for a title and chains into Fetch on success,
        or emits error_occurred if nothing is found.

        GET https://api.themoviedb.org/3/search/movie?query=
        GET https://api.themoviedb.org/3/search/tv?query=

        Args:
            query (str):
                The title string to search for.
        """

        media_type: str = "movie"

        url: str = (
            TMDB.BASE_URL
            + f"/search/{media_type}?query={urllib.parse.quote(query)}&include_adult=true&language=pt-BR&page=1"
        )

        reply: QNetworkReply = self.__make_request(url)

        reply.finished.connect(
            lambda: self.__process_search(reply, media_type)
        )

    def __process_search(self, reply: QNetworkReply) -> None:
        """
        Processes the search reply and chains into Fetch on success.

        Args:
            reply (QNetworkReply):
                The finished network reply.
        """

        media_type: str = "movie"

        try:
            j_resp: Any = self.__parse_reply(reply)

            if j_resp.get("total_results") == 0:
                raise RuntimeError("No titles found for the given query.")

            tmdb_id: int = j_resp.get("results", [])[0].get("id")

            self.Fetch(tmdb_id, media_type)

        except Exception as e:
            self.error_occurred.emit(str(e))

        finally:
            reply.deleteLater()