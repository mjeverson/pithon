/***************************************************
  Lucky Kitty Slot Machine MkII

  Designed for use with Arduino Mini pro 5V 16Hz && Associated Raspberry Pi 

  //todo(mje): Will we still need threads? Arduino mini pro threading?
  // This sets everything up then goes into waiting-for-serial
  // based on the code (loss, reset, victory-type) do all the things (in threads if necessary) and when done send a Done signal to the pi

 ****************************************************/

//#include <PWMServo.h> // Tentacle & Coin
#include <Servo.h> // Tentacle & Coin
#include <pt.h>   // include protothread library
#include <Adafruit_NeoPixel.h> // LED Stuff

// Solenoids
#define SOL1 2
#define SOL2 4
#define SOL3 7
#define SOL4 23

// Valid PWM pins: //3,5,6,9,10,11
#define TENTACLE_SERVO 8
#define COIN_SERVO 6
#define PIXEL 9
#define NUM_PIXELS 90
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_PIXELS, PIXEL, NEO_GRBW + NEO_KHZ800);

static struct pt pt1, pt2; // each protothread needs one of these

Servo tentacleServo;
Servo coinServo;  

#define WINSTATE_NONE 0
#define WINSTATE_NYAN 1
#define WINSTATE_TENTACLE 2
#define WINSTATE_COIN 3
#define WINSTATE_FIRE 4
#define WINSTATE_CHEESY 5
#define WINSTATE_PINCHY 6
#define WINSTATE_LOSS 7
#define WINSTATE_SETH 8
int winState;
int elapsedTime = 0; //testing only
// Get this party started!
void setup() {
  // Sets up the RNG
//  randomSeed(analogRead(A0));
  
  Serial.begin(9600);

  // Set up solenoid
  pinMode(SOL1, OUTPUT);
  pinMode(SOL2, OUTPUT);
  pinMode(SOL3, OUTPUT);
  pinMode(SOL4, OUTPUT);

  //Set up servos
  tentacleServo.attach(TENTACLE_SERVO);
//  coinServo.attach(COIN_SERVO);

  // Set up LEDs. Some default colour to indicate ready to go
  strip.begin();

  // initialise the two protothread variables
  PT_INIT(&pt1);  
  PT_INIT(&pt2);  

  // Initializes the state of the peripherals
  resetState();
  elapsedTime = millis(); //testing only
}


void loop() {
  Serial.flush();

  // schedule the two protothreads by calling them infinitely
  //todo:maybe keep intervals, and then every 10ms or so check to see if we need to update based on other stuff
  protothread1(&pt1); 
  protothread2(&pt2); 

//testcode
  if (millis() - elapsedTime < 5000) {
    if (activeTentacle != 1){ 
      activeTentacle = 1;
    }

    if (activeLights != 1){ 
      activeLights = 1;
    }
  } else {
    activeTentacle = 0;
    activeLights = 0;
    resetState();
  }
}

//todo:wait until we get a code from the pi. 
// Set the global winstate based on that, then doWinState with some small changes, followed by "done"
// There'll need to be an extra command for "dispense N coins"
//  if (Serial.available() > 0){
//    String data = Serial.readStringUntil('\n');
//    Serial.print("You sent me: ");
//    Serial.println(data);
//  }
}

//TODO: Set everything back to normal state for another round. are we missing anything?
void resetState(){
  // Reset the win state
  winState = WINSTATE_NONE;
  
  // Reset coin and tentacle servo positions
  tentacleServo.write(90);
//  coinServo.write(90);
  
  // reset LEDs
  doLights();

  // Make sure fire is off
//  doFire();
}

// Do the fire. Might need to swap to clock watching
void doFire(){
  switch (winState) {
    case WINSTATE_NYAN: 
      //1-2-3-4
      fireSequentialThread(false);
      fireSequentialThread(true);
      break;
    case WINSTATE_TENTACLE:
      // all at once
      fireAllThread();
      break;
    case WINSTATE_COIN:
      // fire: 1-3-2-4-all
      fireSequential(false);
      fireAll();
      break;
    case WINSTATE_FIRE:
      //fire all three at "highway to hell"
      //1s-5s-9s-13s for "highway to hell"
      //each fireAll takes about 2250ms
      
      for (int i = 0; i< 3; i++){
          fireAll();
      }

      delay(2500);

      for (int i = 0; i< 3; i++){
          fireAll();
      }

      delay(2000);

      for (int i = 0; i< 3; i++){
          fireAll();
      }

      delay(2000);

      fireAll();
      
      break;
    case WINSTATE_CHEESY:
      // No fire
      fireOff();
      break;
    case WINSTATE_PINCHY:
      // fire all 4
      fireAll();
      break;
    case WINSTATE_SETH:
      //1-2-3-4
      fireSequentialThread(false);
      fireSequentialThread(true);
      break;
    default:
      // No fire
      fireOff();
      break;
  }
}

