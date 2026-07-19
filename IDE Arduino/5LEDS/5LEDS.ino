String Comando;
int LED=2, L2=4, L3=18, L4=19, L5=21;
int i, datos=5;
int Data[]={0,0,0,0,0};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.setTimeout(50);
  pinMode(LED,OUTPUT);
  pinMode(L2,OUTPUT);
  pinMode(L3,OUTPUT);
  pinMode(L4,OUTPUT);
  pinMode(L5,OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()){
    Comando=Serial.readStringUntil('\n');
   
    for (i=0; i<datos; i+=1)
    {
      Data[i]=Comando.substring(i,i+1).toInt();  
    }

    if (Data[0]==1)
    {
      digitalWrite(LED,HIGH);
    }
    else if (Data[0]==0)
    {
      digitalWrite(LED,LOW);
    }
    else {
      Serial.println("Comando no declarado");
    }

    if (Data[1]==1)
    {
      digitalWrite(L2,HIGH);
    }
    else if (Data[1]==0)
    {
      digitalWrite(L2,LOW);
    }

    if (Data[2]==1)
    {
      digitalWrite(L3,HIGH);
    }
    else if (Data[2]==0)
    {
      digitalWrite(L3,LOW);
    }

    if (Data[3]==1)
    {
      digitalWrite(L4,HIGH);
    }
    else if (Data[3]==0)
    {
      digitalWrite(L4,LOW);
    }

    if (Data[4]==1)
    {
      digitalWrite(L5,HIGH);
    }
    else if (Data[4]==0)
    {
      digitalWrite(L5,LOW);
    }

  }
  delay(20);

}