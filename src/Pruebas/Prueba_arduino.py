import serial
import time

arduino = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(2)

ultimo_estado = 1
estado = 1

print("Esperando señal...")

while True:
    if arduino.in_waiting > 0:
        linea = arduino.readline().decode('utf-8').rstrip()
                                
        if linea == "BTN:1":
            estado += 1

    if estado != ultimo_estado:
        if estado == 2:
            angulo = 86
            velocidad = 200

            cadena_datos = f"<{velocidad},{angulo}>\n"
            arduino.write(cadena_datos.encode('utf-8'))
            print(f"Dato <{velocidad},{angulo}> enviado.")

            ultimo_estado = estado

        elif estado == 3:
            angulo = 86
            velocidad = 0

            cadena_datos = f"<{velocidad},{angulo}>\n"
            arduino.write(cadena_datos.encode('utf-8'))
            print(f"Dato <{velocidad},{angulo}> enviado.")

            estado = 1

arduino.close()