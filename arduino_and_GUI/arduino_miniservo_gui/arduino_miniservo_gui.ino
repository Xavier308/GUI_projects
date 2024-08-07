#include <Servo.h>

Servo myservo;  // create servo object to control a servo
int pos = 0;    // variable to store the servo position

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
}

void loop() {
  if (Serial.available() > 0) {
    int angle = Serial.parseInt(); // read the incoming byte
    if (angle >= 0 && angle <= 180) {
      myservo.write(angle);
      Serial.print("Moved to ");
      Serial.println(angle);
    }
  }
}
