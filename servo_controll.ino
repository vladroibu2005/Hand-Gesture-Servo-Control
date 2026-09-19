#include <ESP32Servo.h>

Servo servo;

const int servoPin = 18;

void setup() {
  Serial.begin(115200);

  // Atașăm servomotorul la GPIO 18
  servo.attach(servoPin);

  // Poziția inițială
  servo.write(90);
}

void loop() {

  // Verificăm dacă Python a trimis ceva
  if (Serial.available() > 0) {

    // Citim valoarea primită
    int angle = Serial.read();

    // Ne asigurăm că este un unghi valid
    if (angle >= 0 && angle <= 180) {
      servo.write(angle);
    }
  }
}