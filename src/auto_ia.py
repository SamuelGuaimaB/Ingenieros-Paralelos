import cv2
import serial
import time
import csv
import numpy as np

centro_objeto_x = None  # Almacena la posición calculada por la IA asíncrona

# --- 2. CALLBACK ASÍNCRONO PARA MEDIAPIPE ---
def callback_resultado_ia(resultado, imagen_salida, timestamp_ms):
    global centro_objeto_x
    if resultado.detections:
        # Tomamos la detección con mayor índice de confianza
        deteccion = resultado.detections[0]
        bbox = deteccion.bounding_box
        ancho_real = imagen_salida.width
        # Calculamos el centro horizontal normalizado (0.0 a 1.0)
        centro_objeto_x = (bbox.origin_x + (bbox.width / 2)) / ancho_real
        try:
            cv2.rectangle(frame, (int(bbox.origin_x), int(bbox.origin_y)), 
                          (int(bbox.origin_x + bbox.width), int(bbox.origin_y + bbox.height)), 
                          (0, 255, 0), 2)
        except:
            pass
    else:
        centro_objeto_x = None

# --- INICIALIZACIÓN DE MEDIAPIPE ---
try:
    import mediapipe as mp
    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision
    
    base_options = python.BaseOptions(model_asset_path='efficientdet_lite0.tflite')
    options = vision.ObjectDetectorOptions(
        base_options=base_options,
        score_threshold=0.35,
        running_mode=vision.RunningMode.LIVE_STREAM, # NO congela el código principal
        result_callback=callback_resultado_ia
    )
    detector = vision.ObjectDetector.create_from_options(options)
    USAR_IA = True
    print(">>> IA Activada en Modo Cooperativo Asíncrono")
except Exception as e:
    print(f"Error crítico al cargar IA: {e}. Entrando en modo solo OpenCV.")
    USAR_IA = False

# --- CONFIGURACIÓN DE PISTA ---
archivo_log = "log_robot_wro.csv"
vueltas_totales = 0
en_meta = False
tiempo_ultima_vuelta = 0
memoria_pista = {}  # Formato: {tiempo: (comando, potencia)}
inicio_vuelta = time.time()

# --- CONSTANTES DE DIRECCIÓN GRADUAL ---
ANGULO_CENTRO = 90  # Servo apuntando al frente en grados
MAX_GIRO = 30        # Máximo desvío del servo (60° a 120°)

# --- CONEXIÓN SERIAL (Protegida) ---
try:
    # Intenta Raspberry (Linux) o Windows
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.02)
except:
    try:
        ser = serial.Serial('COM4', 115200, timeout=0.02)
    except:
        print("AVISO: Arduino no detectado. Modo simulación.")
        ser = None

# --- CONFIGURACIÓN EN ESPACIO LAB ---
# Formato: [L_min, A_min, B_min], [L_max, A_max, B_max]
# Nota: Dejamos el canal L amplio (40-255) para que no le afecte la luz
ROJO = [(40, 145, 130), (255, 255, 255)]     # 'A' alta = Rojo
VERDE = [(40, 0, 135), (255, 110, 255)]      # 'A' baja = Verde, 'B' alta = Amarillo/Verde
MAGENTA = [(40, 150, 40), (255, 255, 120)]   # 'A' alta = Magenta, 'B' baja = Azulado/Meta
NARANJA = [(40, 135, 145), (255, 180, 255)]  # 'A' moderada, 'B' alta = Naranja
AZUL_SUELO = [(40, 110, 0), (255, 140, 115)] # 'B' baja = Azul suelo

