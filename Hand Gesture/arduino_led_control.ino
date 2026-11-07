// ============================================================
// DLD Lab Project - Hand Gesture LED Control
// 2nd Semester - Digital Logic Design
//
// Receives finger count (0-5) from Python via Serial
// and lights up corresponding number of LEDs
//
// Wiring:
//   LED 1 --> 220Ω --> Pin 2 --> GND
//   LED 2 --> 220Ω --> Pin 3 --> GND
//   LED 3 --> 220Ω --> Pin 4 --> GND
//   LED 4 --> 220Ω --> Pin 5 --> GND
//   LED 5 --> 220Ω --> Pin 6 --> GND
// ============================================================

const int ledPins[] = {2, 3, 4, 5, 6};  // Arduino pins for 5 LEDs
const int numLEDs = 5;

void setup() {
  Serial.begin(9600);  // Must match Python script baud rate

  for (int i = 0; i < numLEDs; i++) {
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW);  // All LEDs OFF at start
  }

  // Startup test: blink all LEDs once
  for (int i = 0; i < numLEDs; i++) digitalWrite(ledPins[i], HIGH);
  delay(500);
  for (int i = 0; i < numLEDs; i++) digitalWrite(ledPins[i], LOW);
}

void loop() {
  if (Serial.available() > 0) {
    char received = Serial.read();

    // Ignore newline / carriage return characters
    if (received == '\n' || received == '\r') return;

    int count = received - '0';  // Convert ASCII char to integer

    // Safety check: valid range is 0-5
    if (count < 0 || count > 5) return;

    // Turn ON 'count' LEDs, turn OFF the rest
    for (int i = 0; i < numLEDs; i++) {
      digitalWrite(ledPins[i], i < count ? HIGH : LOW);
    }
  }
}
