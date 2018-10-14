int amt;
int pin250 = 22;
int pin500 = 26;
int pin750 = 30;
int pin1K = 34;
boolean on[4] = {false,false,false,false};
void setup() {
  pinMode(pin250,OUTPUT);
  pinMode(pin500,OUTPUT);
  pinMode(pin750,OUTPUT);
  pinMode(pin1K,OUTPUT);
  // put your setup code here, to run once:
  amt = 0;
}

void loop() {
  // put your main code here, to run repeatedly:
  if(amt%12==0){
    switch250();
  }
  if(amt%6==0){
    switch500();
  }
  if(amt%4==0){
    switch750();
  }
  if(amt%3==0){
    switch1K();
  }
  delayMicroseconds(333);
  //delay(3);
  amt++;
}

void switch250(){
  if(on[0]){
    digitalWrite(pin250, LOW);
  }
  else{
    digitalWrite(pin250, HIGH);
  }
  on[0] = !on[0];
}
void switch500(){
  if(on[1]){
    digitalWrite(pin500, LOW);
  }
  else{
    digitalWrite(pin500, HIGH);
  }
  on[1] = !on[1];
}
void switch750(){
  if(on[2]){
    digitalWrite(pin750, LOW);
  }
  else{
    digitalWrite(pin750, HIGH);
  }
  on[2] = !on[2];
}
void switch1K(){
  if(on[3]){
    digitalWrite(pin1K, LOW);
  }
  else{
    digitalWrite(pin1K, HIGH);
  }
  on[3] = !on[3];
}
