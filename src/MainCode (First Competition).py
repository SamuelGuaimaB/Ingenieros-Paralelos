import cv2
import os
import numpy as np
import serial
import time
import threading

class PIDController:
    def __init__(self, kp, ki, kd, setpoint=160): 
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.prev_error = 0
        self.integral = 0

    def compute(self, current_value, dt):
        error = self.setpoint - current_value
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt > 0 else 0
        self.prev_error = error
        return (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)

class WROAutonomousCar:
    def __init__(self, serial_port='/dev/ttyACM0', baudrate=115200):
        self.ser = serial.Serial(serial_port, baudrate, timeout=0.1)
        time.sleep(2)
        
        # --- CONFIGURACIÓN ESTRATÉGICA ---
        self.SENTIDO_GIRO = "AUTO" # Cambiar a "DERECHA" si la pista lo requiere
        self.memoria_muro_exterior = "NINGUNO"
        self.MITAD_ANCHO_PISTA_PX = 140 # Píxeles estimados desde un muro hasta el centro
        
        # --- VARIABLES DE REGLAMENTO WRO ---
        self.vueltas_completadas = 0
        self.curvas_superadas = 0
        self.en_curva = False
        
        self.ultimo_tiempo_curva = time.time()
        
        # PID más agresivo en P para que reaccione rápido a un solo muro
        self.pid = PIDController(kp=0.07, ki=0.000, kd=0.20) 
        self.running = True
        
        self.centro_suavizado = 160.0
        
        self.current_speed = 0
        self.current_angle = 86 
        
        # --- NUEVAS VARIABLES PARA MODO Y ULTRASONIDO ---
        self.distancia_us = 200      # Distancia leída del Arduino
        self.modo_obstaculos = False # Falso = Modo 1 (Rápido), Verdadero = Modo 2 (Obstáculos)
        self.start_time = time.time()# Para ignorar el garaje al inicio
        
        self.estado_general = "INICIO"
        
        self.muro_izq_global = -1
        self.muro_der_global = -1
        
        self.estado_general = "ESPERA" # Cambiamos de INICIO a ESPERA
        self.boton_presionado = False  # Bandera del botón
        
        self.VER_PANTALLAS = False
        
        print(f"[SISTEMA] Algoritmo Raycasting Iniciado. Giro ciego: {self.SENTIDO_GIRO}")
       
    def read_serial_data(self):
        """Hilo dedicado a leer lo que envía el Arduino"""
        while self.running:
            try:
                if self.ser.in_waiting > 0:
                    linea = self.ser.readline().decode('utf-8').strip()
                    if linea.startswith("US:"):
                        # Extraemos el número después de "US:"
                        self.distancia_us = int(linea.split(":")[1])
                    elif linea == "BTN:1":
                        self.boton_presionado = True
            except:
                pass
            time.sleep(0.01)
    
    def process_vision(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)#medir esta tolerancia
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        
        # Elemento estructurante para limpieza digital de ruido (Morfología)
        kernel = np.ones((5, 5), np.uint8)
        last_time = time.time()

        while self.running:
            ret, frame = cap.read()
            if not ret: continue

            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            #MEMORIA DE CHASIS
            tiempo_ultimo_obstaculo = 0
            memoria_tipo_obstaculo = "NINGUNO"
            
            # =======================================================
            # 1. OPENCV: PROCESAMIENTO Y UMBRAL FIJO
            # =======================================================
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (7, 7), 0)
            
            # Recortamos una franja clave (ajusta esto si la cámara sube o baja)
            y_arriba = 80
            y_abajo = 140
            roi_blur = blur[y_arriba:y_abajo, 0:320]
            
            # Blanco brillante (Piso) = 255. Oscuro (M0uro) = 0.
            _, binarizada = cv2.threshold(roi_blur, 60, 255, cv2.THRESH_BINARY)#medir esta tolerancia
            
            # Extraemos la misma franja pero en color
            roi_color_muros = frame[y_arriba:y_abajo, 0:320]
            hsv_muros = cv2.cvtColor(roi_color_muros, cv2.COLOR_BGR2HSV)
            
            # Rango del magenta/rosa fluorescente (Ajusta estos valores si es necesario)
            lower_magenta = np.array([130, 80, 80])
            upper_magenta = np.array([175, 255, 255])
            mask_magenta = cv2.inRange(hsv_muros, lower_magenta, upper_magenta)
            
            # INYECCIÓN VISUAL: Forzamos que todo lo que sea magenta se vuelva NEGRO (Muro) en la binarizada
            binarizada[mask_magenta == 255] = 0
            
            # =======================================================
            # 1.5 DETECCIÓN DE OBSTÁCULOS (ROJO Y VERDE)
            # =======================================================
            # Usamos una franja similar para que las coordenadas X coincidan
            roi_color = frame[80:240, 0:320] 
            hsv = cv2.cvtColor(roi_color, cv2.COLOR_BGR2HSV)
            
            # Rangos VERDE (Ajusta estos números viendo la ventana "Filtro VERDE")
            lower_green = np.array([35, 60, 50])
            upper_green = np.array([85, 255, 255])
            mask_green = cv2.inRange(hsv, lower_green, upper_green)
            
            # Rangos ROJO (Ajusta estos números viendo la ventana "Filtro ROJO")
            lower_red1 = np.array([0, 100, 80])
            upper_red1 = np.array([5, 255, 255])
            lower_red2 = np.array([175, 100, 80])
            upper_red2 = np.array([180, 255, 255])
            mask_red = cv2.bitwise_or(cv2.inRange(hsv, lower_red1, upper_red1),
                                      cv2.inRange(hsv, lower_red2, upper_red2))
            
            mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel)
            mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_CLOSE, kernel)
            
            mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
            mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_CLOSE, kernel)
            
            obstaculo_tipo = "NINGUNO"
            obstaculo_cx = 160
            area_max_obs = 0
            
            lista_obstaculos = []
            
            contornos_v, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for c in contornos_v:
                area = cv2.contourArea(c)
                x, y, w, h = cv2.boundingRect(c)
                if area > 400 and w < 260 and area > area_max_obs:
                    lista_obstaculos.append({"x": x, "w": w, "tipo": "VERDE", "area": area})
                    if area > area_max_obs:
                        area_max_obs = area
                        obstaculo_cx = x + (w // 2)
                        obstaculo_tipo = "VERDE"
                        
            contornos_r, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for c in contornos_r:
                area = cv2.contourArea(c)
                x, y, w, h = cv2.boundingRect(c)
                if area > 400 and w < 260 and area > area_max_obs:
                    lista_obstaculos.append({"x": x, "w": w, "tipo": "ROJO", "area": area})
                    if area > area_max_obs:
                        area_max_obs = area
                        obstaculo_cx = x + (w // 2)
                        obstaculo_tipo = "ROJO"
                    
            if obstaculo_tipo != "NINGUNO":
                tiempo_ultimo_obstaculo = current_time
                memoria_tipo_obstaculo = obstaculo_tipo
                
            # =======================================================
            # 1.6 LA CAPA DE INVISIBILIDAD (Hack de Muros)
            # =======================================================
            for obs in lista_obstaculos:
                cx_temp = obs["x"] + (obs["w"] // 2)
                x_inicio = max(0, obstaculo_cx - 20)
                x_fin = min(320, obstaculo_cx + 20)
                binarizada[:, x_inicio:x_fin] = 255
                
            if self.VER_PANTALLAS:
                cv2.imshow("Filtro VERDE", mask_green)
                cv2.imshow("Filtro ROJO", mask_red)
                cv2.imshow("Vision Binarizada", binarizada)
                cv2.waitKey(1)
            
            # =======================================================
            # 2. ALGORITMO DE RAYCASTING (Escanear la línea media)
            # =======================================================
            alto_roi, ancho_roi = binarizada.shape
            linea_escaneo = binarizada[alto_roi // 2, :] # Extraer la fila central de la franja
            
            muro_izq = -1
            muro_der = -1
            
            # Disparar rayo hacia la izquierda desde el centro (160 a 0)

            # =======================================================
            # 3. MÁQUINA DE ESTADOS MATEMÁTICA
            # =======================================================
            centro_pista_x = 160
            estado = "DESCONOCIDO"

            franja_central = linea_escaneo[150:170]
            if np.sum(franja_central == 0) > 10:
                estado = "MURO_FRONTAL"
            else:
                for x in range(160, -1, -1):
                    if linea_escaneo[x] == 0: 
                        muro_izq = x; break
                
                for x in range(160, ancho_roi):
                    if linea_escaneo[x] == 0: 
                        muro_der = x; break
                
                self.muro_izq_global = muro_izq
                self.muro_der_global = muro_der
                
                # Máquina de estados normal
                if muro_izq != -1 and muro_der != -1:
                    centro_pista_x = (muro_izq + muro_der) // 2
                elif muro_izq != -1 and muro_der == -1:
                    centro_pista_x = muro_izq + self.MITAD_ANCHO_PISTA_PX
                    estado = "MURO_IZQ"
                elif muro_izq == -1 and muro_der != -1:
                    centro_pista_x = muro_der - self.MITAD_ANCHO_PISTA_PX
                    estado = "MURO_DER"
                else:
                    estado = "CEGUERA_BLANCA"
                    
            # =======================================================
            # 3.3 INYECCIÓN DE EVASIÓN (REPROGRAMACIÓN DEL PID)
            # =======================================================
            
            # Se Calcula cuánto tiempo ha pasado desde que dejamos de ver el bloque
            tiempo_ciego = current_time - tiempo_ultimo_obstaculo
            
            en_memoria_evasion = tiempo_ciego < 1
            
            tipo_evasion_activa = obstaculo_tipo if obstaculo_tipo != "NINGUNO" else memoria_tipo_obstaculo
            
            evadiendo = (obstaculo_tipo != "NINGUNO" or en_memoria_evasion)
            
            # Solo evadimos si vemos un obstáculo
            if evadiendo:
                
                #DISTANCIA_EVASION = 170
                
                if tipo_evasion_activa == "ROJO":
                    # Regla WRO: Pasar por la DERECHA del bloque rojo
                    centro_pista_x = 210 #260 #obstaculo_cx + DISTANCIA_EVASION #medir esta tolerancia
                    estado = "EVADIENDO_ROJO" if obstaculo_tipo != "NINGUNO" else "MEMORIA_ROJO"
                    
                elif tipo_evasion_activa == "VERDE":
                    # Regla WRO: Pasar por la IZQUIERDA del bloque verde
                    centro_pista_x = 40
               
                #60 #obstaculo_cx - DISTANCIA_EVASION #medir esta tolerancia
                    estado = "EVADIENDO_VERDE" if obstaculo_tipo != "NINGUNO" else "MEMORIA_VERDE"
                    
                # ESCUDO ANTI-MURO: Evita chocar contra los bordes de la pista al esquivar
                centro_pista_x = max(45, min(350, centro_pista_x)) #300 #medir esta tolerancia


            # =======================================================
            # 3.5 AUTODETECCIÓN DE SENTIDO (Solo se ejecuta 1 vez)
            # ======================================================= 
            es_vertice_curva = estado in ["MURO_FRONTAL"]
            
            if self.SENTIDO_GIRO == "AUTO" and self.estado_general == "CARRERA":
                # Cortamos la imagen para mirar "a lo lejos" (solo la mitad superior)   
                horizonte = binarizada[:30, :] 
                
                blancos_izq = np.sum(horizonte[:, :160] == 255)
                blancos_der = np.sum(horizonte[:, 160:] == 255)
                    
                if blancos_der > blancos_izq:
                    self.SENTIDO_GIRO = "DERECHA"
                    print("\n[!!!] HORIZONTE LIBRE A LA DERECHA -> HORARIO CONFIRMADO [!!!]\n")
                else:
                    self.SENTIDO_GIRO = "IZQUIERDA"
                    print("\n[!!!] HORIZONTE LIBRE A LA IZQ -> ANTIHORARIO CONFIRMADO [!!!]\n")
                    
            # =======================================================
            # 3.6 CONTEO DE VUELTAS (Reglamento WRO)
            # =======================================================
            perdio_muro_interior = (self.SENTIDO_GIRO == "DERECHA" and muro_der == -1) or (self.SENTIDO_GIRO == "IZQUIERDA" and muro_izq == -1)
           
            es_vertice_curva = estado == "MURO_FRONTAL"
            
            #SÍNTOMA A: EL AUTO CUENTA VUELTAS DE MÁS (Se frena a mitad de carrera)
            # Causa: El auto derrapa en la curva y la cámara parpadea, contando 2 curvas en vez de 1.
            # Solución: Sube el 0.6 a 0.8 o 0.9. Esto hace que el auto se vuelva "sordo" durante todo el derrape.
            # Consideramos que entró a una curva si perdió un muro o chocó de frente
            if es_vertice_curva or perdio_muro_interior:
                # El candado cronometrado: Deben haber pasado al menos 3.5 segundos desde la última esquina
                tiempo_cooldown = 1.5 if self.modo_obstaculos else 4
                
                if not self.en_curva and (current_time - self.ultimo_tiempo_curva > tiempo_cooldown):
                    self.en_curva = True
                    self.ultimo_tiempo_curva = current_time
                    self.curvas_superadas += 1
                    
                    # Si ya pasó 4 esquinas, es 1 vuelta completa
                    if self.curvas_superadas % 4 == 0:
                        self.vueltas_completadas += 1
                        print(f"\n[] VUELTA {self.vueltas_completadas}/3 COMPLETADA []\n")
                        
                        if self.vueltas_completadas >= 3:
                            if self.modo_obstaculos:
                                print("\n[RETO] 3 Vueltas. Iniciando búsqueda de estacionamiento...\n")
                                self.estado_general = "PRE_PARKING" # Dispara la maniobra en main_loop
                            else:
                                print("\n[RETO] Modo 1 Completado. Frenando...\n")
                                self.estado_general = "FIN"
                            
            else:
                #SÍNTOMA B: EL AUTO CUENTA VUELTAS DE MENOS (Da 4 vueltas y no frena nunca)
                # Causa: Tu auto es tan rápido en la recta que llega a la siguiente curva antes de que el candado se abra.
                # Solución: Baja el 0.8 a 0.5 o 0.4. Esto obliga al candado a abrirse rapidísimo apenas pisa la recta.
                # Exigimos ver la recta estabilizada por 0.5s antes de permitir otra curva
                tiempo_desbloqueo = 2.0 if self.modo_obstaculos else 1
                
                if current_time - self.ultimo_tiempo_curva > tiempo_desbloqueo:
                    self.en_curva = False
                
            # =======================================================
            # 4. DIRECCIÓN Y VELOCIDAD (CON ZONA MUERTA)
            # =======================================================
            if estado == "MURO_FRONTAL" and obstaculo_tipo == "NINGUNO":
                # Evadir a toda costa la colisión frontal
                #anadir orientacion dependiendo del sentido
                    
                if self.SENTIDO_GIRO == "DERECHA" or self.SENTIDO_GIRO == "IZQUIERDA":
                    self.current_angle = 60 if self.modo_obstaculos else 60
                #elif self.SENTIDO_GIRO == "IZQUIERDA":
                #    self.current_angle = 110 if self.modo_obstaculos else 100
                else:
                    # Si aún está en "AUTO" y se topa con el muro, gira hacia donde haya hueco
                    if muro_der == -1 or muro_der > 240:
                        self.current_angle = 60 if self.modo_obstaculos else 60
                    elif muro_izq == -1 or muro_izq < 80:
                        self.current_angle = 60 if self.modo_obstaculos else 60
                    else:
                        self.current_angle = 86
                self.current_speed = 220
                
            else:
                error_absoluto_real = 160 - centro_pista_x
                
                # Zona Muerta Generosa (150 píxeles)
                zona_muerta = 55 if ("EVADIENDO" in estado or "MEMORIA" in estado) else 125#150medir esta tolerancia
                
                if abs(error_absoluto_real) < zona_muerta: 
                    self.current_angle = 86
                    self.pid.integral = 0
                else:
                    # AGRESIVIDAD DEL VOLANTE
                    if evadiendo:
                        #Esto le quita la duda y da un volantazo seguro y firme.
                        self.pid.kp = 0.15
                        self.current_speed = 200
                    else:
                        self.pid.kp = 0.08 if estado == "CENTRADO" else 0.15
                        self.current_speed = 250
                    
                    correccion_pid = self.pid.compute(centro_pista_x, dt)
                    angulo_pid = int(86 + correccion_pid)
                    
                    # --- LA MAGIA DUAL-RATE ---
                    if evadiendo:
                        self.current_angle = max(60, min(120, angulo_pid))
                    elif estado == "CENTRADO":
                        # En recta: Topes físicos virtuales (Solo 10 grados de libertad)
                        # Esto destruye el zig-zag inmediatamente.
                        self.current_angle = max(76, min(96, angulo_pid))
                    else:
                        # Si perdió un muro, está entrando a curva: Liberamos el volante
                        self.current_angle = max(70, min(110, angulo_pid))
                
                # Velocidad
                if estado == "CENTRADO" and abs(error_absoluto_real) < 20:
                    self.current_speed = 250
                else:
                    self.current_speed = 250

            # Debug visual en consola
            if int(current_time * 10) % 5 == 0:
                print(f"| Obs: {obstaculo_tipo: <7} | Estado: {estado: <15} | Muros: [I:{muro_izq} D:{muro_der}] | Vel: {self.current_speed} | Ángulo: {self.current_angle}° |")

            time.sleep(0.01)
        cap.release()
        
    def main_loop(self):
        self.ser.write(b"<0,120>\n")
        time.sleep(0.5)
        self.ser.write(b"<0,60>\n")
        time.sleep(0.5)
        self.ser.write(b"<0,86>\n")
        
        # Iniciar el hilo de lectura del Arduino
        rt = threading.Thread(target=self.read_serial_data, daemon=True)
        rt.start()
            
        vt = threading.Thread(target=self.process_vision)
        vt.start()
        
        print("\n[SISTEMA] INICIALIZADO. ESPERANDO PULSADOR PARA COMENZAR...\n")
        
        # ==========================================
        # ESTADO DE ESPERA (Bucle de inactividad)
        # ==========================================
        while self.estado_general == "ESPERA" and self.running:
            if self.boton_presionado:
                print("\n[!] BOTÓN PRESIONADO. LEYENDO SENSORES [!]")
                time.sleep(0.5) # Damos medio segundo para que apartes la mano
                
                if self.distancia_us < 30: 
                    self.modo_obstaculos = True
                    self.estado_general = "INICIO_GARAJE"
                    print("[MODO] MODO OBSTÁCULOS (MODO 2) ACTIVADO\n")
                else:
                    self.modo_obstaculos = False
                    self.estado_general = "CARRERA"
                    print("[MODO] MODO VELOCIDAD (MODO 1) ACTIVADO\n")
                    
                self.start_time = time.time() # Reiniciamos el reloj de inicio
                break # Rompe el bucle de espera y entra a la carrera
            time.sleep(0.1)
        
        try:
            while self.running:
                # --------------------------------------------------
                # ESTADO: SALIDA INTELIGENTE DEL GARAJE V3 (Antichoque)
                # --------------------------------------------------
                if self.estado_general == "INICIO_GARAJE":
                    print("\n[MANIOBRA] Iniciando secuencia. Vaciando búfer serial...")
                    self.ser.reset_output_buffer() # ELIMINA comandos viejos del PID atascados
                    
                    # 1. RETROCESO ABSOLUTO (Prueba de hardware)
                    # NOTA: Si con esto el auto sigue avanzando, DEBES revisar el código de tu Arduino.
                    # Significa que tu Arduino no sabe qué hacer con el signo "-" y lo omite.
                    t_reversa = time.time()
                    while (time.time() - t_reversa) < 1: 
                        if 0 < self.distancia_us <= 5:
                            print(f"[US] Distancia límite trasera alcanzada ({self.distancia_us}cm). Frenando.")
                            break
                            
                        # Bajamos el PWM de -200 a -165. En reversa corta, menos velocidad es más precisión.
                        self.ser.write(b"<-150,86>\n") 
                        time.sleep(0.05)
                    
                    self.ser.write(b"<150,86>\n")
                    time.sleep(0.1)
                    
                    # 2. FRENO TOTAL Y ESCANEO
                    self.ser.write(b"<0,86>\n")
                    time.sleep(0.8) # Freno físico y estabilización de la cámara
                    
                    if self.muro_der_global == -1 or self.muro_der_global > 250:
                        print("-> Apertura a la DERECHA.")
                            
                        # B. PRE-GIRO: Apuntar las ruedas MIENTRAS ESTÁ FRENADO
                        self.ser.write(b"<0,70>\n") # 0 velocidad, máximo giro derecha
                        time.sleep(0.3) # Tiempo sagrado para que el servo físico llegue a la posición
                        
                        # C. Giro cerrado a baja velocidad (cierra el radio de giro)
                        t_giro = time.time()
                        while (time.time() - t_giro) < 1.0:
                            self.ser.write(b"<200,70>\n") # PWM reducido a 160
                            time.sleep(0.05)
                            
                        print("-> Arrastrando el chasis fuera del garaje...")
                        t_arrastre = time.time()
                        while (time.time() - t_arrastre) < 1.5: # Ajusta este tiempo (0.4 a 0.8)
                            self.ser.write(b"<200,70>\n") # MANTENEMOS el giro máximo
                            time.sleep(0.05)
                            
                        self.SENTIDO_GIRO = "DERECHA"
                        
                    elif self.muro_izq_global == -1 or self.muro_izq_global < 70:
                        print("-> Apertura a la IZQUIERDA.")
                            
                        # B. PRE-GIRO: Apuntar las ruedas
                        self.ser.write(b"<0,110>\n") # 0 velocidad, máximo giro izquierda
                        time.sleep(0.3)
                        
                        # C. Giro cerrado a baja velocidad
                        t_giro = time.time()
                        while (time.time() - t_giro) < 1.0:
                            self.ser.write(b"<200,110>\n")
                            time.sleep(0.05)
                        
                        print("-> Arrastrando el chasis fuera del garaje...")
                        t_arrastre = time.time()
                        while (time.time() - t_arrastre) < 1.5: # Ajusta este tiempo (0.4 a 0.8)
                            self.ser.write(b"<200,110>\n") # MANTENEMOS el giro máximo
                            time.sleep(0.05)
                        
                        self.SENTIDO_GIRO = "IZQUIERDA"
                        
                    else:
                        print("-> [ALERTA] Fallback: Salida Recta.")
                        t_fallback = time.time()
                        while (time.time() - t_fallback) < 0.8:
                            self.ser.write(b"<220,86>\n")
                            time.sleep(0.05)
                    
                    # 4. Transferencia limpia al PID
                    self.ser.reset_output_buffer() # Limpiar cualquier remanente de la maniobra
                    self.start_time = time.time() 
                    self.estado_general = "CARRERA"
                    print("[ESTADO] Maniobra completada. PID Activo.\n")
                    
                # --------------------------------------------------
                # ESTADO: CARRERA NORMAL (PID Activo)
                # --------------------------------------------------
                if self.estado_general == "CARRERA":
                    # El bucle normal que lee las variables de process_vision
                    paquete = f"<{self.current_speed},{self.current_angle}>\n"
                    self.ser.write(paquete.encode('utf-8'))
                    time.sleep(0.05)
                    
                # --------------------------------------------------
                # ESTADO: REBASE ANTES DE ESTACIONAR
                # --------------------------------------------------
                elif self.estado_general == "PRE_PARKING":
                    print("[MANIOBRA] Buscando activamente la entrada del garaje...")
                    # Avanzamos lento (145) para darle tiempo a la cámara de escanear los laterales
                    self.current_speed = 150
                    self.current_angle = 86
                    
                    # SOLUCIÓN AL ERROR DE MEDICIÓN:
                    # El carro avanza por la recta final mirando los muros laterales. 
                    # En cuanto uno de los muros cae a -1, significa que detectó el "vacío" o apertura del garaje.
                    if self.muro_der_global == -1 or self.muro_izq_global == -1:
                        lado_garaje = "DERECHA" if self.muro_der_global == -1 else "IZQUIERDA"
                        print(f"[GARAJE DETECTADO] Apertura a la {lado_garaje}. Midiendo distancia de despeje...")
                    
                        t_despeje = time.time()
                        while (time.time() - t_despeje) < 0.35:
                            self.ser.write(b"<150,86>\n")
                            time.sleep(0.05)
                    
                        print("[FRENO] Contra-impulso activo para anular inercia...")
                        self.ser.write(b"<-180,86>\n") 
                        time.sleep(0.15)
                        self.ser.write(b"<0,86>\n")
                        time.sleep(0.3)
                    
                        self.lado_estacionamiento = lado_garaje
                        self.estado_general = "PARKING_MANIOBRA"
                              
                # --------------------------------------------------
                # ESTADO: ESTACIONAMIENTO PARALELO ("S-Curve")
                # --------------------------------------------------
                elif self.estado_general == "PARKING_MANIOBRA":
                    lado = self.lado_estacionamiento
                    print(f"[MANIOBRA] Iniciando S-Curve asistida por Ultrasonido hacia la {lado}...")
                    
                    # =======================================================
                    # PASO 1: INSERCIÓN DE COLA (Giro máximo hacia el garaje)
                    # =======================================================
                    print("[PARKING] Paso 1: Introduciendo la parte trasera...")
                    angulo_insercion = 70 if lado == "DERECHA" else 110
                    
                    t_paso1 = time.time()
                    # Bajamos la velocidad de reversa a -130 para dar tiempo de reacción al sensor
                    while (time.time() - t_paso1) < 1.0:
                        # SOLUCIÓN AL GOLPE TRASERO: Si el ultrasonido detecta que estamos a 16 cm o menos 
                        # de la pared trasera del garaje, corta el paso 1 inmediatamente.
                        if self.distancia_us > 0 and self.distancia_us <= 16:
                            print(f"[US] Proximidad detectada ({self.distancia_us}cm). Interrumpiendo Paso 1.")
                            break
                        self.ser.write(f"<-150,{angulo_insercion}>\n".encode('utf-8'))
                        time.sleep(0.05)
                        
                    # =======================================================
                    # PASO 2: INSERCIÓN DE TROMPA (Contravolante inverso)
                    # =======================================================
                    print("[PARKING] Paso 2: Enderezando el chasis dentro del cajón...")
                    angulo_alineacion = 110 if lado == "DERECHA" else 70
                    
                    t_paso2 = time.time()
                    while (time.time() - t_paso2) < 1.2:
                        # Si nos acercamos peligrosamente al fondo (7 cm), clavamos los frenos
                        if self.distancia_us > 0 and self.distancia_us <= 5:
                            print(f"[US] Fondo del garaje alcanzado ({self.distancia_us}cm). Frenando reversa.")
                            break
                        self.ser.write(f"<-150,{angulo_alineacion}>\n".encode('utf-8'))
                        time.sleep(0.05)
                        
                    # =======================================================
                    # PASO 3: REINTEGRO Y CENTRADO FINAL (Acomodo de llantas)
                    # =======================================================
                    # SOLUCIÓN AL MAL REINTEGRO: Avanzamos un poco hacia adelante con ruedas rectas
                    # para despegar el auto de la pared del fondo y dejarlo perfectamente paralelo.
                    print("[PARKING] Paso 3: Avanzando para centrar y reintegrar el chasis...")
                    
                    t_paso3 = time.time()
                    while (time.time() - t_paso3) < 0.35:
                        self.ser.write(b"<150,86>\n")
                        time.sleep(0.05)
                        
                    # Apagado definitivo del sistema
                    self.ser.write(b"<0,86>\n")
                    self.estado_general = "FIN"
                    
                # --------------------------------------------------
                # ESTADO: APAGADO TOTAL
                # --------------------------------------------------
                elif self.estado_general == "FIN":
                    print("[COMPETENCIA] Misión finalizada con éxito.")
                    tiempo_final = time.time()
                    while (time.time() - tiempo_final) < 0.2:
                        paquete = f"<{self.current_speed},{self.current_angle}>\n"
                        self.ser.write(paquete.encode('utf-8'))
                        time.sleep(0.05)
                        
                    # 2. Freno activo para evitar derrape hacia la siguiente curva
                    self.ser.write(b"<-200,86>\n") # Pulso fuerte de reversa
                    time.sleep(0.15)               # Duración del pulso
                    self.ser.write(b"<0,86>\n")    # Parada total
                    
                    self.running = False
      
        except KeyboardInterrupt:
            self.running = False
        finally:
            self.ser.write(b"<0,86>\n") 
            vt.join()
            self.ser.close()

if __name__ == "__main__":
    bot = WROAutonomousCar(serial_port='/dev/ttyUSB0') # Verifica el puerto
    bot.main_loop()