const int temperaturePin = A0;  // Analog pin for temperature sensor
const int lightPin = A1;        // Analog pin for light sensor

void setup() {
  Serial.begin(9600);  // Start serial communication at 9600 baud
}

void loop() {
  int temperatureReading = analogRead(temperaturePin);
  int lightReading = analogRead(lightPin);
  
  Serial.print("Temperature: ");
  Serial.print(temperatureReading);
  Serial.print(", Light: ");
  Serial.println(lightReading);
  
  delay(1000);  // Wait for a second before the next reading
}
