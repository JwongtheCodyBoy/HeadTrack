#include <ArduinoJson.h>

const float FEET_TO_PIXELS = 1152.0;      //1 feet (AMERICA) == 1152 px       https://everythingfonts.com/font/tools/units/ft-to-px (No clue if this works) (But I think it does, so until proven wrong I am right I think)
const float DIST = 3.5 * FEET_TO_PIXELS;       

void setup() {
  // Initialize the serial communication
  Serial.begin(9600);
  while (!Serial) {
    ; // Wait for serial port to connect
  }
}

void loop() {
  // Check if data is available to read
  if (Serial.available()) {
    // Allocate a temporary JsonDocument
    DynamicJsonDocument doc(200);

    // Read the incoming JSON string
    String jsonString = Serial.readString();

    // Deserialize the JSON document
    DeserializationError error = deserializeJson(doc, jsonString);

    // Check if deserialization succeeded
    if (error) {
      Serial.print(F("deserializeJson() failed: "));
      Serial.println(error.f_str());
      return;
    }

    // Extract the values
    int xAim = doc["aimX"];
    int yAim = doc["aimY"];

    // Print the received data to the serial monitor
    Serial.print("Received data by Arduino - X: ");
    Serial.print(xAim);
    Serial.print(", Y: ");
    Serial.print(yAim);



    float xTheta = atan(xAim / DIST);
    float xDegrees = xTheta * 180.0 / PI;

    float yTheta = atan(yAim / DIST);
    float yDegrees = yTheta * 180.0 / PI;
    
    //Print Degrees of the aim calibrated at the DIST const
    char buffer[50];
    Serial.print("\t\t(X Degrees: ");
    Serial.print(xDegrees);
    Serial.print(", Y Degrees: ");
    Serial.print(yDegrees);
    Serial.println(")");
  }
}
