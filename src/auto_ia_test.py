import cv2
import serial
import time
import csv
import numpy as np

# --- INTENTO DE CARGA DE MEDIAPIPE (Seguro) ---
try:
    import mediapipe as mp
    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision
    base_options = python.BaseOptions(model_asset_path='efficientdet_lite0.tflite')
    options = vision.ObjectDetectorOptions(base_options=base_options,score_threshold=0.4)
    detector = vision.ObjectDetector.create_from_options(options)
    USAR_IA = True
except Exception as e:
    print(f"Aviso: MediaPipe no disponible ({e}). Usando solo Vision de Colores.")
    USAR_IA = False

# --- CONFIGURACIÓN DE PISTA ---
archivo_log = "log_robot_wro.csv"
vueltas_totales = 0
en_meta = False
tiempo_ultima_vuelta = 0
memoria_pista = {}  # Formato: {tiempo: (comando, potencia)}
inicio_vuelta = time.time()

# --- CONEXIÓN SERIAL (Protegida) ---
try:
    # Intenta Raspberry (Linux) o Windows
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0.05)
except:
    try:
        ser = serial.Serial('COM3', 9600, timeout=0.05)
    except:
        print("AVISO: Arduino no detectado. Modo simulación.")
        ser = None

# --- CALIBRACIÓN DE COLORES HSV ---
ROJO = [(0, 120, 70), (10, 255, 255)]
VERDE = [(40, 70, 70), (80, 255, 255)]
MAGENTA = [(140, 70, 70), (170, 255, 255)]
NARANJA = [(5, 150, 150), (25, 255, 255)]
AZUL_SUELO = [(100, 150, 50), (130, 255, 255)]

def detectar_color(hsv, rango):
    mask = cv2.inRange(hsv, np.array(rango[0]), np.array(rango[1]))
    area = cv2.countNonZero(mask)
    if area > 1200:
        M = cv2.moments(mask)
        cx = int(M["m10"] / M["m00"]) if M["m00"] > 0 else 160
        return True, cx
    return False, 160

dist_F = 100.0
dist_A = 100.0
dist_I = 100.0
dist_D = 100.0

def actualizar_sensores():
    global dist_F, dist_A, dist_I, dist_D
    if ser and ser.in_waiting > 0:
        try:
            linea = ser.readline().decode('utf-8', errors='ignore').strip()
            if linea.startswith("D:"):
                # Quitamos el "D:" y separamos los 4 datos por las comas
                datos = linea.replace("D:", "").split(",")
                if len(datos) == 4:
                    dist_F = float(datos[0])
                    dist_A = float(datos[1])
                    dist_I = float(datos[2])
                    dist_D = float(datos[3])
        except Exception as e:
            pass # Si hay un error de lectura, mantiene el último valor seguro

# --- BUCLE PRINCIPAL ---
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320); cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

print(">>> SISTEMA INTEGRADO INICIADO")

