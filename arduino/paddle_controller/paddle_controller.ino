#define SERVO_PIN1 9
#define SERVO_PIN2 8
#define SERVO_PIN3 7
#define SERVO_PIN4 6
#define SERVO_PIN5 5
#define BAUD_RATE 9600
#define PULSE_FLOOR 500
#define PULSE_CEILING 2400
#define REFRESH_PERIOD 1

#include <Servo.h>

Servo board1;
Servo board2;
Servo board3;
Servo board4;
Servo board5;
const Servo* boards[5] = {&board1, &board2, &board3, &board4, &board5};

void setup() {
  board1.attach(SERVO_PIN1);
  board2.attach(SERVO_PIN2, PULSE_FLOOR, PULSE_CEILING);
  board3.attach(SERVO_PIN3, PULSE_FLOOR, PULSE_CEILING);
  board4.attach(SERVO_PIN4, PULSE_FLOOR, PULSE_CEILING);
  board5.attach(SERVO_PIN5, PULSE_FLOOR, PULSE_CEILING);
  Serial.begin(BAUD_RATE);
}

void loop() {
  delay(REFRESH_PERIOD);
  serialCommunication();
}