# --- FUNCIONES DE FILTRADO GEOMÉTRICO INYECTADAS ---
def _clean_mask(mask: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    mask = cv2.GaussianBlur(mask, (kernel_size, kernel_size), 0)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return mask

def _is_valid_obstacle(area: float, w: int, h: int, img_w: int, es_pilar: bool) -> bool:
    if not es_pilar:
        return area > 1200  
        
    min_area = 1200
    min_ratio = 1.0          
    min_fill = 0.40          
    max_width_ratio = 0.50   
    
    ratio = h / max(w, 1)
    fill = area / max(w * h, 1)
    
    if area < min_area: return False
    if ratio < min_ratio: return False
    if fill < min_fill: return False
    if w > img_w * max_width_ratio: return False
    return True

def detectar_color(lab_frame, rango, es_pilar=False):
    # Genera la máscara usando el espacio LAB
    img_h, img_w = lab_frame.shape[:2]
    mask = cv2.inRange(lab_frame, np.array(rango[0]), np.array(rango[1]))
    mask = _clean_mask(mask, kernel_size=5)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    best_cx = 160
    valid_detection = False
    max_score = -1
    
    for contour in contours:
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        
        # Validar si el candidato cumple las reglas geométricas del pilar
        if _is_valid_obstacle(area, w, h, img_w, es_pilar):
            # Calculamos score (Prioriza áreas grandes y verticales)
            fill_ratio = area / max(w * h, 1)
            vertical_ratio = h / max(w, 1)
            score = area * fill_ratio * vertical_ratio
            
            # Conservamos el pilar más confiable
            if score > max_score:
                max_score = score
                best_cx = int(x + w / 2)
                valid_detection = True
                
                # Dibujar caja de depuración (Opcional)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
                
    return valid_detection, best_cx

def actualizar_sensores():
    global dist_F, dist_A, dist_I, dist_D
    if ser:
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
                    # Para confirmar que ya se actualizan
                    print(f"Sensores OK -> F:{dist_F} | A:{dist_A} | I:{dist_I} | D:{dist_D}")
        except Exception as e:
            print(f"no se leyeron los sensores")
            pass # Si hay un error de lectura, mantiene el último valor seguro
    else:
        print(f"No se detectaron sensores, activando simulacion de sensores")

# --- BUCLE PRINCIPAL ---
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320); cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

contador_esquinas = 0
en_esquina_actual = False

print(">>> SISTEMA INTEGRADO INICIADO")

