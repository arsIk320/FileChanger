from PyQt6.QtWidgets import (
    QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, 
    QFileDialog, QWidget, QDialog, QSpacerItem, QSizePolicy, QMessageBox, QProgressBar, QInputDialog, 
    QLineEdit, QVBoxLayout
)
from PyQt6.QtCore import Qt, QIODevice
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtSerialPort import QSerialPort
import time
import os
from serial.tools import list_ports
from styles import STYLES


from PyQt6.QtWidgets import QFileDialog

from PyQt6.QtWidgets import QFileDialog

def create_file(file_name=None, txt=""):
    """
    Создает файл с указанным именем и записывает в него текст.
    Если имя файла не указано, предоставляет возможность выбрать место и имя файла через диалог.
    :param file_name: Имя файла (включая путь), который будет создан. Если None, открывается диалог выбора.
    :param txt: Текст, который будет записан в файл.
    :return: Путь к созданному файлу или None, если сохранение отменено.
    """
    try:
        # Если имя файла не указано, открываем диалог выбора
        if file_name is None:
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(
                None,  # Родительское окно (None для глобального)
                "Сохранить файл",  # Заголовок диалогового окна
                "",  # Начальный путь (пустой для текущей директории)
                "Текстовые файлы (*.txt);;Все файлы (*)",  # Фильтры типов файлов
                options=options
            )
        
        # Если пользователь выбрал путь или имя файла было передано
        if file_name:
            # Открываем файл в режиме записи ('w') и записываем текст
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(txt)
            print(f"Файл '{file_name}' успешно создан и текст записан.")
            return file_name  # Возвращаем путь к созданному файлу
        else:
            print("Сохранение отменено пользователем.")
            return None
    except Exception as e:
        # В случае ошибки выводим сообщение
        print(f"Ошибка при создании файла: {e}")
        return None






class InfoWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(STYLES['info_window'])
        self.setWindowTitle("Информация")
        self.setGeometry(100, 100, 800, 400)
        layout = QVBoxLayout()
        # Заголовок
        label_hello = QLabel("Дорогой пользователь!")
        label_hello.setStyleSheet(STYLES['label_hello'])
        label_hello.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label_hello)
        # Основной текст
        label_main = QLabel(
            "Перед началом работы, убедительно просим ознакомиться с документацией.\n"
            "Проверьте, что у вас установлена последняя версия приложения.\n"
            "В случае возникновения вопросов, вы всегда можете задать вопрос нам: filechanger.io@gmail.com.\n"
            "Надеемся, что использование нашего устройства принесёт вам удовольствие!"
        )
        label_main.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_main.setStyleSheet(STYLES['label_main'])
        layout.addWidget(label_main)
        # Кнопка продолжения
        button_continue = QPushButton("Продолжить")
        button_continue.setStyleSheet(STYLES['button_info'])
        button_continue.setIcon(QIcon("icons/continue.png"))
        button_continue.clicked.connect(self.areplace)
        layout.addWidget(button_continue, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def areplace(self):
        self.w2 = LoginWindow()
        self.w2.show()
        self.close()

host = ''
port = ''
username = ''
password = ''

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(STYLES['info_window'])
        self.setWindowTitle("Вход")
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        
        # Заголовок
        label_hello = QLabel("Введите данные для входа:")
        label_hello.setStyleSheet(STYLES['label_hello'])
        label_hello.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label_hello)
        
        # Поле для ввода хоста
        self.host_input = QLineEdit(self)
        self.host_input.setPlaceholderText("Хост сервера")
        self.host_input.setStyleSheet(STYLES['button_info'])  # Используем стиль кнопки для полей ввода
        layout.addWidget(self.host_input)
        
        # Поле для ввода порта
        self.port_input = QLineEdit(self)
        self.port_input.setPlaceholderText("Порт")
        self.port_input.setStyleSheet(STYLES['button_info'])
        layout.addWidget(self.port_input)
        
        # Поле для ввода имени пользователя
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Имя пользователя")
        self.username_input.setStyleSheet(STYLES['button_info'])
        layout.addWidget(self.username_input)
        
        # Поле для ввода пароля
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)  # Скрываем пароль
        self.password_input.setStyleSheet(STYLES['button_info'])
        layout.addWidget(self.password_input)
        
        # Кнопка входа
        login_button = QPushButton("Войти")
        login_button.setStyleSheet(STYLES['button_info'])
        login_button.setIcon(QIcon("icons/login.png"))
        login_button.clicked.connect(self.check_login)
        layout.addWidget(login_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)
    
    def check_login(self):
        """Проверка введенных данных."""
        host = self.host_input.text().strip()
        port = self.port_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not host or not port or not username or not password:
            self.show_message("Ошибка", "Все поля должны быть заполнены.")
            return
        
        try:
            port = int(port)  # Проверяем, что порт является числом
        except ValueError:
            self.show_message("Ошибка", "Порт должен быть числом.")
            return
        
        # Здесь можно добавить проверку подключения к серверу или другие действия
        print(f"Введенные данные: Хост={host}, Порт={port}, Имя пользователя={username}, Пароль={password}")

        # Если все корректно, переходим к основному окну
        self.w2 = Window_Main(host=host, port=port, username=username, password=password)
        self.w2.show()
        self.close()
    
    def show_message(self, title, message):
        """Показывает сообщение об ошибке."""
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.exec()

