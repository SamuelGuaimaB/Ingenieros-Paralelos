import cv2
import numpy as np

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
        if frame_binario[y_control, x] == 0:  # Detecta el negro de la pared
            x_der = x
            break
    centro_pista_x = int((x_izq + x_der) / 2)
    cv2.circle(frame, (x_izq, y_control), 8, (255, 0, 0), -1)
    cv2.circle(frame, (x_der, y_control), 8, (0, 255, 0), -1)
    cv2.circle(frame, (centro_pista_x, y_control), 10, (0, 0, 255), -1)
    cv2.line(frame, (x_izq, y_control), (x_der, y_control), (255, 255, 255), 2)
    
    print(f"Umbral Otsu actual: {umbral}")

    cv2.imshow("Camara Real - Centro de Pista", frame)
    cv2.imshow("Camara prueba", frame_binario)

    # Detener el programa si presionas la letra 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()