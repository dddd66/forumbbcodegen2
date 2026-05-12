import sys

from PySide6.QtWidgets import QApplication

from bbcodegen.ui.mainwindow import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    _ = app.exec()
    


if __name__ == "__main__":
    main()
