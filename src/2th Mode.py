import serial
import time

# --- CONFIGURACIÓN DE HARDWARE ---
SERIAL_PORT = "/dev/ttyUSB0" 
BAUDRATE = 115200

# =====================================================================
# 📍 COREOGRAFÍA DEL MODO 2 (Edita esto en la pista)
# =====================================================================
# Formato estricto: (Velocidad, Angulo, Tiempo_en_segundos, "Comentario")
# 
# Guía de Ángulos:
# - 86  : Totalmente Recto
# - 60  : Giro fuerte a la DERECHA
# - 115 : Giro fuerte a la IZQUIERDA
# =====================================================================

RUTINA_MANUAL = [
    #salida estacionamiento
    (-140, 86,  0.58,  "Retroceso estacionamiento"),
    (0,   60,  0.5,  "Pausa medicion"),
    (140, 60,  0.56,  "Giro Hacia afuera Corto(Derecha)"),
    (0,   120,  0.5,  "Pausa medicion"),
    (-140, 120,  0.5,  "Retroceso Acomodo(Derecha)"),
    (0,   60,  0.5,  "Pausa medicion"),
    (140, 60,  0.8,  "Giro Hacia afuera Largo(Derecha)"),
    (140, 120,  1,  "Endereso a recta(Derecha)"),
    #(250, 86,  0.6,  "1. Aceleración en recta inicial(prueba)"),
    #1ra vuelta
    (250, 86,  0.6,  "1. Aceleración en recta inicial"),
    (180, 60,  1.8,  "2. Toma de la Curva 1 (Derecha)"),
    (250, 86,  2.8,  "3. Recta media"),
    (180, 60,  1.62,  "2. Toma de la Curva 2 (Derecha)"),
    (250, 86,  2.5,  "3. Recta media"),
    (180, 60,  1.62,  "2. Toma de la Curva 3 (Derecha)"),
    (250, 86,  2.2,  "3. Recta media"),
    (180, 60,  1.62,  "2. Toma de la Curva 4 (Derecha)"),
    (250, 86,  0.8,  "3. Recta corta"),
    #2da vuelta
    (250, 86,  1.2,  "1. Aceleración en recta inicial"),
    (180, 60,  1.6,  "2. Toma de la Curva 1 (Derecha)"),
    (250, 86,  2.6,  "3. Recta media"),
    (180, 60,  1.62,  "2. Toma de la Curva 2 (Derecha)"),
    (250, 86,  2,  "3. Recta media"),
    (180, 60,  1.62,  "2. Toma de la Curva 3 (Derecha)"),
    (250, 86,  2.4,  "3. Recta media"),
    (180, 60,  1.62,  "2. Toma de la Curva 4 (Derecha)"),
    (250, 86,  0.8,  "3. Recta corta"),
    #3ra vuelta
    (250, 86,  1.2,  "1. Aceleración en recta inicial"),
    (180, 60,  1.6,  "2. Toma de la Curva 1 (Derecha)"),
    (250, 86,  2.6,  "3. Recta media"),
    (180, 60,  1.62,  "2. Toma de la Curva 2 (Derecha)"),
    (250, 86,  2.4,  "3. Recta media"),
    (180, 60,  1.62,  "2. Toma de la Curva 3 (Derecha)"),
    (250, 86,  2.4,  "3. Recta media"),
    (180, 60,  1.58,  "2. Toma de la Curva 4 (Derecha)"),
    (250, 86,  1.2,  "3. Recta corta"),
    #Entrada Estacionamiento
    (-140, 120,  0.8,  "Retroceso Entrada estacionamiento(Izquierda)"),
    (0,   86,  0.5,  "Pausa medicion"),
    (-140, 86,  0.4,  "Retroceso Acomodo(Izquierda)"),
    #(0,   60,  0.5,  "Pausa medicion"),
    #(-140, 60,  0.56,  "Giro Hacia adentro Largo(Derecha)"),
    #(0,   120,  0.5,  "Pausa medicion"),
    #(140, 120,  0.4,  "Giro hacia adentro Corto(Derecha)"),
    #(0,   60,  0.5,  "Pausa medicion"),
    #(-140, 60,  0.8,  "Endereso a Estacionamiento"),
    #Archivero de Comandos
    #(150, 115, 0.4,  "4. Maniobra de evasión (Giro Izq)"),
    #(150, 60,  0.4,  "5. Recuperación al centro (Giro Der)"),
    #(250, 86,  1.5,  "6. Recta larga hacia la meta"),
    #(-200,86,  0.2,  "7. Contra-impulso de freno (Reversa)"),
    (0,   86,  0.1,  "8. Apagado de motores")
]

# =====================================================================


class WROCoreografia:
    def __init__(self):
        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=0.1)
            self.serial_enabled = True
            time.sleep(2)
        except Exception as e:
            print(f"[ERROR] Sin Arduino: {e}")
            self.serial_enabled = False

        print("[SISTEMA] MODO 2: COREOGRAFÍA MANUAL CARGADA.")

    def esperar_boton(self):
        """Bucle infinito que bloquea el auto hasta que se presione el botón"""
        print("\n[READY] Esperando pulsador para iniciar secuencia...\n")
        
        # Endereza las ruedas y frena motores mientras espera
        if self.serial_enabled:
            self.ser.write(b"<0,86>\n")

        while True:
            if self.serial_enabled and self.ser.in_waiting > 0:
                linea = self.ser.readline().decode('utf-8', errors='ignore').strip()
                if linea == "BTN:1":
                    print("\n[GO] ¡BOTÓN DETECTADO! Lanzando coreografía...\n")
                    self.ser.reset_output_buffer()
                    break
            time.sleep(0.02)

    def ejecutar_rutina(self):
        """Lee la lista RUTINA_MANUAL paso a paso y la ejecuta"""
        
        for paso in RUTINA_MANUAL:
            velocidad = paso[0]
            angulo = paso[1]
            duracion = paso[2]
            descripcion = paso[3]

            print(f"> Ejecutando: {descripcion} | Vel: {velocidad} | Ang: {angulo} | Tiempo: {duracion}s")

            # 1. Enviar el comando a los motores y servos
            if self.serial_enabled:
                comando = f"<{velocidad},{angulo}>\n"
                self.ser.write(comando.encode('utf-8'))

            # 2. Mantener esa acción por los segundos indicados
            time.sleep(duracion)

        # Al terminar la lista, asegurar que el auto se apague
        print("\n[FIN] Coreografía completada. Apagando sistemas.")
        if self.serial_enabled:
            self.ser.write(b"<0,86>\n")
            self.ser.close()

    def run(self):
        # Secuencia de saludo de servos para confirmar inicio
        if self.serial_enabled:
            self.ser.write(b"<0,120>\n")
            time.sleep(0.3)
            self.ser.write(b"<0,60>\n")
            time.sleep(0.3)
            self.ser.write(b"<0,86>\n")

        # 1. Quedarse esperando el botón
        self.esperar_boton()
        
        # 2. Cuando se presione, disparar la rutina
        self.ejecutar_rutina()


if __name__ == "__main__":
    bot = WROCoreografia()
    bot.run()