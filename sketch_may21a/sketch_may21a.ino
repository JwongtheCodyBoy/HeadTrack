#include <ArduinoJson.h>
#include <Servo.h>
                                         //1 feet (AMERICA) == 456        I put a ruler infront of a camera and cropped the size 
const float FEET_TO_PIXELS = 456.0;      //1 feet (AMERICA) == 1152 px       https://everythingfonts.com/font/tools/units/ft-to-px (No clue if this works) (But I think it does, so until proven wrong I am right I think)
const float DIST = 1.8 * FEET_TO_PIXELS;       

Servo ServoX;
Servo ServoY;

int xServoPin = 9;      //(Black)
int yServoPin = 11;     //(White)

void setup() {
  ServoX.attach(xServoPin);   
  ServoY.attach(yServoPin);
  
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
//    if (xAim > 230)
//      xDegrees = xDegrees + 4;

    float yTheta = atan(yAim / DIST);
    float yDegrees = yTheta * 180.0 / PI;
//    yDegrees = yDegrees -3;
//      int xDegrees = map(xAim, 0, 720, -33, 62);
//      int yDegrees = map(yAim, 0, 480, 6, 65);
      
    //Print Degrees of the aim calibrated at the DIST const
    char buffer[50];
    Serial.print("\t\t(X Degrees: ");
    Serial.print(xDegrees);
    Serial.print(", Y Degrees: ");
    Serial.print(yDegrees);
    Serial.println(")");

    //Servo Foward will be the side that is closest to gears 
    ServoX.write(90-xDegrees);
    ServoY.write(yDegrees);
  }
}
