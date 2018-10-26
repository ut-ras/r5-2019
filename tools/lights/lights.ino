int amt;
//sets which pin each led will be hooked up to
const int pin250 = 22;
const int pin500 = 26;
const int pin750 = 30;
const int pin1K = 34;
// 250HZ,500HZ,750HZ,1000HZ
int pins[4] = {pin250,pin500,pin750,pin1K};
// Keeps track of which light is on or off
boolean on[4] = {false,false,false,false};

void setup() {
  //Sets each pinout to output
  pinMode(pin250,OUTPUT);
  pinMode(pin500,OUTPUT);
  pinMode(pin750,OUTPUT);
  pinMode(pin1K,OUTPUT);
  amt = 0;
}

//Should run every 1/6000th of a second, calls appropriate pins to switch
void loop() {
  if(amt%12==0){
    switchLight(0);
    amt = 0;
  }
  if(amt%6==0){
    switchLight(1);
  }
  if(amt%4==0){
    switchLight(2);
  }
  if(amt%3==0){
    switchLight(3);
  }
  delayMicroseconds(166);
  amt++;
}
//switches pin at pins[i] from on to off
void switchLight(int i){
  if(on[i]){
    digitalWrite(pins[i], LOW);
  }
  else{
    digitalWrite(pins[i], HIGH);
  }
  on[i] = !on[i];
}
