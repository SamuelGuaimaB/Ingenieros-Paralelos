import cv2
import numpy as np

def nada(x):
    pass

# Inicializar cámara con resolución baja (320x240)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

cv2.namedWindow('Controles', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Controles', 450, 450)

# Trackbar para seleccionar el color a calibrar
cv2.createTrackbar('MODO (0=Piso, 1=Naranja, 2=Azul)', 'Controles', 0, 2, nada)

# Trackbars para los rangos de color HSV (Hue, Saturation, Value)
cv2.createTrackbar('H Min', 'Controles', 5, 179, nada)
cv2.createTrackbar('H Max', 'Controles', 25, 179, nada)
cv2.createTrackbar('S Min', 'Controles', 100, 255, nada)
cv2.createTrackbar('S Max', 'Controles', 255, 255, nada)
cv2.createTrackbar('V Min', 'Controles', 100, 255, nada)
cv2.createTrackbar('V Max', 'Controles', 255, 255, nada)

# Trackbar para el umbral de la pista (blanco y negro)
cv2.createTrackbar('Umbral Piso', 'Controles', 95, 255, nada)

modo_anterior = 0

print("\n--- CALIBRADOR DE SENTIDO DE PISTA ---")
print("Usa el deslizador 'MODO' para cambiar entre Naranja, Azul y Piso.")
print("Presiona 'p' para imprimir los valores en la consola.")
print("Presiona 'q' para salir.")
print("--------------------------------------\n")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    modo_actual = cv2.getTrackbarPos('MODO (0=Piso, 1=Naranja, 2=Azul)', 'Controles')
    
    # Auto-ajuste de valores por defecto al cambiar de modo
    if modo_actual != modo_anterior:
        if modo_actual == 0: # PISO (Blanco y Negro)
            cv2.setTrackbarPos('Umbral Piso', 'Controles', 95)
        elif modo_actual == 1: # NARANJA
            # Valores iniciales típicos para el naranja
            cv2.setTrackbarPos('H Min', 'Controles', 5)
            cv2.setTrackbarPos('H Max', 'Controles', 20)
            cv2.setTrackbarPos('S Min', 'Controles', 120)
            cv2.setTrackbarPos('S Max', 'Controles', 255)
            cv2.setTrackbarPos('V Min', 'Controles', 120)
            cv2.setTrackbarPos('V Max', 'Controles', 255)
        elif modo_actual == 2: # AZUL
            # Valores iniciales típicos para el azul
            cv2.setTrackbarPos('H Min', 'Controles', 100)
            cv2.setTrackbarPos('H Max', 'Controles', 130)
            cv2.setTrackbarPos('S Min', 'Controles', 100)
            cv2.setTrackbarPos('S Max', 'Controles', 255)
            cv2.setTrackbarPos('V Min', 'Controles', 50)
            cv2.setTrackbarPos('V Max', 'Controles', 255)
            
        modo_anterior = modo_actual

    # Leer valores de los trackbars
    h_min = cv2.getTrackbarPos('H Min', 'Controles')
    h_max = cv2.getTrackbarPos('H Max', 'Controles')
    s_min = cv2.getTrackbarPos('S Min', 'Controles')
    s_max = cv2.getTrackbarPos('S Max', 'Controles')
    v_min = cv2.getTrackbarPos('V Min', 'Controles')
    v_max = cv2.getTrackbarPos('V Max', 'Controles')
    thresh_val = cv2.getTrackbarPos('Umbral Piso', 'Controles')

    # Usamos un ROI amplio para detectar pilares de lejos
    roi = frame[40:180, 0:320]

    if modo_actual == 0:
        # MODO 0: PISTA (Escala de grises)
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        _, mascara = cv2.threshold(blur, thresh_val, 255, cv2.THRESH_BINARY)
        resultado = cv2.cvtColor(mascara, cv2.COLOR_GRAY2BGR)
        info = f"MODO: PISO | Umbral: {thresh_val}"
    
    else:
        # MODO 1 y 2: COLORES (Naranja y Azul en HSV)
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
        
        # Binarizar por color (Pone blanco lo que coincide, negro el resto)
        mascara = cv2.inRange(hsv, lower, upper)
        
        # Limpiar ruido pequeño
        kernel = np.ones((3,3), np.uint8)
        mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
        
        # Superponer la máscara en la imagen real
        resultado = cv2.bitwise_and(roi, roi, mask=mascara)
        
        # Mostrar el área más grande detectada
        contornos = cv2.countNonZero(mascara)
        area_max = 0
        #if contornos:
            #c_max = max(contornos, key=cv2.contourArea)
            #area_max = cv2.contourArea(c_max)
            # Dibujar el contorno en verde en la imagen resultado
            #cv2.drawContours(resultado, [c_max], -1, (0, 255, 0), 2)
            
        color_str = "NARANJA" if modo_actual == 1 else "AZUL"
        info = f"{color_str} | H:[{h_min}-{h_max}] S:[{s_min}-{s_max}] V:[{v_min}-{v_max}] | Area Max: {int(area_max)}"

    # Escribir la info en la pantalla
    cv2.putText(roi, info, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)

    # Ventanas de visualización
    cv2.imshow('1. Vision Real (ROI)', roi)
    cv2.imshow('2. Mascara (BLANCO = Detectado)', mascara)
    cv2.imshow('3. Resultado Final', resultado)

    tecla = cv2.waitKey(1) & 0xFF
    
    if tecla == ord('p'):
        print(f"\n[VALORES GUARDADOS] {info}")
    elif tecla == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
