from mko_bbcode.ui.wizard import MKOWizard
from PySide6.QtWidgets import QApplication
from mko_bbcode.utils import Resource
from PySide6.QtGui import QIcon
import sys

def main() -> None:
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(str(Resource.path("assets/favicon.ico"))))

    window = MKOWizard()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
