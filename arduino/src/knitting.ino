//Code for automated knitting machine.

//USB serial comms.
//Connect grounds with external power supply.
//Servo data on pins 22-45.
//Data LED on digital 2
//Knitting LED on digital 3
//Carriage sense on digital 4

//Lights:
//Red: no data
//Amber: data, moving servos
//Green: knit


#include <Servo.h>

const int NSERVOS = 24;
const int FIRST_SERVO_PIN = 22; 
Servo Servos[NSERVOS]; 

const int REDLED = 53;
const int YELLOWLED = 52;
const int GREENLED = 51;
const int BUTTON = 50;

bool currentServos[NSERVOS];
bool nextServos[NSERVOS];

const int upLocations[] = {30, 155, 30, 155, 30, 155, 30, 155, 30, 155, 30, 155, 155, 30, 155, 30, 155, 30, 155, 30, 155, 30, 155, 30};
const int downLocations[] = {100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100 };


void setup() {
    pinMode(REDLED, OUTPUT); //waiting for data
    pinMode(YELLOWLED, OUTPUT); //got data, setting pattern
    pinMode(GREENLED, OUTPUT); //ok to knit
    pinMode(BUTTON, INPUT); //carriage sense
    
    Serial.begin(9600); 
  
    for(int i=0; i<NSERVOS; i++) {
        Servos[i].attach(FIRST_SERVO_PIN + i);
    }
    
    byte* pattern = (byte*) malloc(sizeof(byte) * 3);
    
    pattern[0] = 0x00;
    pattern[1] = 0x00;
    pattern[2] = 0x00;
    setPattern(pattern);
 
    pattern[0] = 0xFF;
    pattern[1] = 0xFF;
    pattern[2] = 0xFF;
    setPattern(pattern);

    free(pattern);
    
  }

void loop() {
    while(true) {
        byte* pattern = (byte*) malloc(sizeof(byte) * 3);
        getData(pattern);
        setPattern(pattern);
        doKnitting();
        free(pattern);
    }

    /*
    while(true) {
        testServos();
    }
    */
}

void getData(byte* pattern) {
    digitalWrite(REDLED, HIGH);
    digitalWrite(YELLOWLED, LOW);
    digitalWrite(GREENLED, LOW);

    //get pattern
    while(Serial.available() < 3) {}
    Serial.readBytes((char*)pattern, 3); //readBytes doesn't take byte* ???

    //ack
    Serial.print((byte)0);
}

void setPattern(byte* pattern) {
    digitalWrite(REDLED, LOW);
    digitalWrite(YELLOWLED, HIGH);
    digitalWrite(GREENLED, LOW);
    
    for(int group=0; group<3; group++) {
        for(int bit=0; bit<8; bit++) {
            setServo((group*8) + bit, bool(pattern[group] & (1 << bit)));
        }
    }
    
    moveServos();
}

void doKnitting() {
    digitalWrite(REDLED, LOW);
    digitalWrite(YELLOWLED, LOW);
    digitalWrite(GREENLED, HIGH);

    //wait for carriage
    while(digitalRead(BUTTON) == 0) {}

    //debounce
    delay(500);
}



void setServo(int servo, bool up) {
    //record the next setting for this servo
    nextServos[servo] = up;
}

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

    //actually do the move as efficiently as possible
    int numberAtOnce = 3; //more at once = more current draw
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

//test pattern: alternating stripes in blocks of two
void testServos() {
    byte* pattern = (byte*) malloc(sizeof(byte) * 3);
    
    pattern[0] = 0x00;
    pattern[1] = 0x00;
    pattern[2] = 0x00;
    
    setPattern(pattern);
    doKnitting();
    doKnitting();
 
    pattern[0] = 0xFF;
    pattern[1] = 0xFF;
    pattern[2] = 0xFF;
    
    setPattern(pattern);
    doKnitting();
    doKnitting();

    free(pattern);
}
