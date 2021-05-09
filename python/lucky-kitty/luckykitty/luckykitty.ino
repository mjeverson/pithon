/***************************************************
  Lucky Kitty Slot Machine MkII

  Designed for use with Arduino Mini pro 5V 16Hz && Associated Raspberry Pi 

  //todo(mje): Will we still need threads? Arduino mini pro threading?
  // This sets everything up then goes into waiting-for-serial
  // based on the code (loss, reset, victory-type) do all the things (in threads if necessary) and when done send a Done signal to the pi

 ****************************************************/

#include <PWMServo.h> // Tentacle & Coin
//#include <TeensyThreads.h> // Threading
#include <Adafruit_NeoPixel.h> // LED Stuff

// Handle mechanism
//#define HANDLE A2

// Solenoids
#define SOL1 20
#define SOL2 21
#define SOL3 22
#define SOL4 23

// Valid output pins: //2-10, 14, 16-17, 20-23, 29-30, 35-38
#define TENTACLE_SERVO 35
#define COIN_SERVO 36
#define PIXEL 38
#define NUM_PIXELS 90
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_PIXELS, PIXEL, NEO_GRBW + NEO_KHZ800);

PWMServo tentacleServo;
PWMServo coinServo;  
int tentacleServoPos = 0;
int coinServoPos = 0;

#define WINSTATE_NONE 0
#define WINSTATE_NYAN 1
#define WINSTATE_TENTACLE 2
#define WINSTATE_COIN 3
#define WINSTATE_FIRE 4
#define WINSTATE_CHEESY 5
#define WINSTATE_PINCHY 6
#define WINSTATE_LOSS 7
#define WINSTATE_SETH 8
int winState, slot1_current, slot2_current, slot3_current; 

// Get this party started!
void setup() {
  // Sets up the RNG
  randomSeed(analogRead(A0));
  
  Serial.begin(9600);

  // Set up solenoid
  pinMode(SOL1, OUTPUT);
  pinMode(SOL2, OUTPUT);
  pinMode(SOL3, OUTPUT);
  pinMode(SOL4, OUTPUT);

  //Set up servos
  tentacleServo.attach(TENTACLE_SERVO);
  coinServo.attach(COIN_SERVO);

  // Set up LEDs. Some default colour to indicate ready to go
  strip.begin();

  // Initializes the state of the peripherals
  resetState();
}

void loop() {
  Serial.print("\nPull handle to begin slots!\n");

//todo:wait until we get a code from the pi. 
// Set the winstate based on that, then doWinState with some small changes, followed by "done"
// There'll need to be an extra command for "dispense N coins"
//  if(Serial.available()){
//    doCoin();
//    Serial.read();
//  }

}


