import cv2
import numpy as np
import serial
import time
import math

arduino = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(2)

ultimo_estado = 1
estado = 1

tiempo_inicio = time.time()

cadena_datos = f"<0,120>\n"
arduino.write(cadena_datos.encode('utf-8'))
cadena_datos = f"<0,60>\n"
arduino.write(cadena_datos.encode('utf-8'))
cadena_datos = f"<0,86>\n"
arduino.write(cadena_datos.encode('utf-8'))

print("Esperando señal...")

while True:
    if arduino.in_waiting > 0:
            linea = arduino.readline().decode('utf-8').rstrip()
                                    
            if linea == "BTN:1":
                estado += 1
                
    if estado != ultimo_estado:
            if estado == 2:
                cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

                cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 854)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                cv2.namedWindow("Camara prueba", cv2.WINDOW_NORMAL)

                cv2.resizeWindow("Camara prueba", 1280, 720)

                if not cap.isOpened():
                    print("Error: No se detecta la cámara web.")
                    exit()

                while True:
                    ret, frame = cap.read()
                    if not ret:
                        print("Error: cámara web rota.")
                        break

                    alto, ancho, _ = frame.shape

                    frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                    promedio_s = np.mean(frame_hsv[:, :, 1])
                    promedio_v = np.mean(frame_hsv[:, :, 2])
                    
                    min_s = int(max(40, promedio_s * 0.6))
                    min_v = int(max(30, promedio_v * 0.5))
                    naranja_mascara = cv2.inRange(frame_hsv, np.array([5, min_s, min_v]), np.array([15, 255, 255]))
                    azul_mascara = cv2.inRange(frame_hsv, np.array([90, min_s, min_v]), np.array([130, 255, 255]))
                    
                    desviacion_estandar = np.std(frame_gris)
                    sigma_color_automatico = float(desviacion_estandar * 1.2)
                    #frame_procesado = cv2.GaussianBlur(frame_gris, (5, 5), 0)
                    #frame_procesado = cv2.medianBlur(frame_gris, 5)
                    frame_procesado = cv2.bilateralFilter(frame_gris, 9, sigma_color_automatico, 75)

                    umbral, frame_binario = cv2.threshold(frame_procesado, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                    #frame_binario = cv2.adaptiveThreshold(frame_procesado, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101, 15)

                    #frame_delimitado = cv2.morphologyEx(frame_binario, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)))

                    contornos, _ = cv2.findContours(frame_binario, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    puntos_pared_izq = []
                    puntos_pared_der = []
                    if contornos:
                        c_max = max(contornos, key=cv2.contourArea)
                    for punto in c_max:
                            x, y = punto[0][0], punto[0][1]
                            if x < ancho // 2:
                                puntos_pared_izq.append((x, y))
                            else:
                                puntos_pared_der.append((x, y))
                    y_control = int(alto * 0.25)
                    x_izq = 0
                    for x in range(ancho // 2, 0, -1):
                        if frame_binario[y_control, x] == 0:
                            x_izq = x
                            break
                    x_der = ancho
                    for x in range(ancho // 2, ancho):
                        if frame_binario[y_control, x] == 0:
                            x_der = x
                            break
                    centro_pista_x = int((x_izq + x_der) / 2)
                    cv2.circle(frame, (x_izq, y_control), 8, (255, 0, 0), -1)
                    cv2.circle(frame, (x_der, y_control), 8, (0, 255, 0), -1)
                    cv2.circle(frame, (centro_pista_x, y_control), 10, (0, 0, 255), -1)
                    cv2.line(frame, (x_izq, y_control), (x_der, y_control), (255, 255, 255), 2)

                    #empezar aqui algoritmo pure pursuit
                    dx = centro_pista_x - ancho // 2
                    dy = alto - y_control

                    lookahead_dist = math.hypot(dx, dy)

                    error_lateral = dx

                    angulo_brazo_rad = math.atan2(2.0 * 100 * error_lateral, lookahead_dist**2)

                    cambio_servo = angulo_brazo_rad * 40 #sensibilidad

                    angulo = int(86 + cambio_servo)
                    angulo = max(60, min(120, angulo))

                    velocidad = 0 
                    
                    pre_resultado = cv2.bitwise_or(frame_binario, naranja_mascara )
                    resultado_final = cv2.bitwise_or(pre_resultado, azul_mascara)
                    
                    #print(f"Umbral Otsu actual: {umbral}")

                    cv2.imshow("Camara Real - Centro de Pista", frame)
                    cv2.imshow("Camara prueba", resultado_final)
                    cv2.imshow("Mascara naranja (Blanco y Negro)", naranja_mascara)
                    cv2.imshow("Mascara azul (Blanco y Negro)", azul_mascara)

                    # Detener el programa si presionas la letra 'q'
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                    cadena_datos = f"<{velocidad},{angulo}>\n"
                    arduino.write(cadena_datos.encode('utf-8'))
                    #print(f"Dato <{velocidad},{angulo}> enviado.")

                    if (time.time() - tiempo_inicio) < 30:
                        angulo = 86
                        velocidad = 0
                            
                        cadena_datos = f"<{velocidad},{angulo}>\n"
                        arduino.write(cadena_datos.encode('utf-8'))
                        print(f"Dato <{velocidad},{angulo}> enviado.")
                            
                        estado = 1
                         
    
            elif estado == 3:
                angulo = 86
                velocidad = 0
    
                cadena_datos = f"<{velocidad},{angulo}>\n"
                arduino.write(cadena_datos.encode('utf-8'))
                print(f"Dato <{velocidad},{angulo}> enviado.")
    
                estado = 1

cap.release()
cv2.destroyAllWindows()
arduino.close()