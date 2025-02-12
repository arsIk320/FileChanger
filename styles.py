STYLES = {
    'main_window': """
        QMainWindow {
            background-color: #2C3E50;
        }
    """,
    'central_widget': """
        QWidget {
            background-color: #34495E;
            border-radius: 10px;
            margin: 10px;
        }
    """,
    'status_label': """
        QLabel {
            color: #ECF0F1;
            font-size: 18px;
            font-weight: bold;
            padding: 10px;
            background-color: #2980B9;
            border-radius: 5px;
            min-height: 50px;
        }
    """,

    'button': """
        QPushButton {
            background-color: #3498DB;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            font-size: 14px;
            min-width: 150px;
        }
        QPushButton:hover {
            background-color: #2980B9;
            transform: scale(1.05);
            transition: transform 0.2s;
        }
        QPushButton:pressed {
            background-color: #2574A9;
            transform: scale(0.95);
        }
    """,
    'list_widget': """
        QListWidget {
            background-color: #445566;
            border: 1px solid #566573;
            border-radius: 5px;
            color: #ECF0F1;
            font-size: 14px;
            padding: 5px;
        }
        QListWidget::item {
            padding: 5px;
        }
        QListWidget::item:selected {
            background-color: #3498DB;
        }
        QListWidget::item:hover {
            background-color: #4FA5D5;
        }
    """,
    'file_list_label': """
        QLabel {
            color: #ECF0F1;
            font-size: 16px;
            font-weight: bold;
            padding: 5px;
            margin-top: 10px;
        }
    """,
    'info_window': """
        QDialog {
            background-color: #34495E;
        }
    """,
    'label_hello': """
        QLabel {
            color: #ECF0F1;
            font-size: 24px;
            font-weight: bold;
            padding: 20px;
        }
    """,
    'label_main': """
        QLabel {
            color: #ECF0F1;
            font-size: 16px;
            padding: 10px;
            line-height: 1.5;
        }
    """,
    'button_info': """
        QPushButton {
            background-color: #2ECC71;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            font-size: 16px;
            min-width: 200px;
        }
        QPushButton:hover {
            background-color: #27AE60;
            transform: scale(1.05);
            transition: transform 0.2s;
        }
        QPushButton:pressed {
            background-color: #229954;
            transform: scale(0.95);
        }
    """,
    'button_warning': """
        QPushButton {
            background-color: #E74C3C;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            font-size: 14px;
            min-width: 100px;
        }
        QPushButton:hover {
            background-color: #C0392B;
        }
        QPushButton:pressed {
            background-color: #A93226;
        }
    """
}


