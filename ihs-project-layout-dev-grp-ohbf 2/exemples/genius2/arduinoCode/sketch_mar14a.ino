int c = 262;
int d = 294;
int e = 330;
int f = 349;
int g = 392;
int a = 440;
int b = 494;
int tempo = 400;
long duration;
int distance;


const int trigPin = 8;
const int echoPin = 9;

char cmd;

void setup(){
  pinMode(10,OUTPUT);
  pinMode(trigPin, OUTPUT); 
  pinMode(echoPin, INPUT); 
  Serial.begin(9600); 
}

void loop(){
  cmd = Serial.read();
  if(cmd == 's'){
    delay(1000);
    tone(10,c,tempo); 
    delay(1000);
    tone(10,c,tempo); 
    delay(1000);
    tone(10,c,tempo); 
    delay(1000);
    tone(10,f,3*tempo);
  }
  if(cmd == 'd'){
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    duration = pulseIn(echoPin, HIGH);
    distance = duration * 0.034 / 2;
    Serial.print("Distance: ");
    Serial.println(distance);
  }
  if(cmd == 'a'){
    tone(10,g,tempo);
  }
}