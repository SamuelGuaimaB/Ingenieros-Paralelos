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

    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    promedio_s = np.mean(frame_hsv[:, :, 1])
    promedio_v = np.mean(frame_hsv[:, :, 2])

    min_s = int(max(40, promedio_s * 0.6))
    min_v = int(max(30, promedio_v * 0.5))

    #verde_mascara = cv2.inRange(frame_hsv, np.array([35, min_s, min_v]), np.array([85, 255, 255]))
    #rojo_mascara1 = cv2.inRange(frame_hsv, np.array([0, min_s, min_v]), np.array([10, 255, 255]))
    #rojo_mascara2 = cv2.inRange(frame_hsv, np.array([165, min_s, min_v]), np.array([179, 255, 255]))
    #mascara_roja = cv2.bitwise_or(rojo_mascara1, rojo_mascara2)
    naranja_mascara = cv2.inRange(frame_hsv, np.array([5, min_s, min_v]), np.array([15, 255, 255]))
    azul_mascara = cv2.inRange(frame_hsv, np.array([90, min_s, min_v]), np.array([130, 255, 255]))

    solo_azul = cv2.bitwise_and(frame, frame, mask=azul_mascara)
    solo_naranja = cv2.bitwise_and(frame, frame, mask=naranja_mascara)

    cv2.putText(frame, f"Umbral Dinamico: [{179}, {min_s}, {min_v}]", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    cv2.imshow("Camara prueba", frame)
    cv2.imshow("Mascara (Blanco y Negro)", naranja_mascara)
    cv2.imshow("Mascara (Blanco y Negro)", azul_mascara)
    cv2.imshow("Resultado Final (Solo Azul)", solo_azul)
    cv2.imshow("Resultado Final (Solo Azul)", solo_naranja)
    
    
    # Detener el programa si presionas la letra 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()