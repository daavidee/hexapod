#include <NewPing.h> // using NewPing library by Tim Eckel
#include "RunningMedian.h" // taking median value of 3 ultrasonic read attempts. default one in NewPing had some quirks
#include <Wire.h>

//NewPing defines
#define TRIGGER_PIN  7  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     8  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 255 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

RunningMedian samples = RunningMedian(3); // median sample var
int objectDistance = -1; // object distance in cm. -1 is a default value before any ping is performed
boolean isPerformingPing = false; // flag to execute a ping set by onReceive ISR

void setup() {
  Wire.begin(4);                  // join i2c bus with address #4
  Wire.onReceive(processReceive); // ISR to call on a receive
  Wire.onRequest(processRequest); // ISR to call on a request
  //Serial.begin(115200);           // start serial for debugging output
}

void loop() {
  if (isPerformingPing) {
    executePing();
  }
}

// ISR for receive
void processReceive(int dataSize)
{
  objectDistance = -1; // reset value
  int regNum = Wire.read(); // register number
  while(0 < Wire.available()) Wire.read(); // dump any other data
  if (regNum == 1) isPerformingPing = true; // if register 1, set flag to perform ping. will be performed in main loop
}

// ISR for request. any request returns the ping distance in cm
void processRequest() {
  if ((isPerformingPing) || (objectDistance == -1)) return;
  Wire.write(getDistance());
}

// distance measuring function
void executePing() {
  int i = 1;
  while(i <= 3){                    // perform 3 measurements and get a median....sometimes there is a bad measurement
    unsigned int uS = sonar.ping(); // Send ping, get ping time in microseconds (uS).
    samples.add(uS);
    if (i == 3) break;
    delay(20);                      // Wait 20ms between pings, dont wait after last one. (servo to move between pings anyways)
    i++;
  }
  int tmp = int(samples.getMedian() / US_ROUNDTRIP_CM);
  if (tmp > 255) tmp = 255;
  if (tmp == 0) tmp = 1;
  objectDistance = tmp;
  
  //Serial.print("Ping: ");
  //Serial.print(tmp);
  //Serial.println("cm");
  
  isPerformingPing = false;
}

int getDistance() {
  int res = objectDistance;
  objectDistance = -1;
  return res;
}
