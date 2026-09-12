#include <Servo.h>

// --- CONFIGURACIÓN DE PINES (Ajusta según tu shield o conexiones) ---
const int PIN_SERVO = 6;   // Pin de control del servo de dirección
const int PIN_ENA   = 3;   // Pin PWM para la velocidad del motor (Enable/Speed)
const int PIN_IN1   = 5;   // Dirección del motor A
const int PIN_IN2   = 4;   // Dirección del motor B
const int PIN_BTN   = 2;   // Pulsador físico de inicio

Servo direccionServo;
bool botonEnviado = false;

void setup() {
  Serial.begin(115200);
  
  direccionServo.attach(PIN_SERVO);
  pinMode(PIN_ENA, OUTPUT);
  pinMode(PIN_IN1, OUTPUT);
  pinMode(PIN_IN2, OUTPUT);
  pinMode(PIN_BTN, INPUT_PULLUP); // Botón con resistencia pull-up interna

  // Estado seguro inicial en el arranque
  direccionServo.write(86); // Ángulo recto neutral
  detenerMotores();
}

void loop() {
  // 1. Control del Botón de Inicio físico
  if (!botonEnviado && digitalRead(PIN_BTN) == LOW) {
    delay(50); // Pequeño filtro antirrebote (debounce)
    if (digitalRead(PIN_BTN) == LOW) {
      Serial.println("BTN:1"); // Mensaje que la Raspberry Pi está esperando
      botonEnviado = true;
    }
  }

  // 2. Procesamiento de Comandos Seriales desde la Raspberry Pi (<velocidad,angulo>)
  if (Serial.available() > 0) {
    char c = Serial.read();
    if (c == '<') {
      int velocidad = Serial.parseInt();
      int angulo = Serial.parseInt();
      
      // Aplicar comandos al hardware
      moverMotor(velocidad);
      direccionServo.write(constrain(angulo, 50, 122)); // Límites físicos del servo
    }
  }
}

void moverMotor(int vel) {
  // Limitar valores de PWM de los motores (-255 a 255)
  vel = constrain(vel, -255, 255);
  
  if (vel > 0) {
    // Marcha adelante
    digitalWrite(PIN_IN1, HIGH);
    digitalWrite(PIN_IN2, LOW);
    analogWrite(PIN_ENA, vel);
  } 
  else if (vel < 0) {
    // Reversa
    digitalWrite(PIN_IN1, LOW);
    digitalWrite(PIN_IN2, HIGH);
    analogWrite(PIN_ENA, abs(vel));
  } 
  else {
    // Freno / Detenido
    detenerMotores();
  }
}

void detenerMotores() {
  digitalWrite(PIN_IN1, LOW);
  digitalWrite(PIN_IN2, LOW);
  analogWrite(PIN_ENA, 0);
}
