#include <Servo.h>

Servo myServo;
String input = "";

void setup() {
  Serial.begin(9600);
  myServo.attach(9);
}

void loop() {
  if (Serial.available()) {
    input = Serial.readStringUntil('\n');
    input.trim();

    if (input == "ON") {
      myServo.write(90);  
    }
    else if (input == "OFF") {
      myServo.write(0);
    }
  }
}