// Sets the slots rolling, picks an outcome and displays it
// On rollSlots, we should iterate through 0-6 and set the slot to be whatever its current state is +1 (rolling over, so use %)
// Also need to randomize a win state. States should be any of the 6 outcomes, or a total loss, or an almost loss (Trish has the odds)
// On a result, save the global state of the slots. 
// keep rolling the first slot til it gets where it needs to go. Then the second, then the third. (don't update the global state)
// OR just let the first slot start one or two early, then the second slot, then the third slot. let them roll a few times, then do it all again. Don't need global state
//void rollSlots(){  
//  // Start playing rolling sound
//  int playReelLoopThreadID = threads.addThread(playReelLoopThread);
//
//  // Calculate win state
//  int winRoll = random(1,100); 
//  
//  // Calcuate partial fail slot displays
//  int falseWinSlot, falseWinSlotOdd;
//    
//  do {
//    falseWinSlot = random(0,6);
//    falseWinSlotOdd = random(0,6);
//  } while (falseWinSlot == falseWinSlotOdd);
//  
//  int slot1_end, slot2_end, slot3_end;
//  
//  if (winRoll <= 10) {
//    // nyancat, 10% chance
//    winState = WINSTATE_NYAN;
//    slot1_end = slot2_end = slot3_end = 0;
//  } else if (winRoll <= 20){
//    // tentacle, 10% chance
//    winState = WINSTATE_TENTACLE;
//    slot1_end = slot2_end = slot3_end = 1;
//  } else if (winRoll <= 25) {
//    // coin, 5% chance
//    winState = WINSTATE_COIN;
//    slot1_end = slot2_end = slot3_end = 2;
//  } else if (winRoll <= 35) {
//    // fire, 10% chance
//    winState = WINSTATE_FIRE;
//    slot1_end = slot2_end = slot3_end = 3;
//  } else if (winRoll <= 45) {
//    // cheesy poofs, 10% chance
//    winState = WINSTATE_CHEESY;
//    slot1_end = slot2_end = slot3_end = 4;
//  } else if (winRoll <= 50){
//    // pinchy, 5% chance
//    winState = WINSTATE_PINCHY;
//    slot1_end = slot2_end = slot3_end = 5;
//  } else if (winRoll <= 52) {
//    //todo: seth win, 2% chance
//    winState = WINSTATE_SETH;
//    slot1_end = slot2_end = slot3_end = 6;
//  } else if (winRoll <= 62) {
//    // partial fail, 10% chance
//    winState = WINSTATE_LOSS;
//    slot1_end = slot2_end = falseWinSlot;
//    slot3_end = falseWinSlotOdd;
//  } else if (winRoll <= 72) {
//    // Partial fail, 10% chance
//    winState = WINSTATE_LOSS;
//    slot1_end = slot3_end = falseWinSlot;
//    slot2_end = falseWinSlotOdd;
//  }else if (winRoll <= 82) {
//    // Partial fail, 10% chance
//    winState = WINSTATE_LOSS;
//    slot2_end = slot3_end = falseWinSlot;
//    slot1_end = falseWinSlotOdd;
//  } else {
//    // Total fail, 18% chance
//    winState = WINSTATE_LOSS;
//    slot1_end = falseWinSlot;
//    slot2_end = falseWinSlotOdd;
//    slot3_end = random(0,6);
//  }
//
//  // new shorter rolling logic
//  int rollsBeforeStopping = 4;
//  int i = 0;
//
//  // Want to make sure we don't get a slot rolling the same thing twice, looks like it doesn't update
//  while(i < rollsBeforeStopping){
//    int slot1_new = slot1_current;
//    int slot2_new = slot2_current;
//    int slot3_new = slot3_current;
//    
//    while (slot1_new == slot1_current){
//      slot1_new = random(0,6);
//    }
//    
//    while (slot2_new == slot2_current){
//      slot2_new = random(0,6);
//    }
//
//    while (slot3_new == slot3_current){
//      slot3_new = random(0,6);
//    }
//
//    bmpDraw(images[slot1_new], 0, 0, tft);
//    bmpDraw(images[slot2_new], 0, 0, tft2);
//    bmpDraw(images[slot3_new], 0, 0, tft3);
//
//    slot1_current = slot1_new;
//    slot2_current = slot2_new;
//    slot3_current = slot3_new;
//
//    i++;
//  }
//
//  slot1_current = slot1_end;
//  slot2_current = slot2_end;
//  slot3_current = slot3_end;
//
//  delay(10);
//  
//  while(playWav1.isPlaying()){
//    Serial.println("Waiting for rstop16 audio to finish!");
//    delay(10);
//  }
//}

void doWinState(){
  //based on win state do sounds, fire, etc.
  switch (winState) {
    case WINSTATE_NYAN: {
      Serial.println("doWinState nyan");
      // Start lights thread, start playing nyan cat, start fire thread, wait til both nyancat and fire are done

      // Do Lights in a thread
      int lightThreadId = threads.addThread(doLights);

      // Sound: Nyancat. This occasionally gets skipped. Some weird timing thing? wait til it starts playing.
//      playSound("nyan16.wav");

      // Do the fire. Might need to swap to clock watching
      int fireThreadId = threads.addThread(doFire);

      // Wait for nyancat to finish playing, then kill the lights thread
      while(playWav1.isPlaying() || threads.getState(fireThreadId) == Threads::RUNNING){
        Serial.println("Waiting for nyancat to finish playing or fire to finish");
      }

      threads.kill(lightThreadId);
      
      break;
    }
    case WINSTATE_TENTACLE: {
      Serial.println("doWinState tentacle");
      // Change lights, start scream sound, start tentacle thread, start fire thread, wait til both tentacle and fire are done

      // LEDs: green
      doLights();

      // Sound: person screaming
//      playSound("scream16.wav");
  
      // Wave the tentacle
      int tentacleThreadId = threads.addThread(doTentacle);

      while(threads.getState(tentacleThreadId) == Threads::RUNNING) {
        Serial.println("Waiting for tentacle or fire thread");
      }

      //fire: all at once
      doFire();
        
      break;
    }
    case WINSTATE_COIN:
      Serial.println("doWinState coin");
      // Change lights, start coin sound + 1up sound, do fire, do coin

      // LEDs: Yellow
      doLights();

      //TODO: sound: mario 1up/coin
//      playSound("coin16.wav");
      
      // Dispense a coin
      doCoin();

      delay(10);
      while(playWav1.isPlaying()){
        delay(10);
      }

      playSound("1up16.wav");
      
      delay(10);
      while(playWav1.isPlaying()){
        delay(10);
      }

      // fire: 1-3-2-4-all
      doFire();
      
      break;
    case WINSTATE_FIRE:
      Serial.println("doWinState fire");
      // Change lights, start playing sound, do fire, wait til sound is finished
      
      // LEDs: Red
      doLights();

      // sound: highway to hell
//      playSound("hth16.wav");
      
      doFire();

      break;
    case WINSTATE_CHEESY:
      Serial.println("doWinState cheesy");
      // Change lights, start playing sound, do fire
      
      // LEDs: orange
      doLights();
      
      // Sound: cheesy poofs
//      playSound("cheesy16.wav");

      // no fire
      doFire();

      break;
    case WINSTATE_PINCHY:
      Serial.println("doWinState pinchy");
      
      // LEDs: Red
      doLights();
      
      // Sound: PINCHAY
//      playSound("pinchy16.wav");

      // fire all 4
      doFire();
      
      break;
    case WINSTATE_SETH: {
      Serial.println("doWinState Seth");
      //todo: add seth win
      playSound("seth16.wav");

      delay(1500);

      //todo: threaded rainbow colours
      int lightThreadId = threads.addThread(doLights);

      //todo: threaded fire
      int fireThreadId = threads.addThread(doFire);

      // Wait for nyancat to finish playing, then kill the lights thread
//      while(playWav1.isPlaying()){
//        Serial.println("Waiting for nyancat to finish playing or fire to finish");
//      }
//
//      threads.kill(lightThreadId);

      for(int i = 0; i < 5; i++){
        playSound("coin16.wav");
        doCoin();
        delay(200);
      }

      playSound("1up16.wav");

      break;
    }
    case WINSTATE_LOSS:
      playSound("loss16.wav");
      doLights();
      break;
    default: 
      break;
  } 
}

