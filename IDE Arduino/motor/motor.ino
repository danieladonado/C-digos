// Pines de control para el Motor
const int pinPWM = 15;  // Pin PWM para la velocidad
const int pinIN1 = 19;  // Pin digital para dirección 1
const int pinIN2 = 5;  // Pin digital para dirección 2

void setup() {
  pinMode(pinPWM, OUTPUT);
  pinMode(pinIN1, OUTPUT);
  pinMode(pinIN2, OUTPUT);
}

void loop() {
 
  digitalWrite(pinIN1, HIGH);
  digitalWrite(pinIN2, LOW);
  analogWrite(pinPWM, 30); 
  delay(3000);
}

