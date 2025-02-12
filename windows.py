from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QFileDialog, QWidget, QDialog, QSpacerItem, QSizePolicy, QMessageBox, QProgressBar
from PyQt6.QtCore import Qt, QIODevice
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtSerialPort import QSerialPort
import time
import os, serial
from serial.tools import list_ports
from styles import STYLES

class WarningWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(STYLES['info_window'])
        self.setWindowTitle("Предупреждение")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        label_warning = QLabel("Внимание!")
        label_warning.setStyleSheet(STYLES['label_hello'])
        label_warning.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label_warning)

        label_message = QLabel(
            "Это приложение следует запускать через ярлык на рабочем столе.\n"
            "Вы уверены, что хотите продолжить?"
        )
        label_message.setStyleSheet(STYLES['label_main'])
        label_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label_message)

        button_layout = QHBoxLayout()

        continue_button = QPushButton("Продолжить")
        continue_button.setStyleSheet(STYLES['button'])
        continue_button.clicked.connect(self.continue_to_info)

        exit_button = QPushButton("Выйти")
        exit_button.setStyleSheet(STYLES['button'])
        exit_button.clicked.connect(self.close)

        button_layout.addWidget(continue_button)
        button_layout.addWidget(exit_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def continue_to_info(self):
        self.info_window = InfoWindow()
        self.info_window.show()
        self.close()

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(STYLES['main_window'])
        self.setWindowTitle("FileChangerStart")
        self.setGeometry(0, 0, 600, 300)
        self.Label()
        self.Buttons()
        self.show()

    def Buttons(self):
        button_no = QPushButton("Отмена", self)
        button_no.setGeometry(325, 200, 120, 40)
        button_no.setStyleSheet(STYLES['button'])
        button_no.clicked.connect(self.close)

        button_yes = QPushButton("Продолжить", self)
        button_yes.setGeometry(175, 200, 120, 40)
        button_yes.setStyleSheet(STYLES['button'])
        button_yes.clicked.connect(self.replace)

    def replace(self):
        self.w2 = InfoWindow()
        self.w2.show()
        self.close()

    def Label(self):
        label_name = QLabel(self)
        label_name.setText('Запуститься программа FileChanger. Продолжить?')
        label_name.setAutoFillBackground(True)
        label_name.resize(600, 50)
        label_name.setStyleSheet(STYLES['label'])
        label_name.setFont(QFont('Arial', 15))
        label_name.move(70, 50)

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
            self.w2 = Window_Main()
            self.w2.show()
            self.close()

class Window_Main(QMainWindow):
    def __init__(self):
        super().__init__()

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

        delete_button = QPushButton("Удалить файл")
        delete_button.setStyleSheet(STYLES['button'])
        delete_button.setIcon(QIcon("icons/delete.png"))
        delete_button.clicked.connect(self.delete_selected_file)
        button_layout.addWidget(delete_button)


        # Добавляем элементы на основной макет
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

        file_path = selected_item.data(Qt.ItemDataRole. UserRole)

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
                    'AT+FTPSERV="eu-central-1.sftpcloud.io"',
                    'AT+FTPPORT=21',
                    'AT+FTPUN="senya"',
                    'AT+FTPPW="admin12345"',
                    f'AT+FTPPUTNAME="{file_name}"',
                    'AT+FTPPUTPATH="/"',
                    'AT+FTPPUT=1',
                    f'AT+FTPPUT=2,{len(data_content)+1}'
                ]

                for i, command in enumerate(commands):
                    print(f'Отправка команды: {command}')
                    self.serial_port.write((command + '\r\n').encode())
                    time.sleep(5)

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
        
        # Пытаемся декодировать ответ, игнорируя ошибки
        try:
            return response.decode('utf-8', errors='ignore').strip()
        except UnicodeDecodeError:
            # Если декодирование не удалось, возвращаем шестнадцатеричное представление
            return response.hex()