//TODO: Set everything back to normal state for another round. are we missing anything?
void resetState(){
  Serial.println("Round over, state reset!");

  // Reset the win state
  winState = WINSTATE_NONE;
  
  // Reset coin and tentacle servo positions
  tentacleServo.write(90);
  coinServo.write(90);
  
  // reset LEDs
  doLights();
  analogWrite(SAFETY_PIXEL, 255);

  // Make sure fire is off
  doFire();
}

// Stops any existing sound, makes sure the file is closed, then keeps attempting to play the sound until it actually starts
void playSound(char* filename){
  playWav1.stop();
  delay(10); //TODO: Might not need this
  
  while(!playWav1.isPlaying()){
    if(audioFile){
      Serial.println("closing redundant audioFile inside while loop");
      audioFile.close();
    }
    
    if(audioFile = sd2.open(filename)){
      Serial.println("Playing: ");
      Serial.print(filename);
      playWav1.play(audioFile);
    } else {
      Serial.println("problem opening sound file");
    }

    delay(10);
  }
}

// Do the fire. Might need to swap to clock watching
void doFire(){
  Serial.println("doing fire");

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
  threads.delay(500);
  digitalWrite(SOL1, LOW);
  digitalWrite(SOL2, LOW);
  digitalWrite(SOL3, LOW);
  digitalWrite(SOL4, LOW);
  threads.delay(250);
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
    threads.delay(250);
    digitalWrite(SOL1, LOW);
    threads.delay(250);
    digitalWrite(SOL2, HIGH);
    threads.delay(250);
    digitalWrite(SOL2, LOW);
    threads.delay(250);
    digitalWrite(SOL3, HIGH);
    threads.delay(250);
    digitalWrite(SOL3, LOW);
    threads.delay(250);
    digitalWrite(SOL4, HIGH);
    threads.delay(250);
    digitalWrite(SOL4, LOW);
    threads.delay(250);
  } else {
    digitalWrite(SOL4, HIGH);
    threads.delay(250);
    digitalWrite(SOL4, LOW);
    threads.delay(250);
    digitalWrite(SOL3, HIGH);
    threads.delay(250);
    digitalWrite(SOL3, LOW);
    threads.delay(250);
    digitalWrite(SOL2, HIGH);
    threads.delay(250);
    digitalWrite(SOL2, LOW);
    threads.delay(250);
    digitalWrite(SOL1, HIGH);
    threads.delay(250);
    digitalWrite(SOL1, LOW);
    threads.delay(250);
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
  Serial.println("doing Lights");
  
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

    threads.delay(75);
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

// Makes the tentacle pop out, wiggle around, and go away
void doTentacle(){
  Serial.println("About to do tentacle");

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
}


// Triggers the coin dispenser to dispense a coin
void doCoin(){
  Serial.println("About to do coin");
  coinServo.write(30); 
  delay(200);
  coinServo.write(90);
}


