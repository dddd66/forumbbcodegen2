import json

from PySide6.QtCore import QObject, QUrl, Signal
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest


class FetchIMDB(QObject):
    arrived_data = Signal(object)
    error_occurred = Signal(str)

    def __init__(self, imdb_id: str = "", Parent=None):
        super().__init__(Parent)
        self.network = QNetworkAccessManager()
        self.url = QUrl(f"https://api.imdbapi.dev/titles/{imdb_id}")
        request = QNetworkRequest()
        request.setUrl(self.url)
        request.setRawHeader(b"accept", b"application/json")
        reply = self.network.get(request)
        reply.finished.connect(lambda: self.process_reply(reply))

    def process_reply(self, reply: QNetworkReply):
        try:
            status_code = reply.attribute(QNetworkRequest.Attribute.HttpStatusCodeAttribute)

            if reply.error() != QNetworkReply.NetworkError.NoError:
                raise RuntimeError(reply.errorString())

            if status_code != 200:
                raise RuntimeError(status_code)

            raw = bytes(reply.readAll().data())
            text = raw.decode("utf-8")
            reply_data = json.loads(text)
            self.arrived_data.emit(reply_data)

        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            reply.deleteLater()
