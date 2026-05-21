#include <Servo.h>

Servo servoDir;
const int pinServo = 8;
const int mPWM = 7, mIN3 = 9, mIN4 = 10;

//Pines Sensores Ultrasónicos: {Trigger, Echo}
int sF[] = {2, 3};   // Frente
int sA[] = {13, 6}; // Atrás
int sI[] = {12, 11};   // Izquierda
int sD[] = {5, 4};   // Derecha

// Variables de almacenamiento para el buffer de la Raspberry
String cadenaSerial = ""; 
unsigned long tiempoInicioEstacionamiento = 0; 
int faseEstacionamiento = 0;                  
int ladoParedSalida = 0; // 1 = Pared a la izquierda, 2 = Pared a la derecha
int ladoCajonParqueo = 0; // 1 = Cajón a la izquierda, 2 = Cajón a la derecha

void setup() {
  Serial.begin(115200);
  servoDir.attach(pinServo);
  pinMode(mPWM, OUTPUT); 
  pinMode(mIN3, OUTPUT); 
  pinMode(mIN4, OUTPUT);
  
  //Configurar todos los sensores
  int* sensores[] = {sF, sA, sI, sD};//{sF, sA, sI, sD}
  for(int i=0; i<4; i++){
    pinMode(sensores[i][0], OUTPUT);
    pinMode(sensores[i][1], INPUT);
  }
  
  servoDir.write(90); // Iniciar recto
}

long leer(int p[]) {
  digitalWrite(p[0], LOW); delayMicroseconds(2);
  digitalWrite(p[0], HIGH); delayMicroseconds(10);
  digitalWrite(p[0], LOW);
  long t = pulseIn(p[1], HIGH, 10000);
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
  long dF = leer(sF);
  long dA = leer(sA);
  long dI = leer(sI);
  long dD = leer(sD);

  while (Serial.available() > 0) {
    char caracter = (char)Serial.read();

    if (caracter == '\n') {
      procesarComandoRaspberry(cadenaSerial, dF, dA, dI, dD);
      cadenaSerial = ""; // Limpia datos basura acumulados
    } else {
      cadenaSerial += caracter;
    }
  }
}
    
