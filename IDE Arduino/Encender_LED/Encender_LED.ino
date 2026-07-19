String Comando;
int Led=2;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(50); //Tiempo maximo de espera
  pinMode(Led, OUTPUT);
}

void loop() {
  if (Serial.available()){
    Comando=Serial.readString();
    if (Comando=="On")
    {
      digitalWrite(Led, HIGH);
    }
    else (Comando=="Off")
    {
      digitalWrite(Led,LOW);
    }
  }
  delay(20);
}
