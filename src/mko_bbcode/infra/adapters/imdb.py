from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PySide6.QtCore import QObject, QUrl, Signal
from mko_bbcode.core.models import FetchResult
from typing import Any
import urllib.parse
import json

class IMDB(QObject):
    """
    Qt adapter for the IMDB API methods.
    """

    BASE_URL: str = "https://api.imdbapi.dev"

    arrived_data: Signal = Signal(FetchResult)
    error_occurred: Signal = Signal(str)

    def __init__(self, imdb_id: str, parent: QObject | None = None):
        """
        Initialize a FetchIMDB adapter object and trigger the fetch.

        Args:
            imdb_id (str):
                The IMDB title ID to fetch details for.

            parent (QObject | None):
                Optional Qt parent object.

        Attributes:
            _manager (QNetworkAccessManager):
                Qt HTTP session manager.
        """

        super().__init__(parent)

        self._manager: QNetworkAccessManager = QNetworkAccessManager(self)

    def __make_request(self, url: str) -> QNetworkReply:
        """
        Builds and dispatches a GET request.

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

        return self._manager.get(request)

    def Fetch(self, imdb_id: str) -> None:
        """
        Fetches title details from IMDB by its ID.

        GET https://api.imdbapi.dev/titles/{imdb_id}

        Args:
            imdb_id (str):
                The IMDB title ID.
        """

        reply: QNetworkReply = self.__make_request(
            FetchIMDB.BASE_URL + f"/titles/{imdb_id}"
        )

        reply.finished.connect(lambda: self.__process_fetch(reply))

    def __process_fetch(self, reply: QNetworkReply) -> None:
        """
        Processes the fetch reply and emits arrived_data or error_occurred.

        Args:
            reply (QNetworkReply):
                The finished network reply.
        """

        try:
            status_code: int = reply.attribute(
                QNetworkRequest.Attribute.HttpStatusCodeAttribute
            )

            if reply.error() != QNetworkReply.NetworkError.NoError:
                raise RuntimeError(reply.errorString())

            if status_code != 200:
                raise RuntimeError(f"Unexpected status code: {status_code}")

            j_resp: Any = json.loads(bytes(reply.readAll().data()).decode("utf-8"))

            title_original: str = (
                j_resp.get("originalTitle") or j_resp.get("primaryTitle") or ""
            )

            # pt-BR title falls back to original when unavailable
            title_pt: str = (
                j_resp.get("localizedTitle")
                or j_resp.get("primaryTitle")
                or title_original
            )

            synopsis: str = (
                j_resp.get("plot")
                or j_resp.get("plotLocal")
                or ""
            )

            directors: str = ", ".join(
                d.get("displayName", "")
                for d in j_resp.get("directors", [])
                if d.get("displayName")
            )

            cast: str = ", ".join(
                a.get("displayName", "")
                for a in j_resp.get("cast", [])
                if a.get("displayName")
            )

            poster: str = (
                j_resp.get("primaryImage", {}).get("url") or ""
            )

            genres: str = ", ".join(j_resp.get("genres", []))

            year: str = str(j_resp.get("startYear") or "")

            countries: str = ", ".join(j_resp.get("countriesOfOrigin", []))

            self.arrived_data.emit(
                FetchResult(
                    title_pt = title_pt,
                    title_original = title_original,
                    synopsis = synopsis,
                    directors = directors,
                    cast = cast,
                    poster = poster,
                    genres = genres,
                    year = year,
                    countries = countries,
                )
            )

        except Exception as e:
            self.error_occurred.emit(str(e))

        finally:
            reply.deleteLater()
    
    def Search(self, query: str) -> None:
        """
        Searches IMDB for a title and emits the first matching ID
        via arrived_data after chaining into Fetch, or emits
        error_occurred if nothing is found.

        GET https://api.imdbapi.dev/search/titles?query=

        Args:
            query (str):
                The title string to search for.
        """

        reply: QNetworkReply = self.__make_request(
            FetchIMDB.BASE_URL
            + f"/search/titles?query={urllib.parse.quote(query)}&limit=1"
        )

        reply.finished.connect(lambda: self.__process_search(reply))

    def __process_search(self, reply: QNetworkReply) -> None:
        """
        Processes the search reply and chains into __fetch on success.

        Args:
            reply (QNetworkReply):
                The finished network reply.
        """

        try:
            status_code: int = reply.attribute(
                QNetworkRequest.Attribute.HttpStatusCodeAttribute
            )

            if reply.error() != QNetworkReply.NetworkError.NoError:
                raise RuntimeError(reply.errorString())

            if status_code != 200:
                raise RuntimeError(f"Unexpected status code: {status_code}")

            j_resp: Any = json.loads(bytes(reply.readAll().data()).decode("utf-8"))

            titles: list = j_resp.get("titles", [])

            if not titles:
                raise RuntimeError("No titles found for the given query.")

            imdb_id: str = titles[0].get("id")
            self.__fetch(imdb_id)

        except Exception as e:
            self.error_occurred.emit(str(e))

        finally:
            reply.deleteLater()