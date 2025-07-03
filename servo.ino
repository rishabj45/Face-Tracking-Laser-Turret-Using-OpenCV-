#include <Servo.h>

// Define pin numbers
const int laserPin = 10;     // Pin for laser control
const int servoXPin = 9;     // Pin for horizontal (X-axis) servo
const int servoYPin = 11;    // Pin for vertical (Y-axis) servo

// Create servo objects
Servo servoX;
Servo servoY;

// Variables to manage laser timing
unsigned long laserOffTime = 0;  // Time when laser should turn off

void setup() {
    Serial.begin(9600);               // Initialize serial communication
    servoX.attach(servoXPin);          // Attach horizontal servo
    servoY.attach(servoYPin);          // Attach vertical servo
    pinMode(laserPin, OUTPUT);         // Set laser pin as output
    digitalWrite(laserPin, LOW);       // Laser off initially

    // Center servos at startup
    servoX.write(90);
    servoY.write(100);
    Serial.println("Setup complete.");
}

void loop() {
    // 1) Read incoming serial data
    if (Serial.available()) {
        String input = Serial.readStringUntil('\n');
        input.trim();  // Clean any extra whitespace

        Serial.println("Received: " + input);  // Debug print

        int commaIndex = input.indexOf(',');
        if (commaIndex > 0) {
            int centerX = input.substring(0, commaIndex).toInt();
            int centerY = input.substring(commaIndex + 1).toInt();

            if (centerX == 0 && centerY == 0) {
                //digitalWrite(laserPin, LOW);
                servoX.write(90);   // Center position
                servoY.write(100);  // Center position
                Serial.println("No face detected: Centering servos.");
            } else {
                int posX = map(centerX, 0, 640, 126, 54);
                int posY = map(centerY, 0, 480, 135, 72);

                // Clamp values to servo range (optional, but safe)
                //posX = constrain(posX, 0, 180);
                //posY = constrain(posY, 0, 180);

                servoX.write(posX);
                servoY.write(posY);
                digitalWrite(laserPin, HIGH);

                laserOffTime = millis() + 1000;  // Keep laser on for 1 second

                Serial.print("Aiming at X:");
                Serial.print(posX);
                Serial.print(" Y:");
                Serial.println(posY);
            }
        }
    }

    // 2) Turn off the laser after 1 second
   
    

    // 3) Heartbeat to show the loop is running
    //Serial.println("Loop tick");
    delay(500);  // Small delay to avoid flooding serial output
}
