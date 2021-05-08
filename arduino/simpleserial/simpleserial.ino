int led = 13;
int state = 0;

void setup(){
  Serial.begin(9600);
  pinMode(led, OUTPUT); 
}

void loop(){
  if (Serial.available() > 0){
    Serial.print("STATE: ");
    Serial.print(state);
    
    if (state == 0) {
      digitalWrite(led, HIGH);
      state = 1;
    } else {
      digitalWrite(led, LOW);
      state = 0;
    }
    
    String data = Serial.readStringUntil('\n');
    Serial.print("You sent me: ");
    Serial.println(data);
  }
}
