#include <Servo.h>

Servo goalieServo;  // Create servo object

// Define positions (Adjust these angles if your servo is reversed!)
const int POS_LEFT = 0;   // Move to 0 degrees
const int POS_CENTER = 90; // Stay at 90 degrees
const int POS_RIGHT = 180; // Move to 180 degrees

// LED pins
const int RED_LED = 12;    // Red LED for LEFT position
const int GREEN_LED = 13;  // Green LED for RIGHT position

char incomingByte;

void setup() {
  Serial.begin(9600);
  
  // Attach servo to Pin 9
  goalieServo.attach(9);
  
  // Setup LED pins
  pinMode(RED_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
  
  // Test LEDs on startup - blink both
  digitalWrite(RED_LED, HIGH);
  digitalWrite(GREEN_LED, HIGH);
  delay(1000);
  digitalWrite(RED_LED, LOW);
  digitalWrite(GREEN_LED, LOW);
  
  // Start at center - turn off both LEDs
  goalieServo.write(POS_CENTER);
  digitalWrite(RED_LED, LOW);
  digitalWrite(GREEN_LED, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    
    // Debug: Print what was received
    Serial.print("Received: ");
    Serial.println(incomingByte);

    if (incomingByte == 'L') {
      goalieServo.write(POS_LEFT);
      digitalWrite(RED_LED, HIGH);   // Turn ON red LED
      digitalWrite(GREEN_LED, LOW);  // Turn OFF green LED
    } 
    else if (incomingByte == 'C') {
      goalieServo.write(POS_CENTER);
      digitalWrite(RED_LED, LOW);    // Turn OFF both LEDs
      digitalWrite(GREEN_LED, LOW);
    } 
    else if (incomingByte == 'R') {
      goalieServo.write(POS_RIGHT);
      digitalWrite(RED_LED, LOW);    // Turn OFF red LED
      digitalWrite(GREEN_LED, HIGH); // Turn ON green LED
    }
  }
}