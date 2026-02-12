const int ledRed = 2;    // Left Goalie
const int ledGreen = 4;  // Right Goalie

char incomingByte;

void setup() {
  Serial.begin(9600);
  pinMode(ledRed, OUTPUT);
  pinMode(ledGreen, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    incomingByte = Serial.read();

    // Reset both to OFF initiall
    digitalWrite(ledRed, LOW);
    digitalWrite(ledGreen, LOW);

    if (incomingByte == 'L') {
      // GOALIE MOVES LEFT
      digitalWrite(ledRed, HIGH);
    } 
    else if (incomingByte == 'C') {
      // GOALIE STAYS CENTER (Both lights on)
      digitalWrite(ledRed, HIGH);
      digitalWrite(ledGreen, HIGH);
    } 
    else if (incomingByte == 'R') {
      // GOALIE MOVES RIGHT
      digitalWrite(ledGreen, HIGH);
    }
  }
}