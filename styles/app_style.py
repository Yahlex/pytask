"""
Thème sombre moderne pour l'application
Palette inspirée de Catppuccin Mocha
"""

APP_STYLESHEET = """
/* === FENÊTRE PRINCIPALE === */
QMainWindow {
    background-color: #1e1e2e;
}

QWidget {
    background-color: #1e1e2e;
    color: #cdd6f4;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 12pt;  /* ✅ Augmenté de 10pt → 12pt */
}

/* === BOUTONS === */
QPushButton {
    background-color: #313244;
    color: #cdd6f4;
    border: 2px solid #45475a;
    border-radius: 6px;
    padding: 10px 20px;
    font-weight: bold;
    font-size: 12pt;  /* ✅ Explicite */
}

QPushButton:hover {
    background-color: #45475a;
    border-color: #89b4fa;
}

QPushButton:pressed {
    background-color: #89b4fa;
    color: #1e1e2e;
}

QPushButton:disabled {
    background-color: #181825;
    color: #6c7086;
    border-color: #313244;
}

/* === TABLEAU === */
QTableWidget {
    background-color: #1e1e2e;
    alternate-background-color: #181825;
    gridline-color: #313244;
    border: 1px solid #45475a;
    border-radius: 8px;
    font-size: 11pt;  /* ✅ Légèrement plus petit pour les cellules */
}

QTableWidget::item {
    color: #cdd6f4;
    padding: 10px;  /* ✅ Plus d'espace */
}


QTableWidget::item:focus {
    outline: none;
    border: none;
}

/* ✅ Survol : fond gris moyen + texte BLANC */
QTableWidget::item:hover {
    background-color: #585b70;
    color: #ffffff;
}

/* ✅ Sélection : fond bleu vif + texte NOIR */
QTableWidget::item:selected {
    background-color: #89b4fa;
    color: #181825;
    font-weight: bold;
}

QHeaderView::section {
    background-color: #313244;
    color: #cdd6f4;
    padding: 12px;  /* ✅ Plus d'espace */
    border: none;
    font-weight: bold;
    text-transform: uppercase;
    font-size: 11pt;
}

/* === CHAMPS DE TEXTE === */
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #313244;
    color: #cdd6f4;
    border: 2px solid #45475a;
    border-radius: 6px;
    padding: 8px;
    selection-background-color: #89b4fa;
    selection-color: #1e1e2e;
    font-size: 12pt;  /* ✅ Explicite */
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border-color: #89b4fa;
}

/* === COMBOBOX === */
QComboBox {
    background-color: #313244;
    color: #cdd6f4;
    border: 2px solid #45475a;
    border-radius: 6px;
    padding: 8px;
    font-size: 12pt;  /* ✅ Explicite */
}

QComboBox:hover {
    border-color: #89b4fa;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #cdd6f4;
    margin-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #313244;
    color: #cdd6f4;
    selection-background-color: #89b4fa;
    selection-color: #1e1e2e;
    border: 1px solid #45475a;
    font-size: 12pt;  /* ✅ Explicite */
}

/* === DATEEDIT / TIMEEDIT === */
QDateEdit, QTimeEdit, QDateTimeEdit {
    background-color: #313244;
    color: #cdd6f4;
    border: 2px solid #45475a;
    border-radius: 6px;
    padding: 8px;
    font-size: 12pt;  /* ✅ Explicite */
}

QDateEdit:focus, QTimeEdit:focus, QDateTimeEdit:focus {
    border-color: #89b4fa;
}

QDateEdit::drop-down, QTimeEdit::drop-down, QDateTimeEdit::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: right;
    width: 30px;
    border-left: 1px solid #45475a;
}

QCalendarWidget {
    background-color: #1e1e2e;
    color: #cdd6f4;
}

QCalendarWidget QAbstractItemView {
    background-color: #313244;
    selection-background-color: #89b4fa;
    selection-color: #1e1e2e;
}

/* === LABELS === */
QLabel {
    color: #cdd6f4;
    background-color: transparent;
    font-size: 12pt;  /* ✅ Explicite */
}

/* === CHECKBOX / RADIO === */
QCheckBox, QRadioButton {
    color: #cdd6f4;
    spacing: 8px;
    font-size: 12pt;  /* ✅ Explicite */
}

QCheckBox::indicator, QRadioButton::indicator {
    width: 20px;
    height: 20px;
    border: 2px solid #45475a;
    border-radius: 4px;
    background-color: #313244;
}

QCheckBox::indicator:checked, QRadioButton::indicator:checked {
    background-color: #89b4fa;
    border-color: #89b4fa;
}

/* === SCROLLBAR === */
QScrollBar:vertical {
    background-color: #1e1e2e;
    width: 14px;
    border-radius: 7px;
}

QScrollBar::handle:vertical {
    background-color: #45475a;
    border-radius: 7px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #585b70;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* === ONGLETS === */
QTabWidget::pane {
    border: 1px solid #45475a;
    border-radius: 6px;
    background-color: #1e1e2e;
}

QTabBar::tab {
    background-color: #313244;
    color: #cdd6f4;
    padding: 12px 24px;  /* ✅ Plus d'espace */
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 2px;
    font-size: 12pt;  /* ✅ Explicite */
}

QTabBar::tab:selected {
    background-color: #89b4fa;
    color: #1e1e2e;
    font-weight: bold;
}

QTabBar::tab:hover:!selected {
    background-color: #45475a;
}

/* === DIALOG === */
QDialog {
    background-color: #1e1e2e;
}

QMessageBox {
    background-color: #1e1e2e;
    font-size: 12pt;  /* ✅ Explicite */
}
"""
