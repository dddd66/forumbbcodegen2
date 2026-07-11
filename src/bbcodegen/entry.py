from bbcodegen.ui.mainwindow import MainWindow
from PySide6.QtWidgets import QApplication
from bbcodegen.utils import Resource
from PySide6.QtGui import QIcon
import sys

def main() -> None:
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(str(Resource.path("assets/favicon.ico"))))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
