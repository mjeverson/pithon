/***************************************************
  Lucky Kitty Slot Machine MkII

  Designed for use with Teensy 3.2 && Associated Raspberry Pi 

  // This sets everything up then goes into waiting-for-serial
  // based on the code (loss, reset, victory-type) do all the things (in threads if necessary) and when done send a Done signal to the pi

 ****************************************************/

#include <PWMServo.h> // Tentacle & Coin
#include <TeensyThreads.h> // Threading
#include <Adafruit_NeoPixel.h> // LED Stuff

// Solenoids
#define SOL1 3
#define SOL2 4
#define SOL3 5
#define SOL4 6
#define NUM_SOLS 4
int sols[NUM_SOLS] = {SOL1, SOL2, SOL3, SOL4};

// Valid output pins: //2-10, 14, 16-17, 20-23, 29-30, 35-38
#define TENTACLE_SERVO 9
#define COIN_SERVO 10
#define PIXEL 23
#define BOX_PIXELS 59 // this is how many pixels are in the box
#define COIN_PIXELS 5 // this is how many pixels on the strip are on the coin dispenser

#define WIN_NYAN 0x00
#define WIN_TENTACLE 0x01
#define WIN_COIN 0x02
#define WIN_FIRE 0x03
#define WIN_CHEESE 0x04
#define WIN_PINCHY 0x05
#define WIN_JACKPOT 0x06
#define CMD_LOSS 0x07
#define CMD_DONE 0x09

//todo(mje): BOX_PIXELS + COIN_PIXELS
Adafruit_NeoPixel strip = Adafruit_NeoPixel(BOX_PIXELS, PIXEL, NEO_GRBW + NEO_KHZ800);
PWMServo tentacleServo;
PWMServo coinServo;  

// Get this party started!
void setup() {  
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT); 
  digitalWrite(LED_BUILTIN, HIGH);

  // Set up solenoid
  for (int i = 0; i < NUM_SOLS; i++) {
    pinMode(sols[i], OUTPUT);
  }

  //Set up servos
  tentacleServo.attach(TENTACLE_SERVO);
  coinServo.attach(COIN_SERVO);

  // Set up LEDs. Some default colour to indicate ready to go
  strip.begin();

  // Initializes the state of the peripherals
  resetState();

  //todo: Maybe?
  Serial.flush();
}

void loop() {
  // wait until we get a code from the pi. 
  if (Serial.available() > 0){
    byte b = Serial.read();
    switch (b) {
      case WIN_NYAN:
        winNyan();
        break;
      case WIN_TENTACLE:
        winTentacle();
        break;
      case WIN_COIN:
        winCoin();
        break;
      case WIN_FIRE:
        winFire();
        break;
      case WIN_CHEESE:
        winCheese();
        break;
      case WIN_PINCHY:
        winPinchy();
        break;
      case WIN_JACKPOT:
        winJackpot();
        break;
      case CMD_LOSS:
        loss();
        break;
      default:
        // Got an unexpected command
        Serial.write(b);
        break;
    }
  }

  // Reset everything
  resetState();
  Serial.write(CMD_DONE);
}

/* WAIT HELPERS */
void waitForCommand(byte cmd) {
  while (Serial.available() == 0) {}
    if (Serial.read() != cmd) {
      //todo: some sort of error, break and reset?
    }
}

void waitForThread(int threadId) {
  while(threads.getState(threadId) == Threads::RUNNING) {}
}

//THINK: only reset when you get a reset command? Or - always wait for RESET cmd when finished?
/* WIN/LOSS STATES */
void winNyan() {
  // nyan rainbow colours
  int lightThreadId = threads.addThread(rainbowCycleThread);

  //1-2-3-4 
  fireSequential(false);
  fireSequential(true);

  //todo: Maybe - send a "DONE" signal
  Serial.write(CMD_DONE);

  // Wait for the signal that nyancat is done playing
  waitForCommand(CMD_DONE);
  threads.kill(lightThreadId);
}

void winTentacle() {
  // green 
  setBoxColor(0, 255, 0, 0);

  int tentacleThreadId = threads.addThread(doTentacle);
  fireAll();

  waitForThread(tentacleThreadId);
  Serial.write(CMD_DONE);
}

