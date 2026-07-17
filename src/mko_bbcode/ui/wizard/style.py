from PySide6.QtWidgets import QLabel, QLineEdit, QPlainTextEdit, QComboBox, QGroupBox
from PySide6.QtGui import QPalette
from PySide6.QtCore import Qt

# color palettes
ACCENT     = "#4A90D9" # main blue
REQUIRED   = "#C0392B" # red for the necessary ones
HINT_COLOR = "#333333" # hint text
BG_GROUP   = "transparent"

# global wizard stylesheet
WIZARD_QSS = """
QWizard QLabel#qt_wizard_titleLabel {
    font-size: 16px;
    font-weight: bold;
}
QWizard QLabel#qt_wizard_subTitleLabel {
    font-size: 11px;
}

QWizardPage QLabel {
    font-size: 12px;
}

QLineEdit, QPlainTextEdit, QTextEdit {
    border: 1px solid palette(mid);
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 12px;
    selection-background-color: #4A90D9;
}
QLineEdit:focus, QPlainTextEdit:focus, QTextEdit:focus {
    border: 1px solid #4A90D9;
}

QComboBox {
    border: 1px solid palette(mid);
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 12px;
    min-height: 28px;
}
QComboBox:focus { border: 1px solid #4A90D9; }
QComboBox::drop-down { border: none; width: 24px; }
QComboBox::down-arrow { width: 12px; height: 12px; }

QGroupBox {
    border: 1px solid palette(mid);
    border-radius: 6px;
    margin-top: 14px;
    padding-top: 6px;
    font-size: 11px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 6px;
    left: 10px;
}

QWizard QPushButton {
    border: 1px solid palette(mid);
    border-radius: 4px;
    padding: 5px 14px;
    font-size: 12px;
    min-width: 72px;
}
QWizard QPushButton:hover {
    border-color: #4A90D9;
}
QWizard QPushButton:pressed {
    background-color: #4A90D9;
    color: white;
}
QWizard QPushButton:disabled {
    color: palette(mid);
}

QWizardPage QPushButton {
    border: 1px solid palette(mid);
    border-radius: 4px;
    padding: 5px 14px;
    font-size: 12px;
}
QWizardPage QPushButton:hover  { border-color: #4A90D9; }
QWizardPage QPushButton:pressed { background-color: #4A90D9; color: white; }

QRadioButton {
    font-size: 12px;
    spacing: 6px;
}
QRadioButton::indicator {
    width: 14px; height: 14px;
    border-radius: 7px;
    border: 2px solid palette(mid);
}
QRadioButton::indicator:checked {
    background-color: #4A90D9;
    border-color: #4A90D9;
}

QScrollBar:vertical {
    width: 8px;
    margin: 0;
}
QScrollBar::handle:vertical {
    border-radius: 4px;
    min-height: 24px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }

QListWidget {
    border: none;
    font-size: 12px;
}
QListWidget::item:selected {
    color: #4A90D9;
    font-weight: bold;
}
"""

def required_label(text: str) -> QLabel:
    """
    Returns a label with * for the necessary ones.
    """

    lbl = QLabel(f"{text}  <span style='color:{REQUIRED}'>*</span>")
    lbl.setTextFormat(Qt.TextFormat.RichText)
    return lbl


def optional_label(text: str) -> QLabel:
    """
    Returns a optional (default) label.
    """

    lbl = QLabel(text)
    return lbl

def hint_label(text: str) -> QLabel:
    """
    Returns a hint label.
    """

    lbl = QLabel(text)
    lbl.setStyleSheet("font-size: 13px;")
    lbl.setForegroundRole(QPalette.ColorRole.PlaceholderText)
    lbl.setWordWrap(True)
    return lbl

def section_group(title: str) -> QGroupBox:
    return QGroupBox(title)

def mark_invalid(widget: QLineEdit | QPlainTextEdit | QComboBox, invalid: bool):
    """
    Red borders when the necessary one is missing.
    """
    
    if invalid:
        widget.setStyleSheet("border: 1px solid #E05252;")
    else:
        widget.setStyleSheet("")
