// Sensor and Actuator Pins
const int LDRPin = A0;       // Light sensor (photoresistor)
const int tiltPin = 2;       // Tilt switch
const int buzzerPin = 3;     // Buzzer
const int redPin = 9;        // RGB LED Red
const int greenPin = 10;     // RGB LED Green (Used for blink rate)
const int bluePin = 11;      // RGB LED Blue

// Timing variables
unsigned long previousMillis = 0;
unsigned long buzzerMillis = 0;
int blinkInterval = 1000;  // Default blink rate for green LED
bool ledState = false;
bool buzzerState = false;

// --- Alert Variables ---
const int alertThreshold = 350;  // LOWERED from 200 to 100 for better sensitivity
bool alertSent = false;

// --- Function to Smooth Readings (Takes 5 Samples) ---
int getSmoothedLightValue() {
    int total = 0;
    int numSamples = 5;
    for (int i = 0; i < numSamples; i++) {
        total += analogRead(LDRPin);
        delay(10);  // Short delay between samples
    }
    return total / numSamples;  // Return average
}

void setup() {
    Serial.begin(115200);  // Increase baud rate from 9600 to 115200

    
    pinMode(LDRPin, INPUT);
    pinMode(tiltPin, INPUT_PULLUP);
    pinMode(buzzerPin, OUTPUT);
    
    pinMode(redPin, OUTPUT);
    pinMode(greenPin, OUTPUT);
    pinMode(bluePin, OUTPUT);
}

void loop() {
    unsigned long currentMillis = millis();
    
    // Read smoothed sensor value
    int lightValue = getSmoothedLightValue();
    int tiltState = digitalRead(tiltPin);

    // **More Reactive RGB LED Color Mapping**
    int redValue = map(lightValue, 0, 1023, 255, 20);   // Dark = More Red, Bright = Less Red
    int blueValue = map(lightValue, 0, 1023, 20, 255);  // Dark = Less Blue, Bright = More Blue
    redValue = constrain(redValue, 0, 255);
    blueValue = constrain(blueValue, 0, 255);

    // **Tilt Switch Controls Green LED Blink Rate**
    blinkInterval = (tiltState == HIGH) ? 200 : 1000;

    // **Blinking LED Logic (Green)**
    if (currentMillis - previousMillis >= blinkInterval) {
        previousMillis = currentMillis;
        ledState = !ledState;
        digitalWrite(greenPin, ledState ? HIGH : LOW);
    }

    // **Buzzer and Serial Alert Logic (More Sensitive to Light)**
    if (lightValue > alertThreshold) {  // Now detects very small light changes
        if (!alertSent) {
            Serial.println("LIGHT_DETECTED");
            alertSent = true;
        }
        const int policeInterval = 150;  // Faster police siren effect
        if (currentMillis - buzzerMillis >= policeInterval) {
            buzzerMillis = currentMillis;
            tone(buzzerPin, buzzerState ? 1200 : 1600);
            buzzerState = !buzzerState;
        }
    } else {
        alertSent = false;
        noTone(buzzerPin);
        buzzerState = false;
    }

    // **Apply RGB LED Values**
    analogWrite(redPin, redValue);
    analogWrite(bluePin, blueValue);

    // **Debugging Output**
    Serial.print("Light Level: ");
    Serial.print(lightValue);
    Serial.print(" | Tilt State: ");
    Serial.print(tiltState);
    Serial.print(" | Red: ");
    Serial.print(redValue);
    Serial.print(" | Green Blink: ");
    Serial.print(ledState ? "ON" : "OFF");
    Serial.print(" | Blue: ");
    Serial.println(blueValue);

    delay(10);  // Short delay for stability
}