// --- PROCESADOR ADAPTATIVO: MANTIENE TUS COMENTARIOS Y ESTRUCTURA DE CONTROL ORIGINAL ---
void procesarComandoRaspberry(String comando, long dF, long dA, long dI, long dD) {
  
  comando.trim(); 

  // Validación: Asegura que la cadena contenga el formato procedural enviado por la Pi
  if (comando.startsWith("A") && comando.length() >= 6) {

    // Lee el primer carácter (Dirección) // Dirección -> Ahora extraído del ángulo procedural exacto
    int ang = comando.substring(1, 4).toInt(); 
    
    // Si la Pi envió un segundo carácter rápido, lo leemos. Si no, usamos el por defecto.
    // Valor por defecto por si no llega el segundo carácter
    char pwr = comando.charAt(5); // Potencia/Velocidad         

    int vel = 0;

        // 1. DEFINIR VELOCIDAD (Gradualidad)
    if (pwr == 'H') vel = 255; // Recta Boost
    if (pwr == 'M') vel = 195; // Crucero
    if (pwr == 'L') vel = 115; // Maniobra

    //SALIDA PROYECTADA
    if (pwr == 'O') {
      vel = 125; // Velocidad segura de arranque
      
      // Si aún no sabemos de qué lado está la pared, lo detectamos en frío
      if (ladoParedSalida == 0) {
        tiempoInicioEstacionamiento = millis();
        if (dI < 20)      ladoParedSalida = 1; // Pared a la izquierda
        else if (dD < 20) ladoParedSalida = 2; // Pared a la derecha
        else              ladoParedSalida = 3; // En el centro / No detectada
      }

      unsigned long tiempoSalida = millis() - tiempoInicioEstacionamiento;

      // Ejecutamos la maniobra de evasión según el costado detectado
      if (ladoParedSalida == 1) {
        if (tiempoSalida < 450) {
          ang = 120; // FASE A: Giro rápido a la derecha para apuntar la trompa hacia la trazada
        } else {
          ang = 90;  // FASE B: Enderezar manguetas y dejar que el coche corra en diagonal recta hacia la curva
        }
      } else if (ladoParedSalida == 2) {
        if (tiempoSalida < 450) {
          ang = 60;  // FASE A: Giro rápido a la izquierda para apuntar la trompa hacia la trazada
        } else {
          ang = 90;  // FASE B: Enderezar manguetas y dejar que el coche corra en diagonal recta hacia la curva
        }
      } else {
        ang = 90;  // Salida recta si no está pegado a nada
      }
    }

    // 2. DEFINIR DIRECCIÓN CON PROTECCIÓN TRADICIONAL DE PAREDES EN CARRERA
    if (pwr != 'P' && pwr != 'O') { 
      // Reseteamos el flag de salida para que esté listo en la siguiente carrera
      ladoParedSalida = 0; 

      if (ang < 90) { 
        if (dI < 12) ang = 75; 
        else if (dI < 15 && ang < 75) ang = 75; 
      }
      if (ang > 90) { 
        if (dD < 12) ang = 105; 
        else if (dD < 15 && ang > 105) ang = 105; 
      }
      
      // Zona Segura General en Pasillos de Carrera
      if (dI < 35 && dD < 35) {
        long diferenciaPasillo = dI - dD; 
        int correccionCentrado = 90 - (diferenciaPasillo * 2);
        ang = constrain(correccionCentrado, 75, 105); 
      }
    }

    //sistema de parqueo
    if (pwr == 'P') {
      if (faseEstacionamiento == 0) {
        tiempoInicioEstacionamiento = millis();
        
        // Detectamos de qué lado de la pista está el cajón de estacionamiento (la pared más lejana)
        if (dI > dD) ladoCajonParqueo = 1; // Cajón a la izquierda
        else         ladoCajonParqueo = 2; // Cajón a la derecha
        
        faseEstacionamiento = 1; 
      }

      unsigned long tiempoTranscurrido = millis() - tiempoInicioEstacionamiento;

      // FASE 1: Rebasar la entrada del cajón abriéndose en sentido opuesto
      if (faseEstacionamiento == 1) {
        ang = (ladoCajonParqueo == 1) ? 105 : 75; // Se abre al lado contrario del cajón
        vel = 110;   
        if (dF < 20 || tiempoTranscurrido > 1600) { 
          faseEstacionamiento = 2;
          tiempoInicioEstacionamiento = millis();
        }
      }
      // FASE 2: Freno total y quiebre del servo apuntando hacia el cajón detectado
      else if (faseEstacionamiento == 2) {
        ang = (ladoCajonParqueo == 1) ? 60 : 120; // Rueda hacia el cajón para meter la cola
        vel = 0;     
        if (tiempoTranscurrido > 400) {
          faseEstacionamiento = 3;
          tiempoInicioEstacionamiento = millis();
        }
      }
      // FASE 3: Reversa en diagonal hacia el interior del cajón
      else if (faseEstacionamiento == 3) {
        ang = (ladoCajonParqueo == 1) ? 60 : 120; 
        vel = -130;  
        
        // Detiene la diagonal si el sensor del lado del cajón nota que se acerca al fondo lateral
        long distanciaCierre = (ladoCajonParqueo == 1) ? dI : dD;
        if (distanciaCierre < 14 || tiempoTranscurrido > 2200) { 
          faseEstacionamiento = 4;
          tiempoInicioEstacionamiento = millis();
        }
      }
      // FASE 4: Contravolante en reversa para emparejar la trompa del Fischertechnik
      else if (faseEstacionamiento == 4) {
        ang = (ladoCajonParqueo == 1) ? 120 : 60; // Gira al revés para alinear el coche con la pista
        vel = -110;  
        if (tiempoTranscurrido > 1200) {
          faseEstacionamiento = 5; 
        }
      }
      // FASE 5: Estacionado perfecto y apagado automático
      else if (faseEstacionamiento == 5) {
        ang = 90;
        vel = 0;
      }
    }

    // 3. LÓGICA DE ESTACIONAMIENTO Y SEGURIDAD
    //S para detenerse en seco
    if (pwr == 'S') {
      faseEstacionamiento = 0; // Resetea el parqueo guiado si recibe parada externa
      vel = 0;   // Freno absoluto e inmediato del motor trasero
      ang = 90;  // Alineación recta de las manguetas
    }

    if (dF < 12 ) vel = 0;

    mover(vel, ang);

    // 4. TELEMETRÍA (Para el CSV de la Raspberry)
    Serial.print("D:");
    Serial.print(dF); Serial.print(",");
    Serial.print(dA); Serial.print(",");
    Serial.print(dI); Serial.print(",");
    Serial.println(dD);
  
  }
}