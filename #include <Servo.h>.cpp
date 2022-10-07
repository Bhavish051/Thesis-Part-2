#include <Servo.h>
#include <Adafruit_NeoPixel.h>
#include <IRremote.h>     
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN        13
#define NUMPIXELS 16
#define DELAYVAL 500
decode_results results;
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
const int RECV_PIN = 2;                                       // IR pin
IRrecv irrecv(RECV_PIN);  

int Rled = 10;

int Pbtn = 2;
int Pbtn2 = 7;

int btnst;// = 0;
int btnst2;

int servoPin = 5;
int servoPin2 = 8;

Servo servo1;
Servo servo2;

int ledbtn1 = 12;
int ledbtn2 = 11;

int ledbtnst1;
int ledbtnst2;

int ledStrip = 13;

double angle;

void setup()
{
  Serial.begin(9600);
  pinMode(Rled, OUTPUT);

  pinMode(Pbtn, INPUT);
  pinMode(Pbtn2, INPUT);
  
  servo1.attach(servoPin);
  servo2.attach(servoPin2);
  
  pinMode(ledbtn1, INPUT);
  pinMode(ledbtn2, INPUT);

 IrReceiver.begin(2); 
  #if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  		clock_prescale_set(clock_div_1);
  #endif
attachInterrupt(digitalPinToInterrupt(2), DecodeIR, FALLING); 
  pixels.begin();
}

void loop()
{
 pixels.clear();  
//  btnst = digitalRead(Pbtn);
  btnst2 = digitalRead(Pbtn2);
  
  ledbtnst1 = digitalRead(ledbtn1);
  ledbtnst2 = digitalRead(ledbtn2);

  /*
if (btnst == HIGH) {
    //digitalWrite(Rled, HIGH);
  	angle =0;
    delay(200);
    //digitalWrite(Rled, LOW);
  	angle =90;
  	servo1.write(90);
    
   } else {
  servo1.write(0);
  angle = 0;
  digitalWrite (Rled, LOW);    
  }
  */

 	if(btnst2 == HIGH){
   		digitalWrite(Rled, HIGH);
   			 delay(1000);
    digitalWrite(Rled, LOW);
  	servo2.write(90);
    
 	 }
  
  else {
  servo2.write(0);
  angle = 0;
  digitalWrite (Rled, LOW);    
  }
  if (ledbtnst1 == HIGH) {
  	// Start LED Strip	
	for(int i=0; i<NUMPIXELS; i++) {
		pixels.setPixelColor(i, pixels.Color(0, 150, 0));
	    pixels.show();
    }
  } 
  if (ledbtnst2 == HIGH) {
    // Stop LED Strip	
  	for(int i=0; i<NUMPIXELS; i++) {
		pixels.setPixelColor(i, pixels.Color(150, 0, 0));
	    pixels.show();
    }
  }
}

void DecodeIR() {
	Serial.println("In Decode");
//  	Serial.println(&results);
  if (irrecv.decode(&results)) {  
      	Serial.println(results.decode_type);
    // Get the make of the signal
    switch (results.decode_type) {
      case HIGH: 
      		Serial.println("Signal type: HIGH"); 
      		angle =0;
	    	digitalWrite(Rled, LOW);
	  		angle =90;
	  		servo1.write(90);
      		break ;
      //
    }
    irrecv.resume();
  }
}