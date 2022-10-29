#include <Servo.h>
#include <Adafruit_NeoPixel.h>
#include <IRremote.h>    
#ifdef __AVR__
  #include <avr/power.h>
#endif
#include <YetAnotherPcInt.h>
#define PIN        13
#define NUMPIXELS 16
#define DELAYVAL 500
#include <IRremote.h>

#define PCINT1_PIN 8
#define PCINT2_PIN 9

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
int RECV_PIN_1 = 3;
int RECV_PIN_2 = 4;
int RECV_PIN_3 = 12;
int RECV_PIN_4 = 13;
unsigned long PreviousMillis1=0;
unsigned long PreviousMillis2=0;
int led1 = 0;

IRrecv irrecv1(RECV_PIN_1);
IRrecv irrecv2(RECV_PIN_2);
IRrecv irrecv3(RECV_PIN_3);
IRrecv irrecv4(RECV_PIN_4);

decode_results results1;
decode_results results2;
decode_results results3;
decode_results results4;

int ballCounter = 0;

Servo servo1;
Servo servo2;


void setup()
{
  Serial.begin(9600);
  // In case the interrupt driver crashes on setup, give a clue
  // to the user what's going on.
  Serial.println("Enabling IRin");
  irrecv1.enableIRIn();
  irrecv2.enableIRIn();// Start the receiver
  irrecv3.enableIRIn();
  irrecv4.enableIRIn();
  Serial.println("Enabled IRin");
  servo1.attach(10);
  servo2.attach(11);
  servo1.write(0);
  servo2.write(0);
  #if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
      clock_prescale_set(clock_div_1);
  #endif
 // Servos
     PcInt::attachInterrupt(6, pin3Changed, "Pin 6 has changed to ", RISING);
     PcInt::attachInterrupt(7, pin4Changed, "Pin 7 has changed to ", RISING);

 // Leds
    pinMode(PCINT1_PIN, INPUT_PULLUP);
    pinMode(PCINT2_PIN, INPUT_PULLUP);

    PcInt::attachInterrupt(PCINT1_PIN, pin1Changed, "Pin 8 has changed to ", RISING);
    PcInt::attachInterrupt(PCINT2_PIN, pin2Changed, "Pin 9 has changed to ", RISING);

   Serial.println("Setup Complete");
}


void loop() {

 
 // Close the servos after 1s
   if (millis()-PreviousMillis1>=1000) {
      servo1.write(0);
      PreviousMillis1 = 0;
  }
   if (millis()-PreviousMillis2>=1000) {
      servo2.write(0);
      PreviousMillis2 = 0;
  }
 }

void pin1Changed(const char* message, bool pinstate) {
  Serial.print(message);
  Serial.println(pinstate ? "HIGH" : "LOW");
}
void pin2Changed(const char* message, bool pinstate) {
  Serial.print(message);
  Serial.println(pinstate ? "HIGH" : "LOW");
}

void pin3Changed(const char* message, bool pinstate) {
  Serial.print(message);
  Serial.println(pinstate ? "HIGH" : "LOW");
        if (pinstate) {
          PreviousMillis1=millis();
          servo1.write(90);
          Serial.println("Opening the servo1"); 
        } 
}
void pin4Changed(const char* message, bool pinstate) {
  Serial.print(message);
  Serial.println(pinstate ? "HIGH" : "LOW");
       if (pinstate) {
          PreviousMillis2=millis();
          servo2.write(90);
          Serial.println("Opening the servo2"); 
        } 
}