import os
os.environ["QT_QPA_PLATFORM"] = "xcb"
import cv2
import serial
import time
import csv
import numpy as np
import threading

# --- 1. VARIABLES GLOBALES ---
centro_objeto_x = None
USAR_IA = True
ser = None
ultimo_angulo_enviado = -1
ultima_potencia_enviada = ""
ultimo_tiempo_envio_comando = 0
INTERVALO_MINIMO_COMANDO = 0.04
centro_ia_x = None
lock = threading.Lock()
escenario_ia = "RECTA"
certeza_ia = 1.0

# --- 2. CALLBACK ASÍNCRONO PARA MEDIAPIPE ---
def callback_clasificacion_ia(resultado, imagen_salida, timestamp_ms):
    global centro_objeto_x, certeza_ia
    if resultado and resultado.classifications:
        # Accedemos a la primera clasificación y a su lista de categorías
        categorias = resultado.classifications[0].categories
        if categorias:
            # Tomamos la categoría con mayor puntaje (la primera de la lista)
            mejor_categoria = categorias[0]
            with lock:
                escenario_ia = mejor_categoria.category_name  # Ej: "RECTA", "OBSTACULO_DER"
                certeza_ia = mejor_categoria.score           # Porcentaje de confianza
            return
    with lock: # Evita que la Pi se congele al compartir datos
        escenario_ia = "RECTA"
        certeza_ia = 0.0

# --- 3. INICIALIZACIÓN DE MEDIAPIPE ---
try:
    import mediapipe as mp
    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision

    base_options = python.BaseOptions(
        model_asset_path='clasificador_pista.tflite',
        delegate=python.BaseOptions.Delegate.CPU
    )
    options = vision.ImageClassifierOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.LIVE_STREAM,
        max_results=1,               # Solo nos interesa el escenario más probable
        score_threshold=0.45,        # Descarta clasificaciones débiles o dudosas
        result_callback=callback_clasificacion_ia
    )
     # Cambiamos ObjectDetector por ImageClassifier
    detector = vision.ImageClassifier.create_from_options(options)
    print(">>> IA de Clasificación Corriendo en MediaPipe asíncrono.")
    USAR_IA = True
except Exception as e:
    print(f"Error crítico al cargar Clasificador IA: {e}. Modo solo OpenCV activo.")
    USAR_IA = False

# --- 4. CONFIGURACIÓN DE PISTA Y CONSTANTES ---
archivo_log = "log_robot_wro.csv"
vueltas_totales = 0
en_meta = False
tiempo_ultima_vuelta = 0
memoria_pista = {}
inicio_vuelta = time.time()

ANGULO_CENTRO = 90
MAX_GIRO = 30

# Espacio de Color LAB
ROJO = [np.array([50, 160, 140]), np.array([180, 200, 180])]
VERDE = [np.array([15, 40, 135]), np.array([225, 110, 200])]
MAGENTA = [np.array([40, 165, 50]), np.array([160, 255, 110])]
NARANJA = [np.array([140, 140, 195]), np.array([225, 220, 255])]
AZUL_SUELO = [np.array([30, 100, 30]), np.array([170, 140, 110])]

KERNEL_OPEN = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
KERNEL_CLOSE = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

# --- 5. CONEXIÓN SERIAL ---
for puerto in ['/dev/ttyACM0', 'COM3']:
    try:
        ser = serial.Serial(puerto, 115200, timeout=0.02)
        print(f"Conectado a Arduino en {puerto}")
        break
    except:
        continue
if not ser:
    print("AVISO: Arduino no detectado. Modo simulación.")

# --- 6. FUNCIONES DE FILTRADO GEOMÉTRICO ---
def _clean_mask(mask: np.ndarray) -> np.ndarray:
    kernel_chico = np.ones((3, 3), np.uint8)
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL_OPEN)
    return cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL_CLOSE)

def _is_valid_obstacle(area: float, w: int, h: int, img_w: int, es_pilar: bool) -> bool:
    if area < 300: return False
    if not es_pilar: return True
    
    ratio = h / max(w, 1)
    fill = area / max(w * h, 1)
    return ratio >= 1.0 and fill >= 0.40 and w <= img_w * 0.50