// Triggers all four solenoids with thread delay
void fireAllThread(){
  digitalWrite(SOL1, HIGH);
  digitalWrite(SOL2, HIGH);
  digitalWrite(SOL3, HIGH);
  digitalWrite(SOL4, HIGH);
//  threads.delay(500);
  digitalWrite(SOL1, LOW);
  digitalWrite(SOL2, LOW);
  digitalWrite(SOL3, LOW);
  digitalWrite(SOL4, LOW);
  //threads.delay(250);
}

// Triggers all four solenoids
void fireAll(){
  digitalWrite(SOL1, HIGH);
  digitalWrite(SOL2, HIGH);
  digitalWrite(SOL3, HIGH);
  digitalWrite(SOL4, HIGH);
  delay(500);
  digitalWrite(SOL1, LOW);
  digitalWrite(SOL2, LOW);
  digitalWrite(SOL3, LOW);
  digitalWrite(SOL4, LOW);
  delay(250);
}

// Triggers a  sequential pattern of 1-2-3-4, or reverse, with thread delay
void fireSequentialThread(boolean reverse){
  if(!reverse){
    digitalWrite(SOL1, HIGH);
    //threads.delay(250);
    digitalWrite(SOL1, LOW);
    //threads.delay(250);
    digitalWrite(SOL2, HIGH);
    //threads.delay(250);
    digitalWrite(SOL2, LOW);
    //threads.delay(250);
    digitalWrite(SOL3, HIGH);
    //threads.delay(250);
    digitalWrite(SOL3, LOW);
    //threads.delay(250);
    digitalWrite(SOL4, HIGH);
    //threads.delay(250);
    digitalWrite(SOL4, LOW);
    //threads.delay(250);
  } else {
    digitalWrite(SOL4, HIGH);
    //threads.delay(250);
    digitalWrite(SOL4, LOW);
    //threads.delay(250);
    digitalWrite(SOL3, HIGH);
    //threads.delay(250);
    digitalWrite(SOL3, LOW);
    //threads.delay(250);
    digitalWrite(SOL2, HIGH);
    //threads.delay(250);
    digitalWrite(SOL2, LOW);
    //threads.delay(250);
    digitalWrite(SOL1, HIGH);
    //threads.delay(250);
    digitalWrite(SOL1, LOW);
    //threads.delay(250);
  }
}

// Triggers a  sequential pattern of 1-2-3-4, or reverse
void fireSequential(boolean reverse){
  if(!reverse){
    digitalWrite(SOL1, HIGH);
    delay(250);
    digitalWrite(SOL1, LOW);
    delay(250);
    digitalWrite(SOL2, HIGH);
    delay(250);
    digitalWrite(SOL2, LOW);
    delay(250);
    digitalWrite(SOL3, HIGH);
    delay(250);
    digitalWrite(SOL3, LOW);
    delay(250);
    digitalWrite(SOL4, HIGH);
    delay(250);
    digitalWrite(SOL4, LOW);
    delay(250);
  } else {
    digitalWrite(SOL4, HIGH);
    delay(250);
    digitalWrite(SOL4, LOW);
    delay(250);
    digitalWrite(SOL3, HIGH);
    delay(250);
    digitalWrite(SOL3, LOW);
    delay(250);
    digitalWrite(SOL2, HIGH);
    delay(250);
    digitalWrite(SOL2, LOW);
    delay(250);
    digitalWrite(SOL1, HIGH);
    delay(250);
    digitalWrite(SOL1, LOW);
    delay(250);
  }
}

// Turns off all fire
void fireOff(){
  digitalWrite(SOL1, LOW);
  digitalWrite(SOL2, LOW);
  digitalWrite(SOL3, LOW);
  digitalWrite(SOL4, LOW);
}

