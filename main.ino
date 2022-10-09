/*
 * IRremote: IRrecvDemo - demonstrates receiving IR codes with IRrecv
 * An IR detector/demodulator must be connected to the input RECV_PIN.
 * Version 0.1 July, 2009
 * Copyright 2009 Ken Shirriff
 * http://arcfn.com
 */
#include <Servo.h>
#include <Adafruit_NeoPixel.h>
#include <IRremote.h>     
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN        13
#define NUMPIXELS 16
#define DELAYVAL 500
#include <IRremote.h>
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
int RECV_PIN_1 = 2;
int RECV_PIN_2 = 7;
int RECV_PIN_3 = 12;
int RECV_PIN_4 = 11;
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
  servo1.attach(5);
  servo2.attach(8);
  servo1.write(0);
  servo2.write(0);
  //pinMode(13,OUTPUT);
  //pinMode(0, OUTPUT);
  #if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  		clock_prescale_set(clock_div_1);
  #endif
 // Servos
   attachInterrupt(digitalPinToInterrupt(RECV_PIN_1), DecodeIR1, RISING); 
   attachInterrupt(digitalPinToInterrupt(RECV_PIN_2), DecodeIR2, RISING); 
 // LEDs
   attachInterrupt(digitalPinToInterrupt(RECV_PIN_3), DecodeIR3, CHANGE); 
   attachInterrupt(digitalPinToInterrupt(RECV_PIN_4), DecodeIR4, CHANGE); 
}


void loop() {
  
 // Close the servos after 1s
   if (millis()-PreviousMillis1>=1000) {
			servo1.write(0);
 	}
   if (millis()-PreviousMillis2>=1000) {
			servo2.write(0);
 	}
  
  //for sensor 1- left of stopping mechanism
	if (irrecv1.decode(&results1)) {
    //Serial.println(results1.value);//, DEC);
    if(results1.value == 16582903){
      Serial.println("Sensor1 activated");
     }
    //irrecv1.resume(); // Receive thxt value
  } 
  
  
  //for sensor 2 right of stopping mechanism
  if (irrecv2.decode(&results2)) {
    //Serial.println(results2.value);//, DEC);
    if(results2.value == 16615543){
      Serial.println("Sensor2 activated");
     }
    //irrecv2.resume(); // Receive thxt value
  }
  
  
//for sensor3 top of the box.  
   if (irrecv3.decode(&results3)) {
    //Serial.println(results3.value);//, DEC);
    if(results3.value == 16599223){
      Serial.println("Sensor3 activated");
     }
    //irrecv3.resume(); // Receive thxt value
  }
  
  
  //for sensor4 bottom of the box.  
   if (irrecv4.decode(&results4)) {
    //Serial.println(results4.value);//, DEC);
    if(results4.value == 16591063){
      Serial.println("Sensor4 activated");
     }
    irrecv4.resume(); // Receive thxt value
  }
 
	for(int i=0; i<NUMPIXELS; i++) {
		pixels.setPixelColor(i, pixels.Color(0, ballCounter*30, 0));
	    pixels.show();
    }
  
}

void DecodeIR1() {
	Serial.println("In Decode");
  
  Serial.println(irrecv1.decode(&results1));
  if (!irrecv1.decode(&results1)) {  
      Serial.println(results1.decode_type);	
    switch (results1.decode_type) {
      case 0: 
      PreviousMillis1=millis();
	  		servo1.write(90);
     // start timer
      // and then close
     
      //
    }
    irrecv1.resume();
  }
}

void DecodeIR2() {
	Serial.println("In Decode");
  
  Serial.println(irrecv2.decode(&results2));
  if (!irrecv2.decode(&results2)) {  
      Serial.println(results2.decode_type);	
    switch (results2.decode_type) {
      case 0: 
      PreviousMillis2=millis();

	  		servo1.write(90);
     // start timer
      // and then close
     
      //
    }
    irrecv2.resume();
  }
}

// Control the LEDs using the number of balls inside the box
void DecodeIR3() {
	Serial.println("In Decode 3");
  
  Serial.println(irrecv3.decode(&results3));
  if (!irrecv3.decode(&results3)) {  
      Serial.println(results3.decode_type);	
    switch (results3.decode_type) {
	  case 0:
      ballCounter++;
    }
    irrecv3.resume();
  }
}
void DecodeIR4() {
	Serial.println("In Decode 4");
  
  Serial.println(irrecv4.decode(&results4));
  if (!irrecv4.decode(&results4)) {  
      Serial.println(results4.decode_type);	
    switch (results4.decode_type) {
      case 0: 
      ballCounter--;
    }
    irrecv2.resume();
  }
}