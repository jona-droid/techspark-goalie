#include <Servo.h>

Servo goalieServo;  // Create servo object

// Define positions (Adjust these angles if your servo is reversed!)
const int POS_LEFT = 0;   // Move to 0 degrees
const int POS_CENTER = 90; // Stay at 90 degrees
const int POS_RIGHT = 180; // Move to 180 degrees

char incomingByte;

void setup() {
  Serial.begin(9600);
  
  // Attach servo to Pin 9
  goalieServo.attach(9);
  
  // Start at center
  goalieServo.write(POS_CENTER);
}

void loop() {
  if (Serial.available() > 0) {
    incomingByte = Serial.read();

    if (incomingByte == 'L') {
      goalieServo.write(POS_LEFT);
    } 
    else if (incomingByte == 'C') {
      goalieServo.write(POS_CENTER);
    } 
    else if (incomingByte == 'R') {
      goalieServo.write(POS_RIGHT);
    }
  }
}