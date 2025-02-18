#include <SoftwareSerial.h>

// Создаем объект SoftwareSerial для связи с SIM800L
SoftwareSerial mySerial(7, 8); // SIM800L Tx & Rx подключены к pin 3 и 2 Arduino

void setup() {

  pinMode(10, OUTPUT);
  
  digitalWrite(10, 0);
  delay(1200);
  digitalWrite(10, 1);
  delay(1200);
  // Инициализируем сериальную связь с Arduino и Serial Monitor
  Serial.begin(9600);
  // Инициализируем сериальную связь с Arduino и SIM800L
  mySerial.begin(9600);
  Serial.println("Initializing...");
  delay(1000);

  // Тестовая команда для проверки связи
  mySerial.println("AT");
  updateSerial();

  // Тест сигнального качества
  mySerial.println("AT+CSQ");
  updateSerial();

  // Чтение информации о SIM-карте
  mySerial.println("AT+CCID");
  updateSerial();

  // Проверка регистрации в сети
  mySerial.println("AT+CREG?");
  updateSerial();
}

void loop() {
  updateSerial();
}

// Функция для передачи данных между Serial и SoftwareSerial
void updateSerial() {
  delay(500);
  while (Serial.available()) {
    mySerial.write(Serial.read()); // Передаем данные из Serial в SoftwareSerial
  }
  while (mySerial.available()) {
    Serial.write(mySerial.read()); // Передаем данные из SoftwareSerial в Serial
  }
}