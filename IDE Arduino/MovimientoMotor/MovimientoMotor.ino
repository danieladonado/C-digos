int estadoAnterior;
int estadoActual;

unsigned long ranuras = 0;
unsigned long ranurasAnterior = 0;
unsigned long ranurasInicio = 0;

int pinVelocidad = 5;
int pinDir1 = 3;
int pinDir2 = 4;

float pwm = 150;

const float paso = 0.7;
const float RANURAS_POR_VUELTA = 4.0;
const float tiempoDeseado = 0.3;

float distancia = 0;

float rpmDeseadas = 0;
float rpmActual = 0;
float rpmMax = 0;

bool activo = false;

unsigned long inicioMovimiento = 0;
unsigned long tiempoAnterior = 0;

float Kp = 0.1;

const unsigned long intervalo = 200;

void detenerMotor() {

  activo = false;

  analogWrite(pinVelocidad, 0);
  digitalWrite(pinDir1, LOW);
  digitalWrite(pinDir2, LOW);

  float ranurasRecorridas = ranuras - ranurasInicio;
  float vueltas = ranurasRecorridas / RANURAS_POR_VUELTA;
  float distanciaReal = vueltas * paso;

  if (distancia < 0) {
    distanciaReal = -distanciaReal;
  }

  float errorDistancia = distanciaReal - distancia;

  Serial.println();
  Serial.println("===== RESULTADO =====");

  Serial.print("Ranuras detectadas: ");
  Serial.println(ranurasRecorridas);

  Serial.print("Vueltas: ");
  Serial.println(vueltas);

  Serial.print("Distancia pedida: ");
  Serial.print(distancia);
  Serial.println(" mm");

  Serial.print("Distancia real: ");
  Serial.print(distanciaReal);
  Serial.println(" mm");

  Serial.print("Error: ");
  Serial.print(errorDistancia);
  Serial.println(" mm");

  Serial.print("RPM maxima: ");
  Serial.println(rpmMax);

  Serial.println("=====================");
  Serial.println();

  Serial.println("Ingresa: distancia(mm)");
  Serial.println("Ejemplo: 10");
}

void leerEntrada() {

  if (Serial.available() > 0) {

    String linea = Serial.readStringUntil('\n');
    linea.trim();

    float d = linea.toFloat();

    if (d != 0) {

      distancia = d;

      rpmDeseadas = (abs(distancia) / paso) / tiempoDeseado * 60.0;

      pwm = 150;

      rpmMax = 0;

      ranurasAnterior = ranuras;
      ranurasInicio = ranuras;

      tiempoAnterior = millis();
      inicioMovimiento = millis();

      if (distancia > 0) {
        digitalWrite(pinDir1, HIGH);
        digitalWrite(pinDir2, LOW);
      }
      else {
        digitalWrite(pinDir1, LOW);
        digitalWrite(pinDir2, HIGH);
      }

      activo = true;

      Serial.println();
      Serial.println("===== NUEVO MOVIMIENTO =====");

      Serial.print("Distancia: ");
      Serial.print(distancia);
      Serial.println(" mm");

      Serial.print("Tiempo: ");
      Serial.print(tiempoDeseado);
      Serial.println(" s");

      Serial.print("RPM deseadas: ");
      Serial.println(rpmDeseadas);

      Serial.println("============================");
    }
    else {
      Serial.println("Valor invalido.");
    }
  }
}

void setup() {

  Serial.begin(9600);

  pinMode(2, INPUT);

  pinMode(pinVelocidad, OUTPUT);
  pinMode(pinDir1, OUTPUT);
  pinMode(pinDir2, OUTPUT);

  digitalWrite(pinDir1, LOW);
  digitalWrite(pinDir2, LOW);

  estadoAnterior = digitalRead(2);

  tiempoAnterior = millis();

  Serial.println("Ingresa: distancia(mm)");
  Serial.println("Ejemplo: 10");
}

void loop() {

  leerEntrada();

  estadoActual = digitalRead(2);

  if (estadoAnterior == 0 && estadoActual == 1) {
    ranuras++;
  }

  estadoAnterior = estadoActual;

  if (!activo) {
    analogWrite(pinVelocidad, 0);
    return;
  }

  unsigned long ahora = millis();

  if (ahora - inicioMovimiento >= (unsigned long)(tiempoDeseado * 1000.0)) {
    detenerMotor();
    return;
  }

  analogWrite(pinVelocidad, (int)pwm);

  if (ahora - tiempoAnterior >= intervalo) {

    unsigned long huecos = ranuras - ranurasAnterior;

    float tiempoMedicion = ahora - tiempoAnterior;

    rpmActual =
      (huecos * (1000.0 / tiempoMedicion) /
      RANURAS_POR_VUELTA) * 60.0;

    if (rpmActual > rpmMax) {
      rpmMax = rpmActual;
    }

    float error = rpmDeseadas - rpmActual;

    pwm = pwm + (Kp * error);

    if (pwm < 120) {
      pwm = 120;
    }

    if (pwm > 255) {
      pwm = 255;
    }

    ranurasAnterior = ranuras;
    tiempoAnterior = ahora;

    Serial.print("RPM: ");
    Serial.print(rpmActual);

    Serial.print(" | RPM deseadas: ");
    Serial.print(rpmDeseadas);

    Serial.print(" | PWM: ");
    Serial.println(pwm);
  }
}