try:
    print("Calibrando entorno... No mueva el robot.")
    
    actualizar_sensores()

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
        SENTIDO_CIRCUITO = "INDETERMINADO"
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
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2Lab)
        t_actual = round(time.time() - inicio_vuelta, 1)
        
        if ser:
            actualizar_sensores() # Tu función que imprime "Sensores OK" 
        
        angulo_servo = ANGULO_CENTRO
        potencia_motor = "M"
        
        # Si estamos en el Modo Obstáculos, aplicamos la rutina de salida estacionada en la Vuelta 0
        if MODO_COMPETENCIA == "OBSTACULOS_ESTACIONADO" and vueltas_totales == 0:
            # El robot arranca suave para salir del cajón de paredes
            angulo_servo = ANGULO_CENTRO
            potencia_motor = 'L'
            # Una vez que el sensor trasero detecte que salimos del cajón (ej. > 30cm) 
            # pasamos a la carrera real
            if float(dist_A) > 30: 
                vueltas_totales = 1
                inicio_vuelta = time.time() # Sincronizamos cronómetro de memoria aquí
                print("¡Fuera del cajón! Iniciando Vuelta 1")
        
        if USAR_IA:
            # Convertir frame para MediaPipe
            timestamp_ia_ms = int(time.time_ns() / 1000000)
            img_mp = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            resultado_ia = detector.detect_async(img_mp, timestamp_ia_ms)
        
        # 1. LÓGICA DE VUELTAS Y META (MAGENTA) o (NARANJA o AZUL)
        # SISTEMA INTELIGENTE DE CONTEO DE VUELTAS SEGÚN EL MODO
        hay_meta, _ = detectar_color(lab, MAGENTA)
        # MODO 2: Competencia de Obstáculos (Meta = Muros Magenta)
        if MODO_COMPETENCIA == "OBSTACULOS_ESTACIONADO":
            if hay_meta:
                if not en_meta and (time.time() - tiempo_ultima_vuelta > 6):
                    vueltas_totales += 1
                    tiempo_ultima_vuelta = time.time()
                    inicio_vuelta = time.time() # REINICIO CRUCIAL PARA LA MEMORIA
                    en_meta = True
                    print(f"Vuelta {vueltas_totales} completada (Meta Magenta)")
            else:
                en_meta = False
                
            if vueltas_totales == 1:    
                # MODO APRENDIZAJE: Navegación y reglas
                es_naranja, _ = detectar_color(lab, NARANJA, es_pilar=False)
                es_azul, _ = detectar_color(lab, AZUL_SUELO, es_pilar=False)
                es_rojo, cx_r = detectar_color(lab, ROJO, es_pilar=True)
                es_verde, cx_v = detectar_color(lab, VERDE, es_pilar=True)
                               
                if USAR_IA and centro_objeto_x is None:
                    if es_rojo: centro_objeto_x = cx_r / frame.shape[1]
                    elif es_verde: centro_objeto_x = cx_v / frame.shape[1]
                
                angulo_servo = ANGULO_CENTRO
                potencia_motor = VELOCIDAD_CRUCERO
                
                if es_naranja:
                    if SENTIDO_CIRCUITO == "INDETERMINADO":
                        angulo_servo = ANGULO_CENTRO + MAX_GIRO # Giro procedural derecho completo
                        SENTIDO_CIRCUITO = "HORARIO"
                        inicio_vuelta = time.time() # Sincroniza el tiempo 0.0 en la primera esquina
                        t_actual = 0.0
                        contador_esquinas = 0
                        memoria_pista.clear()
                        print(">>> Sentido HORARIO, Iniciando grabación procedural desde la Curva 1")
                    elif SENTIDO_CIRCUITO == "HORARIO":
                        print("-> Giro HORARIO NARANJA")
                        angulo_servo = ANGULO_CENTRO + MAX_GIRO         
                    if not en_esquina_actual:
                        en_esquina_actual = True    
                    
                        # 2. Detectar Esquina Azul (Giro Izquierda)
                elif es_azul:
                    if SENTIDO_CIRCUITO == "INDETERMINADO":
                        angulo_servo = ANGULO_CENTRO - MAX_GIRO # Giro procedural izquierdo completo
                        SENTIDO_CIRCUITO = "ANTIHORARIO"
                        inicio_vuelta = time.time() # Sincroniza el tiempo 0.0 en la primera esquina
                        t_actual = 0.0
                        contador_esquinas = 0
                        memoria_pista.clear()
                        print(">>> Sentido ANTIHORARIO")
                    elif SENTIDO_CIRCUITO == "ANTIHORARIO":
                        print("-> Giro ANTIHORARIO AZUL")
                        angulo_servo = ANGULO_CENTRO - MAX_GIRO
                            
                    if not en_esquina_actual:
                        en_esquina_actual = True
                    
                elif es_rojo:
                    if centro_objeto_x is not None:
                        # Calculamos la desviación del pilar rojo (0.0 Izquierda, 1.0 Derecha)
                        # Buscamos proyectar una trayectoria de escape proporcional hacia la derecha
                        error_gradual = 0.5 - centro_objeto_x
                        ajuste = int(error_gradual * MAX_GIRO)
                        # Obligamos a corregir hacia la izquierda para evadir el pilar derecho o viceversa
                        angulo_servo = ANGULO_CENTRO - ajuste 
                        print(f"-> Procedural Rojo. Ajustando ángulo servo a: {angulo_servo}°")
                    else:
                        angulo_servo = ANGULO_CENTRO - MAX_GIRO
                    potencia_motor = 'L'
                        
                elif es_verde:
                    if centro_objeto_x is not None:
                        # Mapeamos la distancia del pilar verde al centro de la pantalla
                        # Si el pilar está muy a la derecha (ej. centro_objeto_x = 0.7), el error es bajo (0.2)
                        # Si el pilar está en el centro (centro_objeto_x = 0.5), el error es alto (0.4) lo que obliga a girar más
                        distancia_al_borde_izq = centro_objeto_x - 0.1
                        ajuste_gradual = int(distancia_al_borde_izq * MAX_GIRO)
                        
                        # Restamos para obligar a que el servo apunte SIEMPRE a la izquierda (menor a 90 grados)
                        angulo_servo = ANGULO_CENTRO - abs(ajuste_gradual)
                        print(f"-> Procedural Verde (Fijo Izquierda). Ángulo servo: {angulo_servo}°")
                    else:
                        # Fallback seguro: Giro máximo a la izquierda si se pierde el centro matemático
                        angulo_servo = ANGULO_CENTRO - MAX_GIRO
                    potencia_motor = 'L'
                else:
                    angulo_servo, potencia_motor = ANGULO_CENTRO, 'M'
                
                # Guardar en memoria
                memoria_pista[t_actual] = (angulo_servo, potencia_motor)
                    
            if vueltas_totales > 1:
                comando, potencia = memoria_pista.get(t_actual, (ANGULO_CENTRO, 'H'))
                
        # MODO 1: Carrera Abierta (Meta = Línea del suelo según el sentido de giro)
        # MODO APRENDIZAJE
        elif MODO_COMPETENCIA == "CARRERA_ABIERTA":
            es_naranja, _ = detectar_color(lab, NARANJA, es_pilar=False)
            es_azul, _ = detectar_color(lab, AZUL_SUELO, es_pilar=False)
            
            angulo_servo = ANGULO_CENTRO
            potencia_motor = VELOCIDAD_CRUCERO # Se adapta automáticamente según la calibración inicial
            
            if vueltas_totales == 1:
                # 1. Detectar Esquina Naranja (Giro Derecha)
                if es_naranja:
                    if SENTIDO_CIRCUITO == "INDETERMINADO":
                        angulo_servo = ANGULO_CENTRO + MAX_GIRO
                        SENTIDO_CIRCUITO = "HORARIO"
                        inicio_vuelta = time.time() # Sincroniza el tiempo 0.0 en la primera esquina
                        t_actual = 0.0
                        contador_esquinas = 0
                        print(">>> Sentido HORARIO. Iniciando cronómetro de aprendizaje.")
                    elif SENTIDO_CIRCUITO == "HORARIO":
                        print("-> Giro HORARIO NARANJA")
                        angulo_servo = ANGULO_CENTRO + MAX_GIRO
                        
                    if not en_esquina_actual:
                        en_esquina_actual = True    
            
                 # 2. Detectar Esquina Azul (Giro Izquierda)
                elif es_azul:
                    if SENTIDO_CIRCUITO == "INDETERMINADO":
                        angulo_servo = ANGULO_CENTRO - MAX_GIRO
                        SENTIDO_CIRCUITO = "ANTIHORARIO"
                        inicio_vuelta = time.time() # Sincroniza el tiempo 0.0 en la primera esquina
                        t_actual = 0.0
                        contador_esquinas = 0
                        print(">>> Sentido ANTIHORARIO. Iniciando cronómetro de aprendizaje.")
                    elif SENTIDO_CIRCUITO == "ANTIHORARIO":
                        print("-> Giro ANTIHORARIO AZUL")
                        angulo_servo = ANGULO_CENTRO - MAX_GIRO
                    
                    if not en_esquina_actual:
                        en_esquina_actual = True
                        
                # 3. Tramo Recto (Liberar el estado al salir de la línea de color)
                else:
                    if en_esquina_actual:
                        contador_esquinas += 1
                        en_esquina_actual = False
                        print(f"-> Esquina {contador_esquinas} superada.")
                        
                        # Cierre de Aprendizaje: Al superar la 4ta esquina, la Vuelta 1 ha terminado
                        if contador_esquinas >= 4:
                            vueltas_totales += 1 # Cambia automáticamente al Modo Carrera (Vuelta 2)
                            tiempo_ultima_vuelta = time.time()
                            inicio_vuelta = time.time() # REINICIO DEL RELOJ PARA LA MEJORA PERFECTA
                            t_actual = 0.0
                            contador_esquinas = 0
                            print(">>> ¡4 Esquinas completadas! Vuelta 1 cerrada. Iniciando Modo Carrera.")
                            print(f"Vuelta {vueltas_totales} completada")
                            
                    # Si no hay líneas, mantenemos el avance recto firme
                    angulo_servo = ANGULO_CENTRO
                    potencia_motor = VELOCIDAD_CRUCERO # Fuerza 'H' continua en recta limpia
            
                # GUARDAR EN MEMORIA (Solo graba si ya se definió el sentido del circuito)
                if SENTIDO_CIRCUITO != "INDETERMINADO":
                    memoria_pista[t_actual] = (angulo_servo, potencia_motor)
            
            # Evitamos falsos positivos mientras el auto está sobre la línea
            elif not es_azul or es_naranja:
                en_meta = False
            
            #MODO CARRERA
            if es_naranja and SENTIDO_CIRCUITO == "HORARIO":
                if not en_esquina_actual:
                    en_esquina_actual = True    
            
            elif es_azul and SENTIDO_CIRCUITO == "ANTIHORARIO":
                if not en_esquina_actual:
                    en_esquina_actual = True
            else:
                if en_esquina_actual:
                    contador_esquinas += 1
                    en_esquina_actual = False
                    print(f"-> Esquina {contador_esquinas} superada.")
                        
                    if contador_esquinas >= 4:
                        vueltas_totales += 1
                        tiempo_ultima_vuelta = time.time()
                        inicio_vuelta = time.time()
                        t_actual = 0.0
                        contador_esquinas = 0
                        print(">>> ¡4 Esquinas completadas!")
                        print(f"Vuelta {vueltas_totales} completada")
            
            if vueltas_totales > 1:
                comando, potencia = memoria_pista.get(t_actual, (ANGULO_CENTRO, 'H'))

        # 2. LÓGICA DE APRENDIZAJE vs CARRERA
        if vueltas_totales > 1 and comando != 'S':
            # MODO CARRERA: Usar memoria
            angulo_servo_rec, potencia_rec = memoria_pista.get(t_actual, (ANGULO_CENTRO, 'H'))
            angulo_servo, potencia_motor = angulo_servo_rec, 'H' # Boost en la mejora
                
        if vueltas_totales >= 4:
            if MODO_COMPETENCIA == "OBSTACULOS_ESTACIONADO":
                angulo_servo = ANGULO_CENTRO # Activa la sub-rutina de centrado y retroceso en el Arduino
                potencia_motor = 'P'
                print("ESTACIONANDO >>> MODO 2: Iniciando Estacionamiento en Paralelo Asistido")
            else:
                angulo_servo = ANGULO_CENTRO
                potencia_motor = 'S' # Frenado en seco inmediato en la línea
                print("DETENIDO >>> MODO 1: DETENIDO TOTAL DE CARRERA")

        # 3. COMUNICACIÓN Y LOG
        if ser:
            # Transmite de forma limpia una cadena con el ángulo entero exacto y el caracter de potencia original
            # Formato: "A090PL\n", "A125PH\n", "A055PS\n"
            ser.write(f"A{int(angulo_servo):03d}P{potencia_motor}\n".encode())
            linea = ser.readline().decode('utf-8', errors='ignore').strip()
        else:
            linea = "D:0,0,0,0"

        # Guardar CSV
        with open(archivo_log, mode='a', newline='') as f:
            csv.writer(f).writerow([time.time(), vueltas_totales, angulo_servo, potencia_motor, linea])
        
        if potencia_motor == 'S' and vueltas_totales >= 4: break
        
        #COMANDO PARA ESTACIONAMIENTO(IR AQUI)

        cv2.imshow('WRO Vision', frame) # Comentar en competencia
        if cv2.waitKey(1) & 0xFF == ord('q'): break

finally:
    if ser: ser.write(b'A090PS\n')
    cap.release()
    cv2.destroyAllWindows()