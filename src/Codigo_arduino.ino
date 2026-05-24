#include <Servo.h>

// --- CONFIGURACIÓN DE PINES ---
Servo servoDir;
const int pinServo = 8;
const int mPWM = 7, mIN3 = 9, mIN4 = 10;

// Pines Sensores Ultrasónicos: {Trigger, Echo}
const int sF[] = {2, 3};   // Frente
const int sA[] = {5, 4};  // Atrás
const int sI[] = {12, 13}; // Izquierda
const int sD[] = {11, 6};   // Derecha

// --- VARIABLES DE ESTADO ---
String cadenaSerial = "";
unsigned long tiempoInicioEstacionamiento = 0;
int faseEstacionamiento = 0;                  
int ladoParedSalida = 0;     // 1 = Izquierda, 2 = Derecha, 3 = Centro
int ladoCajonParqueo = 0;    // 1 = Izquierda, 2 = Derecha
unsigned long ultimoEnvioSensores = 0;
const unsigned long intervaloEnvio = 200;

void setup() {
  Serial.begin(115200);
  servoDir.attach(pinServo);
  
  pinMode(mPWM, OUTPUT);
  pinMode(mIN3, OUTPUT);
  pinMode(mIN4, OUTPUT);
  
  int sensores[4][2] = {{sF[0], sF[1]}, {sA[0], sA[1]}, {sI[0], sI[1]}, {sD[0], sD[1]}};
  for(int i = 0; i < 4; i++){
    pinMode(sensores[i][0], OUTPUT);
    pinMode(sensores[i][1], INPUT);
  }
  servoDir.write(90);
  cadenaSerial.reserve(32); // Evita fragmentación de memoria RAM
}

long leer(const int p[]) {
  digitalWrite(p[0], LOW); 
  delayMicroseconds(2);
  digitalWrite(p[0], HIGH); 
  delayMicroseconds(10);
  digitalWrite(p[0], LOW);
  
  long t = pulseIn(p[1], HIGH, 10000); // Timeout a 10ms (máx ~1.7 metros) para no colgar el bucle
  return (t == 0) ? 400 : t * 0.034 / 2;
}

void mover(int v, int a) {
  servoDir.write(a);
  if (v == 0) {
    digitalWrite(mIN3, LOW); 
    digitalWrite(mIN4, LOW);
  } else {
    digitalWrite(mIN3, v > 0 ? HIGH : LOW);
    digitalWrite(mIN4, v > 0 ? LOW : HIGH);
  }
  analogWrite(mPWM, abs(v));
}

void loop() {
  unsigned long tiempoActual = millis();
  
  while (Serial.available() > 0) {
    char caracter = (char)Serial.read();
    if (caracter == '\n') {
      procesarComandoRaspberry(cadenaSerial, 60, 60, 60, 60);
      cadenaSerial = ""; 
    } else {
      cadenaSerial += caracter;
    }
  }

  if (tiempoActual - ultimoEnvioSensores >= intervaloEnvio) {
    ultimoEnvioSensores = tiempoActual;

    long dF = leer(sF);
    long dA = leer(sA);
    long dI = leer(sI);
    long dD = leer(sD);

    // Envía los datos hacia la Raspberry de forma controlada
    Serial.print("D:");
    Serial.print(dF); Serial.print(",");
    Serial.print(dA); Serial.print(",");
    Serial.print(dI); Serial.print(",");
    Serial.println(dD);
  }
}

void procesarComandoRaspberry(String comando, long dF, long dA, long dI, long dD) {
  comando.trim();
  if (!comando.startsWith("A") || comando.length() < 6) return;

  int ang = comando.substring(1, 4).toInt();
  char pwr = comando.charAt(5);         
  int vel = 0;

  // 1. DEFINICIÓN DE VELOCIDAD
  switch (pwr) {
    case 'H': vel = 255; break; // Boost
    case 'M': vel = 196; break; // Crucero
    case 'L': vel = 140; break; // Maniobra
    case 'O':                   // Salida Proyectada
      vel = 125; 
      if (ladoParedSalida == 0) {
        tiempoInicioEstacionamiento = millis();
        if (dI < 20)      ladoParedSalida = 1;
        else if (dD < 20) ladoParedSalida = 2;
        else              ladoParedSalida = 3;
      }
      
      unsigned long tiempoSalida = millis() - tiempoInicioEstacionamiento;
      if (ladoParedSalida == 1) {
        ang = (tiempoSalida < 450) ? 120 : 90;
      } else if (ladoParedSalida == 2) {
        ang = (tiempoSalida < 450) ? 60 : 90;
      } else {
        ang = 90;
      }
      break;
  }

  // 2. PROTECCIÓN TRADICIONAL DE PAREDES EN CARRERA
  if (pwr != 'P' && pwr != 'O') {
    ladoParedSalida = 0;
    if (ang < 90 && dI < 15) {
      ang = 75;
    } else if (ang > 90 && dD < 15) {
      ang = 105;
    }
    
    // Zona Segura Pasillos
    if (dI < 35 && dD < 35) {
      ang = constrain(90 - ((dI - dD) * 2), 75, 105);
    }
  }

  // 3. SISTEMA DE PARQUEO GUIADO (MÁQUINA DE ESTADOS)
  if (pwr == 'P') {
    if (faseEstacionamiento == 0) {
      tiempoInicioEstacionamiento = millis();
      ladoCajonParqueo = (dI > dD) ? 1 : 2;
      faseEstacionamiento = 1;
    }
    
    unsigned long tiempoTranscurrido = millis() - tiempoInicioEstacionamiento;

    switch (faseEstacionamiento) {
      case 1: // Rebasar abriéndose
        ang = (ladoCajonParqueo == 1) ? 105 : 75;
        vel = 110;  
        if (dF < 20 || tiempoTranscurrido > 1600) {
          faseEstacionamiento = 2;
          tiempoInicioEstacionamiento = millis();
        }
        break;

      case 2: // Quiebre estático del servo
        ang = (ladoCajonParqueo == 1) ? 60 : 120;
        vel = 0;    
        if (tiempoTranscurrido > 400) {
          faseEstacionamiento = 3;
          tiempoInicioEstacionamiento = millis();
        }
        break;

      case 3: // Reversa diagonal
        ang = (ladoCajonParqueo == 1) ? 60 : 120;
        vel = -130;  
        if (((ladoCajonParqueo == 1) ? dI : dD) < 14 || tiempoTranscurrido > 2200) {
          faseEstacionamiento = 4;
          tiempoInicioEstacionamiento = millis();
        }
        break;

      case 4: // Contravolante para alinear
        ang = (ladoCajonParqueo == 1) ? 120 : 60;
        vel = -110;  
        if (tiempoTranscurrido > 1200) {
          faseEstacionamiento = 5;
        }
        break;

      case 5: // Estacionado y apagado
        ang = 90;
        vel = 0;
        break;
    }
  }

  // Parada externa de emergencia o seguridad por proximidad frontal
  if (pwr == 'S') {
    faseEstacionamiento = 0;
    vel = 0;   
    ang = 90;  
  }
  
  if (dF < 12) vel = 0;

  mover(vel, ang;

  // Telemetría serial de retorno
  Serial.print("D:");
  Serial.print(dF); Serial.print(",");
  Serial.print(dA); Serial.print(",");
  Serial.print(dI); Serial.print(",");
  Serial.println(dD);
}