class Window_Main(QMainWindow):
    def __init__(self, host=None, port=None, username=None, password=None):
        super().__init__()
        # Store the passed parameters as instance attributes
        self.host = host
        self.port = port
        self.username = username
        self.password = password


        self.setGeometry(100, 100, 1080, 720)
        self.setStyleSheet(STYLES['main_window'])
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet(STYLES['central_widget'])
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)  # Изначально скрыт
        self.main_layout.addWidget(self.progress_bar)
        # Статус подключения
        self.status_label = QLabel("Нажмите кнопку для проверки подключения.")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(STYLES['status_label'])
        self.main_layout.addWidget(self.status_label)
        # Кнопка проверки подключения
        self.check_button = QPushButton("Проверить подключение")
        self.check_button.setStyleSheet(STYLES['button'])
        self.check_button.setIcon(QIcon("icons/check.png"))
        self.check_button.clicked.connect(self.check_connection)
        self.main_layout.addWidget(self.check_button, alignment=Qt.AlignmentFlag.AlignCenter)
        # Добавляем текст над списком файлов
        self.file_list_label = QLabel("Список файлов для отправки:")
        self.file_list_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_list_label.setStyleSheet(STYLES['file_list_label'])
        self.main_layout.addWidget(self.file_list_label)
        # Список файлов для отображения
        self.data_file_list = QListWidget()
        self.data_file_list.setStyleSheet(STYLES['list_widget'])
        self.main_layout.addWidget(self.data_file_list)
        # Добавляем кнопки для управления файлами
        self.button_layout()
        # Инициализация последовательного порта
        self.serial_port = QSerialPort()
        # Отображаем окно
        self.show()

    def check_connection(self):
        ports = list_ports.comports()
        arduino_found = False
        # Закрываем порт, если он открыт
        if self.serial_port.isOpen():
            self.serial_port.close()
        if ports:
            for port in ports:
                try:
                    if "USB-SERIAL CH340" in port.description or "USB-SERIAL CH340" in port.device:
                        self.serial_port.setPortName(port.device)
                        self.serial_port.setBaudRate(9600)
                        if self.serial_port.open(QIODevice.OpenModeFlag.ReadWrite):
                            time.sleep(2)  # Даем время на инициализацию
                            self.status_label.setText(f"Подключено к {port.device}")
                            self.status_label.setStyleSheet(STYLES['status_label'] + "color: #2ECC71;")
                            arduino_found = True
                            print(f"Checking port: {port.device} - {port.description}")
                            break
                        else:
                            print(f"Не удалось открыть порт: {port.device} - {port.description}")
                except Exception as e:
                    print(f"Ошибка подключения: {e}")
            if not arduino_found:
                self.status_label.setText("Arduino не найдена.")
                self.status_label.setStyleSheet(STYLES['status_label'] + "color: #E74C3C;")
        else:
            self.status_label.setText("Нет доступных COM-портов.")
            self.status_label.setStyleSheet(STYLES['status_label'] + "color: #E74C3C;")

    def button_layout(self):
        button_layout = QHBoxLayout()
        select_data_button = QPushButton("Выбрать файл")
        select_data_button.setStyleSheet(STYLES['button'])
        select_data_button.setIcon(QIcon("icons/select.png"))
        select_data_button.clicked.connect(self.select_data_file)
        button_layout.addWidget(select_data_button)
        send_button = QPushButton("Отправить файл")
        send_button.setStyleSheet(STYLES['button'])
        send_button.setIcon(QIcon("icons/send.png"))
        send_button.clicked.connect(self.send_file_to_server)
        button_layout.addWidget(send_button)
        receive_button = QPushButton("Получить файл")
        receive_button.setStyleSheet(STYLES['button'])
        receive_button.setIcon(QIcon("icons/receive.png"))
        receive_button.clicked.connect(self.receive_file_from_server)
        button_layout.addWidget(receive_button)
        delete_button = QPushButton("Удалить файл")
        delete_button.setStyleSheet(STYLES['button'])
        delete_button.setIcon(QIcon("icons/delete.png"))
        delete_button.clicked.connect(self.delete_selected_file)
        button_layout.addWidget(delete_button)
        self.main_layout.addLayout(button_layout)

    def select_data_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл с данными", "", "Все файлы (*)")
        if file_path:
            file_name = os.path.basename(file_path)
            item = QListWidgetItem(file_name)
            item.setData(Qt.ItemDataRole.UserRole, file_path)
            self.data_file_list.addItem(item)

    def delete_selected_file(self):
        current_row = self.data_file_list.currentRow()
        if current_row != -1:
            item_to_remove = self.data_file_list.takeItem(current_row)
            print(f"Удален файл: {item_to_remove.text()}")

    def send_file_to_server(self):
        current_row = self.data_file_list.currentRow()
        if current_row == -1:
            self.show_message("Ошибка", "Необходимо выбрать файл из списка.")
            return
        selected_item = self.data_file_list.item(current_row)
        file_name = selected_item.text()
        file_path = selected_item.data(Qt.ItemDataRole.UserRole)
        try:
            with open(file_path, 'rb') as data_file:
                data_content = data_file.read()
                # Показываем и сбрасываем прогресс-бар
                self.progress_bar.setVisible(True)
                self.progress_bar.setValue(0)
                commands = [
                    'AT+SAPBR=3,1,"CONTYPE","GPRS"',
                    'AT+SAPBR=3,1,"APN","internet.mts.ru"',
                    'AT+SAPBR=1,1',
                    'AT+SAPBR=2,1',
                    'AT+FTPCID=1',
                    f'AT+FTPSERV="{self.host}"',
                    f'AT+FTPPORT={self.port}',
                    f'AT+FTPUN="{self.username}"',
                    f'AT+FTPPW="{self.password}"',
                    f'AT+FTPPUTNAME="{file_name}"',
                    'AT+FTPPUTPATH="/"',
                    'AT+FTPPUT=1',
                    f'AT+FTPPUT=2,{len(data_content)}'
                ]
                for i, command in enumerate(commands):
                    print(f'Отправка команды: {command}')
                    self.serial_port.write((command + '\r\n').encode())
                    time.sleep(2)
                    response = self.wait_for_response()
                    print(f'Ответ на команду "{command}": {response}')
                    self.progress_bar.setValue(int((i + 1) / len(commands) * 40))
                print('Отправка содержимого файла...')
                self.serial_port.write(data_content)
                time.sleep(3)
                response = self.wait_for_response()
                print(f'Ответ на отправку содержимого файла: {response}')
                time.sleep(5)
                self.progress_bar.setValue(80)
                self.serial_port.write(('AT+FTPPUT=2,0' + '\r\n').encode())
                response = self.wait_for_response()
                print(f'Ответ на команду "AT+FTPPUT=2,0": {response}')
                self.progress_bar.setValue(100)
                if "OK" in response:
                    self.show_message("Успех", f"Файл '{file_name}' успешно отправлен.")
                    item_to_remove = self.data_file_list.takeItem(current_row)
                    print(f"Файл '{item_to_remove.text()}' удален из списка после успешной отправки.")
                else:
                    self.show_message("Ошибка", f"Не удалось отправить файл '{file_name}'. Ответ сервера: {response}")
        except Exception as e:
            self.show_message("Ошибка", f"Ошибка при отправке файла: {e}")
        finally:
            self.progress_bar.setVisible(False)


    def receive_file_from_server(self):
        # Диалог для выбора папки сохранения
        save_folder = QFileDialog.getExistingDirectory(
            self,  # Родительское окно
            "Выберите папку для сохранения файла",  # Заголовок диалогового окна
            "",  # Начальный путь (пустой для текущей директории)
        )

        if not save_folder:
            self.show_message("Ошибка", "Папка для сохранения не выбрана.")
            return

        # Диалог для ввода имени файла на сервере
        file_name, ok = QInputDialog.getText(
            self,
            "Получение файла",
            "Введите имя файла на сервере:",
        )

        if not ok or not file_name:
            self.show_message("Ошибка", "Имя файла не указано.")
            return

        try:
            # Показываем прогресс-бар
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)

            commands = [
                'AT+SAPBR=3,1,"CONTYPE","GPRS"',
                'AT+SAPBR=3,1,"APN","internet.mts.ru"',
                'AT+SAPBR=1,1',
                'AT+SAPBR=2,1',
                'AT+FTPCID=1',
                f'AT+FTPSERV="{self.host}"',
                f'AT+FTPPORT={self.port}',
                f'AT+FTPUN="{self.username}"',
                f'AT+FTPPW="{self.password}"',
                f'AT+FTPGETNAME="{file_name}"',  # Устанавливаем имя файла на сервере
                'AT+FTPGETPATH="/"',
                'AT+FTPGET=1',
                'AT+FTPGET=2,100',
            ]

            s = ''
            for i, command in enumerate(commands):
                print(f'Отправка команды: {command}')
                self.serial_port.write((command + '\r\n').encode())
                time.sleep(2)  # Ждем ответа
                response = self.wait_for_response()
                print(f'Ответ на команду "{command}": {response}')
                s += response
                # Обновляем прогресс-бар
                self.progress_bar.setValue(int((i + 1) / len(commands) * 50))

            # Завершаем прогресс-бар
            self.progress_bar.setValue(100)

            if '+FTPGET: 2' in s:
                start_str = '+FTPGET: 2'
                start_index = s.index(start_str) + len(start_str) + 3
                end_str = 'OK'
                end_index = s.rfind(end_str)
                txt = s[start_index:end_index]

                # Полный путь к файлу
                file_path = os.path.join(save_folder, file_name)

                # Создаем файл
                create_file(file_path, txt)

                self.show_message("Успех", f"Файл успешно сохранен по пути: {file_path}")
            else:
                self.show_message("Ошибка", "Не удалось получить файл с сервера.")
        except Exception as e:
            self.show_message("Ошибка", f"Ошибка при получении файла: {e}")
        finally:
            self.progress_bar.setVisible(False)



    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Information if title == "Успех" else QMessageBox.Icon.Warning)
        msg.exec()

    def wait_for_response(self):
        """Ожидает ответа от SIM800L и возвращает его."""
        response = b""
        start_time = time.time()
        while time.time() - start_time < 5:  # Таймаут в 5 секунд
            if self.serial_port.waitForReadyRead(1000):  # Ждем данные в течение 1 секунды
                response += self.serial_port.readAll().data()
        try:
            return response.decode('utf-8', errors='ignore').strip()
        except UnicodeDecodeError:
            return response.hex()