void winCoin() {
  // yellow
  setBoxColor(255, 255, 0, 0);
  setCoinLightColor(255, 255, 0, 0);
  delay(500);
  doCoin();
  
  // fire: 1-3-2-4-all
  fireSequential(false);
  fireAll();
  waitForCommand(CMD_DONE);
}

void winFire() {
  // red
  setBoxColor(255, 0, 0, 0);
  delay(3000);

  //fire all three at "highway to hell"
  //1s-5s-9s-13s for "highway to hell"
  //each fireAll set takes about 2250ms
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
  waitForCommand(CMD_DONE);
}

void winCheese() {
  // orange
  setBoxColor(255, 36, 0, 0);
  fireOff();
  waitForCommand(CMD_DONE);
}

void winPinchy() {
  // Red
  setBoxColor(255, 0, 0, 0);
  // fire all 4
  fireAll();
  waitForCommand(CMD_DONE);
}

void winJackpot() {
  delay(1500);
  // nyan rainbow colours
  int lightThreadId = threads.addThread(rainbowCycleThread);
  
  //1-2-3-4 
  fireSequential(false);
  fireSequential(true);

  Serial.write(CMD_DONE);
  waitForCommand(CMD_DONE);

  threads.kill(lightThreadId);
  setCoinLightColor(255, 255, 0, 0);

  // dispense 3 coins
  for(int i = 0; i < 3; i++){
    delay(500);
    doCoin();
  }
  
  waitForCommand(CMD_DONE);
}

// Fail, dim lights
void loss() {
  setBoxColor(0, 0, 0, 10);
  Serial.write(CMD_DONE);
  waitForCommand(CMD_DONE);
}

void resetState(){
  // Reset coin and tentacle servo positions
  tentacleServo.write(90);
  coinServo.write(90);
  
  // reset LEDs
  setBoxColor(0, 0, 0, 50);
  setCoinLightColor(0, 0, 0, 0);

  // Make sure fire is off
  fireOff();
}

/* FIRE HELPERS */
// Triggers all four solenoids
void fireAll(){
  for (int i = 0; i < NUM_SOLS; i++) {
    digitalWrite(sols[i], HIGH);
  }

  delay(500);
  
  for (int i = 0; i < NUM_SOLS; i++) {
    digitalWrite(sols[i], LOW);
  }
  delay(250);
}

// Triggers a  sequential pattern of 1-2-3-4, or reverse
void fireSequential(boolean reverse){
  for (int i = 0; i < NUM_SOLS; i++) {
    int s = sols[i];
    
    if (reverse){
      s = sols[NUM_SOLS - 1 - i];
    }

    digitalWrite(s, HIGH);
    delay(500);
    digitalWrite(s, LOW);
    delay(500);
  }
}

// Turns off all fire
void fireOff(){
  for (int i = 0; i < NUM_SOLS; i++) {
    int s = sols[i];
    digitalWrite(s, LOW);
  }
}

/* LIGHTS */
// Sets the LED strip around the box all to one colour
void setBoxColor(int r, int g, int b, int w){
  for (int i = COIN_PIXELS; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, r, g, b, w);
  }

  strip.show();
}

// Sets the LED strip for the coin display all to one colour
void setCoinLightColor(int r, int g, int b, int w){
  for (int i = 0; i < COIN_PIXELS; i++) {
    strip.setPixelColor(i, r, g, b, w);
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

    for(i=COIN_PIXELS; i< strip.numPixels(); i++) {
      strip.setPixelColor(i, Wheel(((i * 256 / strip.numPixels()) + j) & 255));
    }
    
    strip.show();
    j += 10;

    threads.delay(50);
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

/* SERVOS */
void doTentacle(){
  tentacleServo.write(0); 
  threads.delay(500);

  tentacleServo.write(45); 
  threads.delay(300);

  tentacleServo.write(0); 
  threads.delay(300);

  tentacleServo.write(45); 
  threads.delay(300);

  tentacleServo.write(0); 
  threads.delay(500);
  
  tentacleServo.write(90);
  delay(15);
}

// Triggers the coin dispenser to dispense a coin
void doCoin(){
  coinServo.write(30); 
  delay(200);
  coinServo.write(90);
  delay(15);
}
