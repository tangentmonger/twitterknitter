//Code for automated knitting machine.

//USB serial comms.
//Connect grounds with external power supply.
//Servo data on pins 22-45.
//Data LED on digital 2
//Knitting LED on digital 3
//Carriage sense on digital 4

#include <Servo.h>

const int NSERVOS = 24;
const int FIRST_SERVO_PIN = 22; 
Servo Servos[NSERVOS]; 

const int REDLED = 53;
const int YELLOWLED = 52;
const int GREENLED = 51;
const int BUTTON = 50;

int nRows = 0;
byte * pattern;

const int upLocations[] = {30, 155, 30, 155, 30, 155, 30, 155, 30, 155, 30, 155, 155, 30, 155, 30, 155, 30, 155, 30, 155, 30, 155, 30};
const int downLocations[] = {100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100 };


void setup() {
    
    
    for( int i =0; i < NSERVOS; i++) {
        Servos[i].attach(FIRST_SERVO_PIN + i);
        Servos[i].write(downLocations[i]);
        delay(200);
    }

  
  pinMode(REDLED, OUTPUT); //waiting
  pinMode(YELLOWLED, OUTPUT); //data
  pinMode(GREENLED, OUTPUT); //knitting
  pinMode(BUTTON, INPUT); //carriage sense
  pinMode(13, OUTPUT); //arduino LED      

  digitalWrite(2, LOW);
  digitalWrite(3, LOW);
}
 
 void react() {
    for(int i=0;i<1;i++){
        Servos[1].write(155);
        delay(200);
        Servos[1].write(100);
        delay(200);
        }
       }



void loop() {
  while(true) {
        getPattern();
       doKnitting();
    }
/*
   
    while(true) {
       testServos();
   }
*/
    
}

void testServos() {
    digitalWrite(REDLED, HIGH);
   
    delay(500);
    for(int i=0; i<NSERVOS; i++) {
        setServo(i, true);
        delay(150);
    }
    digitalWrite(REDLED, LOW);
    
    while(digitalRead(BUTTON) ==0) {}
    delay(500);
    while(digitalRead(BUTTON) == 0) {}
    

    digitalWrite(REDLED, HIGH);
    delay(500);
    for(int i=0; i<NSERVOS; i++) {
        setServo(i, false);
        delay(150);
    }
    digitalWrite(REDLED, LOW);
    
    while(digitalRead(BUTTON) ==0) {}
    delay(500);
    while(digitalRead(BUTTON) == 0) {}


}

void getPattern() {
    //light on  
    digitalWrite(REDLED, HIGH);
    digitalWrite(13, HIGH);
   


    //connect serial
    Serial.begin(9600); 
    
    while(Serial.available() == 0) {
        delay(100);
    }

    digitalWrite(REDLED, LOW);
    digitalWrite(YELLOWLED, HIGH);
   //read length of pattern, in rows

    nRows = Serial.read();
    //prepare buffer
    pattern = (byte*) malloc(sizeof(byte) * nRows * 3);

    Serial.readBytes((char*)pattern, nRows * 3); //readBytes doesn't take byte* ???

    //light off
    digitalWrite(YELLOWLED, LOW);
    digitalWrite(13, LOW);

    Serial.end();

}



int myPow(int x, int p) {
  if (p == 0) return 1;
    if (p == 1) return x;
      return x * myPow(x, p-1);
      }

void doKnitting() {
    //light on
    digitalWrite(GREENLED, HIGH);

    int get =0;
    for(int i=0; i<nRows; i++) {
        if(i % 10 == 0) {
            digitalWrite(YELLOWLED,HIGH);
        } else {
            digitalWrite(YELLOWLED,LOW);
        }
        digitalWrite(REDLED, HIGH);

        //assumption: servo 0 is on the right
        //unpack and set servos for row
        //LSByte first
        for(int group=0; group<3; group++) {
            for(int bit=0; bit<8; bit++) {
                setServo((group*8) + bit, bool(pattern[get] & (myPow(2,bit))));
                delay(100);
            }
            get++;
        }

        digitalWrite(REDLED, LOW);
        //wait for carriage
        while(digitalRead(BUTTON) == 0) {}

        delay(500);

        //may need debouncing here
    }

    //tidy up
    free(pattern);
    digitalWrite(GREENLED, LOW);
}


void setServo(int servo, bool up) {
    if(up) {
        Servos[servo].write(upLocations[servo]);
    } else {
        Servos[servo].write(downLocations[servo]);
    }

    //smarter version: only change it if it needs changing? might not matter
}
