#include <Servo.h>

Servo servoDir;
const int pinServo = 8;
const int mPWM = 7, mIN3 = 9, mIN4 = 10;

// Pines Sensores Ultrasónicos: {Trigger, Echo}
//int sF[] = {2, 3};   // Frente
//int sA[] = {14, 15}; // Atrás (A0, A1)
//int sI[] = {4, 5};   // Izquierda
//int sD[] = {6, 7};   // Derecha

void setup() {
  Serial.begin(9600);
  servoDir.attach(pinServo);
  pinMode(mPWM, OUTPUT); 
  pinMode(mIN3, OUTPUT); 
  pinMode(mIN4, OUTPUT);
  
  // Configurar todos los sensores
  //int* sensores[] = {sF, sA, sI, sD};
  //for(int i=0; i<4; i++){
   // pinMode(sensores[i][0], OUTPUT);
    //pinMode(sensores[i][1], INPUT);
  //}
  
  servoDir.write(90); // Iniciar recto
}

long leer(int p[]) {
  digitalWrite(p[0], LOW); delayMicroseconds(2);
  digitalWrite(p[0], HIGH); delayMicroseconds(10);
  digitalWrite(p[0], LOW);
  long t = pulseIn(p[1], HIGH, 20000);
  return (t == 0) ? 400 : t * 0.034 / 2;
}

void mover(int v, int a) {
  servoDir.write(a);
  if (v == 0) {
    digitalWrite(mIN3, LOW); digitalWrite(mIN4, LOW);
  } else {
    digitalWrite(mIN3, v > 0 ? HIGH : LOW);
    digitalWrite(mIN4, v > 0 ? LOW : HIGH);
  }
  analogWrite(mPWM, abs(v));
}

void loop() {
  if (Serial.available() >= 2) {
    char cmd = Serial.read();   // Dirección
    char pwr = Serial.read();   // Potencia/Velocidad

    long dF = 100;//leer(sF);
    long dA = 100;//leer(sA);
    long dI = 100;//leer(sI);
    long dD = 100;//leer(sD);

    Serial.print("S:"); 
    Serial.print(dI);
    Serial.print(",");
    Serial.println(dD); 

    int vel = 0;
    int ang = 90;

    // 1. DEFINIR VELOCIDAD (Gradualidad)
    if (pwr == 'H') vel = 255; // Recta Boost
    if (pwr == 'M') vel = 195; // Crucero
    if (pwr == 'L') vel = 115; // Maniobra

    // 2. DEFINIR DIRECCIÓN (Agresividad y Fusión)
    if (cmd == 'F') ang = 90;
    if (cmd == '1') ang = (dI < 15) ? 88 : 75;  // Izq leve (Fusión con sensor)
    if (cmd == 'I') ang = (dI < 12) ? 75 : 60;  // Izq agresiva
    if (cmd == '2') ang = (dD < 15) ? 92 : 105; // Der leve
    if (cmd == 'D') ang = (dD < 12) ? 105 : 120; // Der agresiva
    
    // 3. LÓGICA DE ESTACIONAMIENTO Y SEGURIDAD
    if (cmd == 'S') {
      if (dA < 8) vel = 0; // Detenerse al tocar pared trasera
      else { vel = -130; ang = 90; } // Retroceder al cajón
    }

    // LOGICA DE FRENADO 1era MODALIDAD (IR AQUI)
    
    if (dF < 12 && cmd == 'F') vel = 0; // Freno emergencia frontal

    mover(vel, ang);

    // 4. TELEMETRÍA (Para el CSV de la Raspberry)
    Serial.print("D:");
    Serial.print(dF); Serial.print(",");
    Serial.print(dA); Serial.print(",");
    Serial.print(dI); Serial.print(",");
    Serial.println(dD);
  }
}