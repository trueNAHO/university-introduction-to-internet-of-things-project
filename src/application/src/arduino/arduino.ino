#include <math.h>

const int B = 4275; // B value of the thermistor
const int R0 = 100000; // R0 = 100k
const String BOARD_ID = "Room1";  // Unique identifier for this Arduino

unsigned long lastUpdate = 0; // Track last update time

void setup() {
  Serial.begin(9600);
}

int compute_temperature(int sensor) {
  float R = 1023.0 / sensor - 1.0;
  R = R0 * R;
  return (1.0 / (log(R / R0) / B + 1 / 298.15)) - 273.15; // Convert to °C
}

int compute_sound(int sensor) {
  long sum = 0;
  for (int i = 0; i < 32; i++) {
    sum += sensor;
  }
  return sum >> 5; // Averaging
}

void loop() {
  if (millis() - lastUpdate >= 30000) {  // Check if 10 seconds have passed
    lastUpdate = millis();  // Update the last run time

    int potentiometer = analogRead(A1);
    int sound = compute_sound(analogRead(A0));
    int light = analogRead(A3);
    int temp = compute_temperature(analogRead(A2));

    // Print each sensor data in "Room_ID/sensor:value" format
    //Serial.print(BOARD_ID);
    //Serial.print("/sensor/potentiometer:");
    //Serial.println(potentiometer);
    
    Serial.print(BOARD_ID);
    Serial.print("/sensor/Sound:");
    Serial.println(sound);

    Serial.print(BOARD_ID);
    Serial.print("/sensor/Light_Intensity:");
    Serial.println(light);

    Serial.print(BOARD_ID);
    Serial.print("/sensor/Temperature:");
    Serial.println(temp);

    Serial.flush(); // Ensure all data is sent
  }
}
