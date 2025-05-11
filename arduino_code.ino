#include <ESP32Servo.h>

// --- IMPORTANT: Define GPIO Pins Used ---
// !!! REPLACE 0 WITH ACTUAL GPIO NUMBERS YOU CONNECTED !!!
#define BASE_SERVO_PIN      2  // GPIO pin for Base servo (MG90S)
#define SHOULDER_SERVO_PIN  12  // GPIO pin for Shoulder servo (MG995)
#define ELBOW_SERVO_PIN     13  // GPIO pin for Elbow servo (MG995)

// --- Servo Objects ---
Servo baseServo;
Servo shoulderServo;
Servo elbowServo;

// --- Servo Configuration ---
// Pulse widths might need tuning for your specific servos (500-2500us often works well)
const int minUs = 500;
const int maxUs = 2500;
// Angle limits (degrees) - sanity check, main clamping done in Python
const int SERVO_MIN_DEG = 0;
const int SERVO_MAX_DEG = 180;

// --- Initial/Reset Angles (Degrees) ---
// Derived from URDF mapping in Python script description
const int INITIAL_BASE_DEG = 90;
const int INITIAL_SHOULDER_DEG = 45;
const int INITIAL_ELBOW_DEG = 180;

// --- Serial Communication ---
const long SERIAL_BAUD_RATE = 115200;
String serialBuffer = ""; // Buffer to hold incoming serial data

void setup() {
  Serial.begin(SERIAL_BAUD_RATE);
  serialBuffer.reserve(100); // Reserve space for incoming commands
  Serial.println("\nESP32 Servo Controller Initializing...");

  // Verify Pin Definitions
  if (BASE_SERVO_PIN == 0 || SHOULDER_SERVO_PIN == 0 || ELBOW_SERVO_PIN == 0) {
      Serial.println("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
      Serial.println("ERROR: Servo GPIO pins not defined! Edit the code.");
      Serial.println("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
      while(1) delay(1000); // Halt execution
  }
   Serial.print("Base Pin: "); Serial.println(BASE_SERVO_PIN);
   Serial.print("Shoulder Pin: "); Serial.println(SHOULDER_SERVO_PIN);
   Serial.print("Elbow Pin: "); Serial.println(ELBOW_SERVO_PIN);


  // Allow allocation of all timers for ESP32Servo library
  ESP32PWM::allocateTimer(0);
	ESP32PWM::allocateTimer(1);
	ESP32PWM::allocateTimer(2);
	ESP32PWM::allocateTimer(3);

  // Attach servos to specified pins and pulse widths
  baseServo.attach(BASE_SERVO_PIN, minUs, maxUs);
  shoulderServo.attach(SHOULDER_SERVO_PIN, minUs, maxUs);
  elbowServo.attach(ELBOW_SERVO_PIN, minUs, maxUs);
  Serial.println("Servos Attached.");

  // Move servos to initial position on startup
  Serial.println("Moving servos to initial position...");
  baseServo.write(INITIAL_BASE_DEG);
  shoulderServo.write(INITIAL_SHOULDER_DEG);
  elbowServo.write(INITIAL_ELBOW_DEG);
  delay(1000); // Give servos time to reach initial position

  Serial.println("Setup Complete. Waiting for commands...");
  Serial.println("---------------------------------------");
}

void loop() {
  // Check for incoming serial data
  while (Serial.available() > 0) {
    char receivedChar = Serial.read();
    serialBuffer += receivedChar;

    // Process buffer when newline character is received
    if (receivedChar == '\n') {
      serialBuffer.trim(); // Remove newline and any whitespace
      //Serial.print("Raw Command Received: ["); Serial.print(serialBuffer); Serial.println("]"); // Debug raw input

      // Parse command like "S0:angle0,S1:angle1,S2:angle2"
      int s0_val = -1, s1_val = -1, s2_val = -1; // Use -1 to indicate not found

      char cmdBuffer[100]; // Buffer to hold command copy
      serialBuffer.toCharArray(cmdBuffer, sizeof(cmdBuffer));

      char* token = strtok(cmdBuffer, ","); // Split by comma

      while (token != NULL) {
          String part = String(token);
          part.trim();

          if (part.startsWith("S0:")) {
              s0_val = part.substring(3).toInt();
          } else if (part.startsWith("S1:")) {
              s1_val = part.substring(3).toInt();
          } else if (part.startsWith("S2:")) {
              s2_val = part.substring(3).toInt();
          }
          token = strtok(NULL, ","); // Get next token
      }

      // Check if all values were parsed successfully
      if (s0_val != -1 && s1_val != -1 && s2_val != -1) {
        // Clamp values received (Safety check on ESP32 side)
        s0_val = constrain(s0_val, SERVO_MIN_DEG, SERVO_MAX_DEG);
        s1_val = constrain(s1_val, SERVO_MIN_DEG, SERVO_MAX_DEG); // Note: Python clamps shoulder more tightly
        s2_val = constrain(s2_val, SERVO_MIN_DEG, SERVO_MAX_DEG);

        // Write angles to servos
        baseServo.write(s0_val);
        shoulderServo.write(s1_val);
        elbowServo.write(s2_val);

        // Optional: Print parsed angles for debugging
        // Serial.print("Executing Angles -> Base:"); Serial.print(s0_val);
        // Serial.print(" Shoulder:"); Serial.print(s1_val);
        // Serial.print(" Elbow:"); Serial.println(s2_val);

      } else {
          Serial.print("Error parsing command: ["); Serial.print(serialBuffer); Serial.println("]");
      }

      // Clear the buffer for the next command
      serialBuffer = "";
    } // end if newline received
  } // end while Serial.available
} // end loop
