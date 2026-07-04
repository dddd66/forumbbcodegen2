from bbcodegen.ui.mainwindow import MainWindow
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from pathlib import Path
import sys

def main():
    app = QApplication(sys.argv)

    icon_path = Path(__file__).parent.parent / "assets" / "favicon.ico"
    app.setWindowIcon(QIcon(str(icon_path)))

    window = MainWindow()
    window.show()
    _ = app.exec()

if __name__ == "__main__":
    main()
