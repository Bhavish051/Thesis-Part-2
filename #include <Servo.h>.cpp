#include <Servo.h>
#include <Adafruit_NeoPixel.h>

#define SERVO_PIN1 10
#define SERVO_PIN2 11
#define DELAYVAL 200
#define PIN       12
#define NUMPIXELS 59
unsigned long servo1Time;
unsigned long servo2Time;


Servo servo1;
Servo servo2;
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  servo1.attach(SERVO_PIN1);
  servo2.attach(SERVO_PIN2);

  pixels.begin();
  servo1Time = millis() + 1000;
  servo2Time = servo1Time + 1000;
  servo1.write(0);
  servo2.write(0);
}

void loop() {
    pixels.clear();  
       
    for(int i=0; i<NUMPIXELS; i++) {
        pixels.setPixelColor(i, pixels.Color(200, 0, 0));
        pixels.show();
        delay(DELAYVAL);
    }
  
  if (servo1Time = millis()) { //Servo 1 rise
    servo1.write(90);
    pixels.clear();  
       
    for(int i=0; i<NUMPIXELS; i++) {
        pixels.setPixelColor(i, pixels.Color(0, 200, 0));
        pixels.show();
        delay(DELAYVAL);
    }
  }
  if (servo1Time = millis() + 500) { //Servo 1 fall
    servo1.write(0);
    servo1Time = +2000;
  }
  if (servo2Time = millis()) { //Servo 2 rise
    servo2.write(90);
    pixels.clear();  
       
    for(int i=0; i<NUMPIXELS; i++) {
        pixels.setPixelColor(i, pixels.Color(0, 200, 0));
        pixels.show();
        delay(DELAYVAL);
    }
  }
  if (servo2Time = millis() + 500) { //Servo 2 fall
    servo2.write(0);
    servo2Time = +2000;
  }
}