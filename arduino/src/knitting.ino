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

bool currentServos[NSERVOS];
bool nextServos[NSERVOS];


const int upLocations[] = {30, 155, 30, 155, 30, 155, 30, 155, 30, 155, 30, 155, 155, 30, 155, 30, 155, 30, 155, 30, 155, 30, 155, 30};
const int downLocations[] = {100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100 };


void setup() {


    for( int i =0; i < NSERVOS; i++) {
        Servos[i].attach(FIRST_SERVO_PIN + i);
        Servos[i].write(downLocations[i]);
        currentServos[i] = false;
        nextServos[i] = false;
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



    /*    while(true) {
          testServos();
          }
     */

}

//test pattern: alternating stripes in blocks of two
void testServos() {
    digitalWrite(REDLED, HIGH);

    delay(500);
    for(int i=0; i<NSERVOS; i++) {
        setServo(i, true);
    }
    moveServos();
    digitalWrite(REDLED, LOW);

    while(digitalRead(BUTTON) ==0) {}
    delay(500);
    while(digitalRead(BUTTON) == 0) {}


    digitalWrite(REDLED, HIGH);
    delay(500);
    for(int i=0; i<NSERVOS; i++) {
        setServo(i, false);
    }
    moveServos();
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
                setServo((group*8) + bit, bool(pattern[get] & (1 << bit)));
            }
            get++;
        }
        moveServos();

        digitalWrite(REDLED, LOW);
        //wait for carriage
        while(digitalRead(BUTTON) == 0) {}

        //debounce
        delay(500);
    }

    //tidy up
    free(pattern);
    digitalWrite(GREENLED, LOW);
}

void setServo(int servo, bool up) {
    //record the next setting for this servo
    nextServos[servo] = up;
}

//actually do the move as efficiently as possible
void moveServos() {
    //make list of servos that need moving
    int toMove[NSERVOS];
    int numberToMove;
    numberToMove = 0;

    for(int i=0;i<NSERVOS;i++) {
        if (currentServos[i] != nextServos[i]) {
            toMove[numberToMove] = i;
            numberToMove++;
            currentServos[i] = nextServos[i];
        }
    }

    int numberAtOnce = 3;
    int count = 0;
    for(int i=0; i<numberToMove; i++) {
        if(nextServos[toMove[i]]) {
            Servos[toMove[i]].write(upLocations[toMove[i]]);
        } else {
            Servos[toMove[i]].write(downLocations[toMove[i]]);
        }
        count++;
        if (count == numberAtOnce) {
            count = 0;
            delay(100);
        }
    }

}