// Sets the LED colours based on the win state
void doLights(){
//  Serial.println("doing Lights");
  
  switch (winState) {
    case WINSTATE_NYAN: 
      // nyan rainbow colours
      rainbowCycleThread();
      break;
     case WINSTATE_TENTACLE:
      // green 
      setStripColor(0, 255, 0);
      break;
    case WINSTATE_COIN:
      // yellow
      setStripColor(255, 255, 0);
      break;
    case WINSTATE_FIRE:
      // red
      setStripColor(255, 0, 0);
      break;
    case WINSTATE_CHEESY:
      // orange
      setStripColor(255, 36, 0);
      break;
    case WINSTATE_PINCHY:
      // Red
      setStripColor(255, 0, 0);
      break;
    case WINSTATE_SETH:
      // nyan rainbow colours
      rainbowCycleThread();
    case WINSTATE_LOSS:
      // Dim white
      setStripColor(25, 25, 25);
      break;
    default:
      // White
      //TODO: since this is rgbw try (0,0,0,255) here?
      setStripColor(255, 255, 255);
      break;
  }
}

// Sets the LED strip all to one colour
void setStripColor(int r, int g, int b){
  for (int i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, r, g, b);
  }

  strip.show();
}

// Makes the rainbow equally distributed throughout, intended to be run inside a thread and killed manually
void rainbowCycleThread() {
  uint16_t i;
  uint16_t j = 0;

  while(true){
    if (j > 255){
      j = 0;
    }

    for(i=0; i< strip.numPixels(); i++) {
      strip.setPixelColor(i, Wheel(((i * 256 / strip.numPixels()) + j) & 255));
    }
    
    strip.show();
    j += 10;

    //threads.delay(75);
  }
}

 
// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos) {
  if(WheelPos < 85) {
   return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
  } else if(WheelPos < 170) {
   WheelPos -= 85;
   return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  } else {
   WheelPos -= 170;
   return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
}

// Triggers the coin dispenser to dispense a coin
void doCoin(){
  coinServo.write(30); 
  delay(200);
  coinServo.write(90);
}


//protothreads, experimental
int activeTentacle = 0;
int activeLights = 0;

/* This function toggles the LED after 'interval' ms passed */
static int protothread1(struct pt *pt) {
  static unsigned long timestamp = 0;
  PT_BEGIN(pt);
  while(1) { // never stop 
    Serial.print("PT1");
    /* each time the function is called the second boolean
    *  argument "millis() - timestamp > interval" is re-evaluated
    *  and if false the function exits after that. */
      PT_WAIT_UNTIL(pt, activeTentacle == 1);
      Serial.print("PT1 PART A");
      tentacleServo.write(0); 
      timestamp = millis(); // take a new timestamp
      
      PT_WAIT_UNTIL(pt, activeTentacle == 1 && millis() - timestamp > 500);
      Serial.print("PT1 PART B");
      tentacleServo.write(45); 
      timestamp = millis(); // take a new timestamp
      
      PT_WAIT_UNTIL(pt, activeTentacle == 1 && millis() - timestamp > 300);
      Serial.print("PT1 PART C");
      tentacleServo.write(0); 
      timestamp = millis(); // take a new timestamp
      
      PT_WAIT_UNTIL(pt, activeTentacle == 1 && millis() - timestamp > 300);
      tentacleServo.write(45); 
      timestamp = millis(); // take a new timestamp
      
      PT_WAIT_UNTIL(pt, activeTentacle == 1 && millis() - timestamp > 300);
      tentacleServo.write(0); 
      timestamp = millis(); // take a new timestamp
      
      PT_WAIT_UNTIL(pt, activeTentacle == 1 && millis() - timestamp > 500);
      tentacleServo.write(90); 
      timestamp = millis(); // take a new timestamp
      activeTentacle = 0;
  }

  PT_END(pt);
}

static int protothread2(struct pt *pt) {
  static unsigned long timestamp = 0; 
  static uint16_t i;
  static uint16_t j = 0;
  
  PT_BEGIN(pt);
  while(1) { // never stop 
//    Serial.print("PT2");
    /* each time the function is called the second boolean
    *  argument "millis() - timestamp > interval" is re-evaluated
    *  and if false the function exits after that. */
    PT_WAIT_UNTIL(pt, activeLights == 1);
    timestamp = millis();
    if (j > 255){
      j = 0;
    }

    for(i=0; i< strip.numPixels(); i++) {
      strip.setPixelColor(i, Wheel(((i * 256 / strip.numPixels()) + j) & 255));
    }
    
    strip.show();
    j += 10;
    PT_WAIT_UNTIL(pt, activeLights == 1 && millis() - timestamp > 10);
    timestamp = millis();
  }
  PT_END(pt);
}
