import cv2
import numpy as np
import serial
import time
import threading

SERIAL_PORT = "/dev/ttyUSB0" 
BAUDRATE = 115200

class WROPrimitivoBlindado:
    def __init__(self):
        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=0.1)
            self.serial_enabled = True
            time.sleep(2)
        except Exception as e:
            print(f"[ERROR] Sin Arduino: {e}")
            self.serial_enabled = False

        self.running = True
        self.estado_general = "ESPERA"
        self.boton_presionado = False
        self.start_time = None
        
        # Variables de Control
        self.current_speed = 0
        self.current_angle = 86
        
        # Conteo y Sentido
        self.SENTIDO_GIRO = "AUTO"
        self.vueltas_completadas = 0
        self.curvas_superadas = 0
        self.en_curva = False
        self.tiempo_ultima_curva = time.time()
        
        self.score_muro_frontal = 0
        
        # Control de visualización (False para competir de forma autónoma)
        self.VER_PANTALLAS = True 
        
        print("[SISTEMA] Modo 1 Primitivo Blindado Inicializado.")

    def read_serial_data(self):
        while self.running and self.serial_enabled:
            try:
                if self.ser.in_waiting > 0:
                    linea = self.ser.readline().decode('utf-8', errors='ignore').strip()
                    if linea == "BTN:1":
                        self.boton_presionado = True
            except:
                pass
            time.sleep(0.02)

    def process_vision(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1) # Cero lag

        kernel = np.ones((3, 3), np.uint8)

        while self.running:
            ret, frame = cap.read()
            if not ret: continue
            
            current_time = time.time()
            tiempo_en_carrera = current_time - self.start_time if self.start_time else 0

            # 1. ENFOQUE EXCLUSIVO EN LA PISTA (Filtrando el techo)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Recortamos una franja de la pista (Filas 60 a 150 del video original)
            roi_pista = blur[60:150, :]
            _, binarizada = cv2.threshold(roi_pista, 95, 255, cv2.THRESH_BINARY)
            binarizada = cv2.morphologyEx(binarizada, cv2.MORPH_OPEN, kernel)
            
            # 2. SEPARACIÓN DE HORIZONTE Y ESCANEO (Dentro de la pista)
            # Horizonte libre (pista lejana): filas superiores del recorte
            horizonte = binarizada[0:25, :] 
            # Línea de manejo (pista cercana): fila inferior del recorte
            linea_escaneo = binarizada[65, :] 

            # 3. DETECCIÓN DE MURO FRONTAL (Detección de Esquina)
            caja_central = binarizada[30:70, 120:200]
            ratio_oscuro = np.mean(caja_central == 0)
            
            # ESCENARIO PROBLEMATICO 2 (Muro interno al arrancar): 
            # Si lleva menos de 1.5 segundos corriendo, forzamos que no detecte muro frontal
            # Esto evita que confunda la pared lateral cercana con el final de la recta.
            if self.estado_general == "CARRERA" and tiempo_en_carrera < 1.5:
                es_muro_frontal = False
            else:
                es_muro_frontal = ratio_oscuro > 0.55

            # 4. ESCANEO DE RAYOS LATERALES
            muro_izq = -1
            muro_der = -1
            for x in range(160, -1, -1):
                if linea_escaneo[x] == 0: muro_izq = x; break
            for x in range(160, 320):
                if linea_escaneo[x] == 0: muro_der = x; break

            # =======================================================
            # 5. MÁQUINA DE ESTADOS REACCIONARIA
            # =======================================================
            if self.SENTIDO_GIRO == "AUTO" and self.estado_general == "CARRERA":
                blancos_izq = np.sum(horizonte[:, :160] == 255)
                blancos_der = np.sum(horizonte[:, 160:] == 255)
                    
                if blancos_der > blancos_izq: 
                    self.SENTIDO_GIRO = "DERECHA"
                    print("\n[>>] HORARIO DETECTADO (DERECHA) [>>]\n")
                else: 
                    self.SENTIDO_GIRO = "IZQUIERDA"
                    print("\n[<<] ANTIHORARIO DETECTADO (IZQUIERDA) [<<]\n")
            
            if es_muro_frontal:

                # B) CONTEO DE VUELTAS REALES (4 esquinas = 1 vuelta)
                if not self.en_curva and (current_time - self.tiempo_ultima_curva > 2):
                    self.en_curva = True
                    self.tiempo_ultima_curva = current_time
                    self.curvas_superadas += 1
                    
                    if self.curvas_superadas % 4 == 0:
                        self.vueltas_completadas += 1
                        print(f"\n[OK] VUELTA {self.vueltas_completadas}/3 COMPLETADA \n")
                        
                        if self.vueltas_completadas >= 3:
                            self.estado_general = "RETORNO_A_META"

                # C) ÁNGULO DETERMINADO DE GIRO FIJO
                if self.SENTIDO_GIRO == "DERECHA":   self.current_angle = 70
                elif self.SENTIDO_GIRO == "IZQUIERDA": self.current_angle = 104
                else:                                  self.current_angle = 86
                
                self.current_speed = 180 # Velocidad segura en curva

            else:
                # D) NAVEGACIÓN EN RECTA (Control Proporcional con Zona Muerta)
                self.current_speed = 250 
                
                # Calculamos el centro estimado de la pista
                if muro_izq != -1 and muro_der != -1:   centro_pista = (muro_izq + muro_der) // 2
                elif muro_izq != -1:                    centro_pista = muro_izq + 80
                elif muro_der != -1:                    centro_pista = muro_der - 80
                else:                                   centro_pista = 160

                error = 160 - centro_pista
                
                # ZONA MUERTA GRANDE (22 píxeles): Si está cerca del centro, va recto (86). No tiembla.
                if abs(error) < 22:
                    self.current_angle = 86
                else:
                    # Si se desvía, aplica una corrección proporcional suave basada en el error
                    # Multiplicamos por 0.15 para que el ajuste sea progresivo y no dé un golpe brusco
                    correccion_suave = int(error * 0.15)
                    angulo_prop = 86 + correccion_suave
                    
                    # Limitamos el volante en recta a rangos que no causen zigzag (74 a 98)
                    self.current_angle = max(74, min(98, angulo_prop))

                # Candado de liberación de curva
                if current_time - self.tiempo_ultima_curva > 3:
                    self.en_curva = False

            if self.VER_PANTALLAS:
                cv2.imshow("Vision Procesada", binarizada)
                if cv2.waitKey(1) & 0xFF == ord('q'): self.running = False

            time.sleep(0.01)
        cap.release()

    def main_loop(self):
        if self.serial_enabled:
            self.ser.write(b"<0,120>\n")
            time.sleep(0.4)
            self.ser.write(b"<0,60>\n")
            time.sleep(0.4)
            self.ser.write(b"<0,86>\n")
            self.ser.write(b"<0,86>\n")

   
        threading.Thread(target=self.read_serial_data, daemon=True).start()
        threading.Thread(target=self.process_vision, daemon=True).start()

        print("\n[SISTEMA] ESPERANDO BOTÓN PARA INICIAR...\n")
        
        while self.running:
            if self.estado_general == "ESPERA":
                if self.boton_presionado:
                    print("[START] Botón detectado.")
                    self.start_time = time.time()
                    
                    # ESCENARIO PROBLEMATICO 1: Si inicia pegado al muro frontal de frente
                    # Evaluamos si la cámara ya registra el muro negro antes de arrancar
                    if self.en_curva == True: # Significa que detectó bloqueo visual previo
                        print("[DESPEGUE] Muro al frente. Retrocediendo...")
                        if self.serial_enabled: self.ser.write(b"<-160,86>\n")
                        time.sleep(1) # Reversa de medio segundo
                        if self.serial_enabled: self.ser.write(b"<0,86>\n")
                        time.sleep(0.1)
                    
                    if self.serial_enabled: self.ser.reset_output_buffer()
                    self.estado_general = "CARRERA"
                    self.start_time = time.time()
                else:
                    time.sleep(0.05)

            elif self.estado_general == "CARRERA":
                if self.serial_enabled:
                    paquete = f"<{self.current_speed},{self.current_angle}>\n"
                    self.ser.write(paquete.encode())
                time.sleep(0.04)

            elif self.estado_general == "RETORNO_A_META":
                # Cruza la meta y frena con contra-impulso
                if self.serial_enabled:
                    self.ser.write(b"<200,86>\n")
                    time.sleep(0.4)
                    self.ser.write(b"<-200,86>\n")
                    time.sleep(0.15)
                    self.ser.write(b"<0,86>\n")
                print("[FIN] Vuelta 3 completada con éxito.")
                self.running = False

        if self.serial_enabled: self.ser.close()

if __name__ == "__main__":
    bot = WROPrimitivoBlindado()
    bot.main_loop()