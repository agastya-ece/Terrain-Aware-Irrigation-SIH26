
#include <Arduino.h>

#define SOIL_PIN 2
#define LED_PIN 4

#define DRY_THRESHOLD 1400
#define WET_THRESHOLD 1200

bool watering = false;

void setup() {
    Serial.begin(115200);

    pinMode(LED_PIN, OUTPUT);
    digitalWrite(LED_PIN, LOW);

    Serial.println("Soil Moisture System");
}

void loop() {

    int soilValue = analogRead(SOIL_PIN);

    Serial.print("Soil ADC: ");
    Serial.print(soilValue);

    // Soil is dry → watering state ON → LED ON
    if (!watering && soilValue > DRY_THRESHOLD) {
        watering = true;
        digitalWrite(LED_PIN, HIGH);

        Serial.println(" -> DRY | WATERING ON");
    }

    // Soil is wet → watering state OFF → LED OFF
    else if (watering && soilValue < WET_THRESHOLD) {
        watering = false;
        digitalWrite(LED_PIN, LOW);

        Serial.println(" -> WET | WATERING OFF");
    }

    // Between thresholds
    else if (soilValue >= WET_THRESHOLD && soilValue <= DRY_THRESHOLD) {
        Serial.println(" -> MOIST | MONITORING");
    }

    else {
        Serial.println();
    }

    delay(1000);
}

