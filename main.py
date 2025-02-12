import sys
from PyQt6.QtWidgets import QApplication, QLabel
from windows import WarningWindow, InfoWindow

def main():
    """
    Функция main, которая инициализирует приложение, создает главное окно,
    показывает его, проверяет подключение при запуске и запускает цикл событий приложения.

    Параметры:
    None

    Возвращает:
    None
    """
    app = QApplication(sys.argv)

    # Проверяем, запущено ли приложение через ярлык
    if len(sys.argv) > 1 and sys.argv[1] == "--from-icon":
        window = InfoWindow()  # Создаем окно InfoWindow
    else:
        window = WarningWindow()  # Создаем окно WarningWindow

    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