def detectar_color(lab_pequeno, rango, frame_dibujo, nombre_color ,escala_factor=2, es_pilar=False):
    img_h, img_w = lab_pequeno.shape[:2]
    mask = cv2.inRange(lab_pequeno, rango[0], rango[1])
    mask = _clean_mask(mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    best_cx = 160
    valid_detection = False
    max_score = -1
    
    for contour in contours:
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        
        if area > 150 and _is_valid_obstacle(area, w, h, img_w, es_pilar):
            fill_ratio = area / max(w * h, 1)
            vertical_ratio = h / max(w, 1)
            score = area * fill_ratio * vertical_ratio
            
            if score > max_score:
                max_score = score
                best_cx = int((x + w / 2)* escala_factor)
                valid_detection = True
                # Dibujar rectángulo del objeto detectado
                rx, ry, rw, rh = x * escala_factor, y * escala_factor, w * escala_factor, h * escala_factor
                cv2.rectangle(frame_dibujo, (rx, ry), (rx + rw, ry + rh), (0, 255, 255), 2)
                cv2.putText(frame_dibujo, f"{nombre_color} ({int(area * 4)}px)", (rx, max(ry - 10, 15)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
                
    return valid_detection, best_cx

def actualizar_sensores():
    global dist_F, dist_A, dist_I, dist_D
    if ser and ser.in_waiting > 0:
        try:
            linea = ser.readline().decode('utf-8', errors='ignore').strip()
            if linea.startswith("D:"):
                datos = linea.replace("D:", "").split(",")
                if len(datos) == 4:
                    dist_F, dist_A, dist_I, dist_D = map(float, datos)
        except Exception as e:       
            pass

# --- 7. CONFIGURACIÓN INICIAL DE CÁMARA Y CALIBRACIÓN ---
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
contador_esquinas = 0
en_esquina_actual = False

print(">>> SISTEMA INTEGRADO INICIADO\nCalibrando entorno...")
try:
    actualizar_sensores()
    print(f"Sensores OK")
except:
    print("Error de lectura de sensores.")
    
try:
    if dist_F < 40 and dist_A < 40:
        MODO_COMPETENCIA = "OBSTACULOS_ESTACIONADO"
        SENTIDO_CIRCUITO = "INDETERMINADO"
        VELOCIDAD_CRUCERO = "M"
        vueltas_totales = 0
        print(">>> MODO DETECTADO: 2 - Obstáculos")
    else:
        MODO_COMPETENCIA = "CARRERA_ABIERTA"
        SENTIDO_CIRCUITO = "INDETERMINADO"
        VELOCIDAD_CRUCERO = "H"
        vueltas_totales = 1
        print(">>> MODO DETECTADO: 1 - Carrera Abierta")
except:
    print(">>> MODO DETECTADO: 0 - SIMULACION")
    #Cambie E para elegir el escenario a simular
    E = 1
    if E == 1:
        MODO_COMPETENCIA = "OBSTACULOS_ESTACIONADO"
        SENTIDO_CIRCUITO = "INDETERMINADO"
        VELOCIDAD_CRUCERO = "M"
        vueltas_totales = 0
        print(">>> MODO SIMULACION: 2 - Obstáculos")
    else:
        MODO_COMPETENCIA = "CARRERA_ABIERTA"
        SENTIDO_CIRCUITO = "INDETERMINADO"
        VELOCIDAD_CRUCERO = "H"
        vueltas_totales = 1
        print(">>> MODO SIMULACION: 1 - Carrera Abierta")

# --- 8. BUCLE PRINCIPAL ---
archivo_csv = open(archivo_log, mode='a', newline='')
log_writer = csv.writer(archivo_csv)
ultimo_tiempo_ia = 0
INTERVALO_IA = 0.10

try:
    while cap.isOpened():
        
        ret, frame = cap.read()
        if not ret: break
        
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2Lab)
        t_actual = round(time.time() - inicio_vuelta, 1)
        actualizar_sensores()
        
        t_actual_ms = time.time()
        
        angulo_servo = ANGULO_CENTRO
        potencia_motor = VELOCIDAD_CRUCERO

        # Rutina de salida (Vuelta 0)
        if MODO_COMPETENCIA == "OBSTACULOS_ESTACIONADO" and vueltas_totales == 0:
            potencia_motor = 'L'
            try:
                if dist_A > 30:
                    vueltas_totales = 1
                    inicio_vuelta = time.time()
                    print("¡Fuera del cajón! Iniciando Vuelta 1")
            except:
                vueltas_totales = 1
                inicio_vuelta = time.time()
                print("¡Fuera del cajón! Iniciando Vuelta 1")
                
        
        # DOWN-SAMPLING (Optimización OpenCV): Reducimos la carga matemática a la cuarta parte
        frame_pequeno = cv2.resize(frame, (160, 120), interpolation=cv2.INTER_NEAREST)
        lab_pequeno = cv2.cvtColor(frame_pequeno, cv2.COLOR_BGR2Lab)

        # PROCESAMIENTO ULTRA RÁPIDO DE COLOR
        hay_meta, _ = detectar_color(lab_pequeno, MAGENTA, frame, "MAGENTA", 2)
        es_naranja, _ = detectar_color(lab_pequeno, NARANJA, frame, "NARANJA", 2, False)
        es_azul, _ = detectar_color(lab_pequeno, AZUL_SUELO, frame, "AZUL", 2, False)
        es_rojo, cx_r = detectar_color(lab_pequeno, ROJO, frame, "ROJO", 2, True)
        es_verde, cx_v = detectar_color(lab_pequeno, VERDE, frame, "VERDE", 2, True)
        
        if USAR_IA and (es_rojo or es_verde):
            if (t_actual_sistema - ultimo_tiempo_ia) > 0.05: # ~20 FPS para la IA
                # Pasamos la imagen de 160x120 para liberar mas del 60% de CPU
                img_mp = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_pequeno)
                timestamp_unico = int(time.time_ns() / 1000)
                detector.classify_async(img_mp, timestamp_unico) # .classify_async reemplaza a .detect_async
                ultimo_tiempo_ia = t_actual_sistema
            # Extracción segura de datos calculados por la IA en segundo plano
        with lock:
            local_escenario = escenario_ia
            local_certeza = certeza_ia
        
        # Dibujamos el estado de la IA en la pantalla del robot para los jueces
        cv2.putText(frame, f"IA MODO: {local_escenario} ({int(local_certeza*100)}%)", (10, 25), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
        
        #FUSIÓN DE DATOS: IA + OPENCV 
        # Inyección de visión tradicional a la IA
        if local_escenario == "OBSTACULO_DER" and es_rojo:
            # IA confirma obstáculo a la derecha y OpenCV ve el pilar rojo -> Forzamos esquivar a la izquierda
            centro_objeto_x = 0.1 
            potencia_motor = 'L'
        elif local_escenario == "OBSTACULO_IZQ" and es_verde:
            # IA confirma obstáculo a la izquierda y OpenCV ve el pilar verde -> Forzamos esquivar a la derecha
            centro_objeto_x = 0.9
            potencia_motor = 'L'
        elif local_escenario == "CURVA_PROXIMA":
            # La IA detecta la geometría de la esquina antes de llegar a la línea -> Prepara el coche bajando velocidad
            potencia_motor = 'M'
            centro_objeto_x = cx_r / 320.0 if es_rojo else (cx_v / 320.0 if es_verde else None)
        else:
            # Modo Estándar / "RECTA": Conducción directa por OpenCV tradicional
            if es_rojo:
                centro_objeto_x = cx_r / 320.0
            elif es_verde:
                centro_objeto_x = cx_v / 320.0
            else:
                centro_objeto_x = None
                
                
        # --- LÓGICA DE CONTROL Y NAVEGACIÓN ---
        if vueltas_totales == 1:
            if es_naranja or es_azul:
                if SENTIDO_CIRCUITO == "INDETERMINADO":
                    SENTIDO_CIRCUITO = "HORARIO" if es_naranja else "ANTIHORARIO"
                    inicio_vuelta = time.time()
                    t_actual = 0.0
                    contador_esquinas = 0
                    memoria_pista.clear()
                    print(f">>> Sentido {SENTIDO_CIRCUITO} Detectado.")
                
                angulo_servo = ANGULO_CENTRO + (MAX_GIRO if SENTIDO_CIRCUITO == "HORARIO" else -MAX_GIRO)
                en_esquina_actual = True
                
                
            elif es_rojo and centro_objeto_x is not None:
                if centro_objeto_x <= 0.5:
                    factor_giro = 1.0
                else:
                    factor_giro = 1.5 - centro_objeto_x
                    
                angulo_servo = ANGULO_CENTRO + int(MAX_GIRO * factor_giro)
                potencia_motor = 'L'
                print(f">>> {angulo_servo}")
                
            elif es_verde and centro_objeto_x is not None:
                if centro_objeto_x >= 0.5:
                    factor_giro = 1.0
                else:
                    factor_giro = centro_objeto_x
                    
                angulo_servo = ANGULO_CENTRO + int(MAX_GIRO * factor_giro)
                potencia_motor = 'L'
                print(f">>> {angulo_servo}")#Sacar mejor el calculo de los giros
                
            else:  # Tramo Recto / Salida de curva
                if en_esquina_actual:
                    contador_esquinas += 1
                    en_esquina_actual = False
                    print(f"-> Esquina {contador_esquinas} superada.")
                    
                    if contador_esquinas >= 4:
                        tiempo_ultima_vuelta = time.time()
                        inicio_vuelta = time.time()
                        t_actual = 0.0
                        contador_esquinas = 0
                
                angulo_servo = ANGULO_CENTRO
                potencia_motor = VELOCIDAD_CRUCERO

            if SENTIDO_CIRCUITO != "INDETERMINADO":
                memoria_pista[t_actual] = (angulo_servo, potencia_motor)

        elif vueltas_totales > 1:
            # Conteo de vueltas avanzado por Meta Magenta en Obstáculos
            if MODO_COMPETENCIA == "OBSTACULOS_ESTACIONADO":
                if hay_meta and not en_meta and (time.time() - tiempo_ultima_vuelta > 6):
                    vueltas_totales += 1
                    tiempo_ultima_vuelta = time.time()
                    inicio_vuelta = time.time()
                    en_meta = True
                    print(f"Vuelta {vueltas_totales} completada (Meta Magenta)")
                elif not hay_meta:
                    en_meta = False
            else:
                # Conteo en modo Carrera Abierta
                if (es_naranja and SENTIDO_CIRCUITO == "HORARIO") or (es_azul and SENTIDO_CIRCUITO == "ANTIHORARIO"):
                    en_esquina_actual = True
                else:
                    if en_esquina_actual:
                        contador_esquinas += 1
                        en_esquina_actual = False
                        if contador_esquinas >= 4:
                            vueltas_totales += 1
                            tiempo_ultima_vuelta = time.time()
                            inicio_vuelta = time.time()
                            t_actual = 0.0
                            contador_esquinas = 0
                            print(f"Vuelta {vueltas_totales} completada")
                            
 # --- SISTEMA DE FRENADO / ESTACIONAMIENTO ---
        if vueltas_totales >= 4:
            if MODO_COMPETENCIA == "OBSTACULOS_ESTACIONADO":
                angulo_servo, potencia_motor = ANGULO_CENTRO, 'P'
                print("ESTACIONANDO >>> Iniciando Estacionamiento Asistido")
            else:
                angulo_servo, potencia_motor = ANGULO_CENTRO, 'S'
                print("DETENIDO >>> FIN DE CARRERA ABIERTA")

        # --- COMUNICACIÓN Y LOG ---
        linea_arduino = "D:0,0,0,0"
        if ser:
            tiempo_actual_serial = time.time()
            ang_int = int(angulo_servo)
            
            # Condición: Solo envía si cambió el comando O si ya pasó el tiempo límite de seguridad
            if (ang_int != ultimo_angulo_enviado or 
                potencia_motor != ultima_potencia_enviada or 
                (tiempo_actual_serial - ultimo_tiempo_envio_comando) > INTERVALO_MINIMO_COMANDO):
            
                ser.write(f"A{int(angulo_servo):03d}P{potencia_motor}\n".encode())
                
                ultimo_angulo_enviado = ang_int
                ultima_potencia_enviada = potencia_motor
                ultimo_tiempo_envio_comando = tiempo_actual_serial
                
            if ser.in_waiting > 0:
                linea_arduino = ser.readline().decode('utf-8', errors='ignore').strip()
            
        log_writer.writerow([time.time(), vueltas_totales, angulo_servo, potencia_motor, linea_arduino])
        archivo_csv.flush() 
            
        # Condición de salida corregida para que rompa el bucle en ambos modos de competencia
        if vueltas_totales >= 4:
            if potencia_motor == 'S' or potencia_motor == 'P':
                break
                
        cv2.imshow('WRO Vision', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
            
finally:
    archivo_csv.close()
    if ser: 
        ser.write(b'A090PS\n')
        ser.close()
    cap.release()
    cv2.destroyAllWindows()