try:
    print("Calibrando entorno... No mueva el robot.")
    for _ in range(20): # Intentar leer durante 2 segundos (20 * 0.1s)
    actualizar_sensores()
    time.sleep(0.1)

    # Simulamos que leemos el puerto para capturar la posición inicial
    # dist_F, dist_A, dist_I, dist_D deben venir de la lectura serial
    try:
        pared_frente = float(dist_F)
        pared_atras = float(dist_A)
    except:
        pared_frente, pared_atras = 100, 100 # Failsafe si no hay Arduino

    # DETECCIÓN: Si ambas paredes laterales están a menos de 40cm, estamos encajonados (Modo 2)
    if pared_frente < 40 and pared_atras < 40:
        MODO_COMPETENCIA = "OBSTACULOS_ESTACIONADO"
        VELOCIDAD_CRUCERO = "M"  # Más controlado para esquivar pilares
        vueltas_totales = 0      # Empezamos estacionados (Vuelta 0)
        print(">>> MODO DETECTADO: 2 - Obstáculos (Salida desde Cajón Magenta)")
    else:
        MODO_COMPETENCIA = "CARRERA_ABIERTA"
        SENTIDO_CIRCUITO = "INDETERMINADO" # Cambiará a 'HORARIO' o 'ANTIHORARIO'
        VELOCIDAD_CRUCERO = "H"  # ¡A tope desde el inicio!
        vueltas_totales = 1      # Arrancamos ya en pista corriendo
        print(">>> MODO DETECTADO: 1 - Carrera Abierta (Salida fluida)")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        t_actual = round(time.time() - inicio_vuelta, 1)
        
        actualizar_sensores() 
        
        comando = 'F'
        potencia = VELOCIDAD_CRUCERO # Se adapta automáticamente según la calibración inicial

        # Si estamos en el Modo Obstáculos, aplicamos la rutina de salida estacionada en la Vuelta 0
        if MODO_COMPETENCIA == "OBSTACULOS_ESTACIONADO" and vueltas_totales == 0:
            # El robot arranca suave para salir del cajón de paredes
            comando = 'F'
            potencia = 'L'
            # Una vez que el sensor trasero detecte que salimos del cajón (ej. > 30cm) 
            # pasamos a la carrera real
            if float(dist_A) > 30: 
                vueltas_totales = 1
                inicio_vuelta = time.time() # Sincronizamos cronómetro de memoria aquí
                print("¡Fuera del cajón! Iniciando Vuelta 1")
        
        if USAR_IA:
            # Convertir frame para MediaPipe
            img_mp = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            resultado_ia = detector.detect(img_mp)
            centro_objeto_x = None
            ancho_real = frame.shape[1]

            if resultado_ia.detections:
                for detection in resultado_ia.detections:
                    bbox = detection.bounding_box 
                    # Calculamos el centro X del objeto (0.0 a 1.0)
                    centro_objeto_x = (bbox.origin_x + (bbox.width / 2)) / ancho_real 
            
                    # Dibujar en pantalla (Debug)
                    cv2.rectangle(frame, (int(bbox.origin_x), int(bbox.origin_y)), 
                                  (int(bbox.origin_x + bbox.width), int(bbox.origin_y + bbox.height)), 
                                  (0, 255, 0), 2)
        
        # 1. LÓGICA DE VUELTAS Y META (MAGENTA) o (NARANJA o AZUL)
        # SISTEMA INTELIGENTE DE CONTEO DE VUELTAS SEGÚN EL MODO
        hay_meta, _ = detectar_color(hsv, MAGENTA)
        # MODO 2: Competencia de Obstáculos (Meta = Muros Magenta)
        if MODO_COMPETENCIA == "OBSTACULOS_ESTACIONADO":
            if hay_meta:
                if not en_meta and (time.time() - tiempo_ultima_vuelta > 5):
                    vueltas_totales += 1
                    tiempo_ultima_vuelta = time.time()
                    inicio_vuelta = time.time() # REINICIO CRUCIAL PARA LA MEMORIA
                    en_meta = True
                    print(f"Vuelta {vueltas_totales} completada (Meta Magenta)")
                if vueltas_totales >= 4:
                    if MODO_COMPETENCIA == "OBSTACULOS_ESTACIONADO":
                        comando = 'S' # Activa la sub-rutina de centrado y retroceso en el Arduino
                        potencia = 'L'
                        print("ESTACIONANDO")
                    else:
                        comando = 'S' # Frenado en seco inmediato en la línea
                        potencia = 'L'
                        print("DETENIDO")
            else:
                en_meta = False
                
        # MODO 1: Carrera Abierta (Meta = Línea del suelo según el sentido de giro)
        elif MODO_COMPETENCIA == "CARRERA_ABIERTA":
            # Si el circuito gira a la derecha, la línea Naranja es nuestra meta
            if SENTIDO_CIRCUITO == "HORARIO" and detectar_color(hsv, NARANJA):
                if not en_meta and (time.time() - tiempo_ultima_vuelta > 8):
                    vueltas_totales += 1
                    tiempo_ultima_vuelta = time.time()
                    inicio_vuelta = time.time()  # Reinicio del reloj para la memoria
                    en_meta = True
                    print(f"Vuelta {vueltas_totales} completada (Meta Naranja)")
            
            # Si el circuito gira a la izquierda, la línea Azul es nuestra meta
            elif SENTIDO_CIRCUITO == "ANTIHORARIO" and detectar_color(hsv, AZUL_SUELO):
                if not en_meta and (time.time() - tiempo_ultima_vuelta > 8):
                    vueltas_totales += 1
                    tiempo_ultima_vuelta = time.time()
                    inicio_vuelta = time.time()  # Reinicio del reloj para la memoria
                    en_meta = True
                    print(f"Vuelta {vueltas_totales} completada (Meta Azul)")
            
            # Evitamos falsos positivos mientras el auto está sobre la línea
            elif not (detectar_color(hsv, NARANJA) or detectar_color(hsv, AZUL_SUELO)):
                en_meta = False
                

        # 2. LÓGICA DE APRENDIZAJE vs CARRERA
        if vueltas_totales > 1 and comando != 'S':
            # MODO CARRERA: Usar memoria
            comando_rec, potencia_rec = memoria_pista.get(t_actual, ('F', 'H'))
            comando, potencia = comando_rec, 'H' # Boost en la mejora
            
            # ANTICIPACIÓN ULTRA-AGRESIVA:
            # Si la memoria dice que toca girar, pero el sentido dominante nos permite 
            # abrirnos en la pista para tomar la curva más rápido:
            # Caso 1: Circuito hacia la Derecha (Horario)
            if SENTIDO_CIRCUITO == "HORARIO" and comando == 'D':
                # Optimizamos el ángulo de entrada en el Arduino si es necesario
                # Reduce de 'H' a 'M' en el milisegundo exacto antes del giro para no derrapar
                potencia = 'M' # Velocidad óptima de paso por curva calculada
            # Caso 2: Circuito hacia la Izquierda (Antihorario)
            elif SENTIDO_CIRCUITO == "ANTIHORARIO" and comando == 'I':
                # Aplica la misma reducción controlada para entrar rápido pero firme a la izquierda
                potencia = 'M'
                
        elif comando != 'S':
            # MODO APRENDIZAJE: Navegación y reglas
            es_rojo, cx_r = detectar_color(hsv, ROJO)
            es_verde, cx_v = detectar_color(hsv, VERDE)
            es_naranja, _ = detectar_color(hsv, NARANJA)
            es_azul, _ = detectar_color(hsv, AZUL_SUELO)
            
            if es_naranja:
                comando = 'D' # Giro agresivo derecha en esquina
                potencia = 'M'
                if SENTIDO_CIRCUITO == "INDETERMINADO":
                    SENTIDO_CIRCUITO = "HORARIO"
                    print(">>> ¡Sentido detectado: HORARIO! Optimizando giros a la Derecha.")

            elif es_azul:
                comando = 'I' # Giro agresivo izquierda en esquina
                potencia = 'M'
                if SENTIDO_CIRCUITO == "INDETERMINADO":
                    SENTIDO_CIRCUITO = "ANTIHORARIO"
                    print(">>> ¡Sentido detectado: ANTIHORARIO! Optimizando giros a la Izquierda.")
            
            elif es_rojo:
                if centro_objeto_x is not None:
                    # Si el objeto está a la izquierda (x < 0.4), giro leve
                    if centro_objeto_x < 0.4:
                        comando = '1'
                        print("-> Giro LEVE ROJO(1)")
                    else:
                        'I'
                        print("-> Giro AGRESIVO ROJO (I)")
                else:
                    comando = 'I'# Seguridad
                    print("-> Giro AGRESIVO ROJO CV (I)")
                potencia = 'L'
                print("potencia L")
            elif es_verde:
                if centro_objeto_x is not None:
                    if dist_I > dist_D:
                        # Hay más espacio a la izquierda
                        if centro_objeto_x < 0.4:
                            comando = '1'
                            print("-> Giro LEVE VERDE (1)")
                        else:
                            'I'
                            print("-> Giro AGRESIVO VERDE IA (I)")
                    else:
                        # Hay más espacio a la derecha (o igual)
                        if centro_objeto_x > 0.6:
                            comando = '2'
                            print("-> Giro LEVE VERDE (2)")
                        else:
                            'D'
                            print("-> Giro AGRESIVO VERDE IA (D)")
                else:
                    comando = 'D'
                    print("-> Giro AGRESIVO VERDE CV (D)")
                potencia = 'L'
                print("potencia L")
            else:
                comando, potencia = 'F', 'M'
                print("potencia M")
            
            # Guardar en memoria
            if vueltas_totales == 1:
                memoria_pista[t_actual] = (comando, potencia)
                
            if vueltas_totales > 1:
                comando, potencia = memoria_pista.get(t_actual, ('F', 'H'))

        # 3. COMUNICACIÓN Y LOG
        if ser:
            ser.write(f"{comando}{potencia}".encode())
            linea = ser.readline().decode('utf-8', errors='ignore').strip()
        else:
            linea = "D:0,0,0,0" # Simulación

        # Guardar CSV
        with open(archivo_log, mode='a', newline='') as f:
            csv.writer(f).writerow([time.time(), vueltas_totales, comando, potencia, linea])

        if comando == 'S' and vueltas_totales >= 4: break
        
        #COMANDO PARA ESTACIONAMIENTO(IR AQUI)

        cv2.imshow('WRO Vision', frame) # Comentar en competencia
        if cv2.waitKey(1) & 0xFF == ord('q'): break

finally:
    if ser: ser.write(b'SS')
    cap.release()
    cv2.destroyAllWindows()