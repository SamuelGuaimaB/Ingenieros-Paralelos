# WRO2026 Future Engineers – Ingenieros Paralelos

## Engineering materials // Ingenieros-Paralelo

Proyecto Competencia de Robotica WRO

Una descripción breve en inglés (no menor a 5,000 caracteres) de la solución desarrollada

This repository contains engineering materials of a self-driven vehicle's model participating in the WRO Future Engineers competition in the season 2026

## Content

* `t-photos` contains 2 photos of the team (an official one and one funny photo with all team members)
* `v-photos` contains 6 photos of the vehicle (from every side, from top and bottom)
* `video` contains the video.md file with the link to a video where driving demonstration exists
* `schemes` contains one or several schematic diagrams in form of JPEG, PNG or PDF of the electromechanical components illustrating all the elements (electronic components and motors) used in the vehicle and how they connect to each other.
* `src` contains code of control software for all components which were programmed to participate in the competition
* `models` is for the files for models used by 3D printers, laser cutting machines and CNC machines to produce the vehicle elements. If there is nothing to add to this location, the directory can be removed.
* `other` is for other files which can be used to understand how to prepare the vehicle for the competition. It may include documentation how to connect to a SBC/SBM and upload files there, datasets, hardware specifications, communication protocols descriptions etc. If there is nothing to add to this location, the directory can be removed.

## Introduction

_This part must be filled by participants with the technical clarifications about the code: which modules the code consists of, how they are related to the electromechanical components of the vehicle, and what is the process to build/compile/upload the code to the vehicle’s controllers._

## Acerca de nosotros 👥

>Miembros del equipo
- Samuel Guaimacuto
- Andrés Villareal
- David Xu

_Somos un equipo conformado por estudiantes de Ingeniería Informática de la Universidad Gran Mariscal de Ayacucho (UGMA) del núcleo Barcelona, siendo nuestra primera participación en una competición WRO, compitiendo en la categoría Futuros Ingenieros. Lo que nos inspiró a formar parte de este torneo fueron las ganas de aprender acerca del mundo de la robótica, queriendo enfrentarnos a este desafío para lograrlo. Estamos muy agradecidos por todos aquellos familiares, profesores y compañeros que nos apoyaron en el desarrollo del proceso de nuestro proyecto, ya que sin su apoyo no hubiese sido posible lograr lo que nos propusimos._


## Vision Management 🖥️

- **Logitech C922 Web Camera**

<table>
  <tr>
    <td align="center" width="300" >
      <img src="./resources/Logitech C922.png " alt="Logitech C922 Webcam" >
    </td>
    <td>
      <h3>Specifications:</h3>
      <ul>
        <li>Max resolution: 1080p at 30fps (Full HD) or 720p at 60fps (HD) </li>
        <li>Field of View (FoV): 78° diagonal </li>
        <li>Focus Type: Autofocus </li>
        <li>Lens Technology: Full HD glass lens with automatic light correction</li>
        <li>Audio: Dual omnidirectional stereo microphones </li>
        <li>Connectivity: Wired USB 2.0 (includes a 5-foot / 1.5m cable)</li>
      </ul>
    </td>
  </tr>
</table>

The Logitech C922 Pro Stream is a popular, high-definition webcam designed specifically for content creators, streamers, and professionals. It offers sharp video resolution, smooth frame rates for fluid motion, and a convenient low-light correction feature. In our project, we used it as the eye of the car, catching the view of the environment.

- **Raspberry Pi 4**

<table>
  <tr>
    <td align="center" width="300" >
      <img src="./resources/Raspberry Pi 4.png " alt="Raspberry Pi 4" >
    </td>
    <td>
      <h3>Specifications:</h3>
      <ul>
        <li>Processor: Quad-Core Cortex-A72 (ARM v8) 64-bit SoC @ 1.5–1.8 GHz </li>
        <li>Memory: 1GB, 2GB, 4GB, or 8GB LPDDR4-3200 SDRAM </li>
        <li>Video: Dual micro-HDMI ports supporting 4K @ 60fps </li>
        <li>Connectivity: Gigabit Ethernet, 2.4/5.0 GHz Wi-Fi, and Bluetooth 5.0 </li>
        <li>USB: 2x USB 3.0, 2x USB 2.0 ports </li>
        <li>Power: USB-C (5V/3A) or Power over Ethernet (PoE) supported </li>
      </ul>
    </td>
  </tr>
</table>

The Raspberry Pi 4 Model B is a credit card-sized, single-board computer. It functions as a fully operational, low-cost computer capable of desktop computing, media streaming, home automation, and robotics, while using only a fraction of the power of a standard desktop. <b>This piece of hardware acts as the brain of the car, with software capable to process the view of the web camera, deciding which is the most appropriate action to execute, according the scenery, to later let our microcontroller perform it</b>.

<hr>

<h2> Software implemented in the Raspberry </h2>

<img src="./resources/GoogleMediapipe.png " alt="Mediapipe Logo" height="70" >

_Is an open-source, cross-platform framework developed by Google that allows developers to build high-performance machine learning (ML) pipelines for processing "streaming" media like video and audio. It is specifically optimized for real-time performance on edge devices such as mobile phones (Android, iOS), web browsers, and embedded systems like Raspberry Pi. <b>Implementing this framework with the purpose of obstacles detection, the camera is able to detect objets in real time supported by the dataset clasificador_pista.tflite</b>._


<img src="./resources/OpenCV_Logo.png " alt="OpenCV Logo" height="100" width="200">

_Open Source Computer Vision Library is a massive, free, and open-source software library packed with tools for real-time computer vision, image processing, and machine learning. It is designed to act as the eyes of a system, allowing computers to read, analyze, and understand visual data like images and videos. Computers do not see images, they interpret them as huge numeric matrices of pixels. <b>OpenCV provides functions to manipulate these numbers rapidly, that is the reason why we applied this library, allowing the autonomous car to detect colors, performing mathematical operations to achieve it</b>._

<hr>

## Mobility Management ⚙️

- **Arduino Uno**

<table>
  <tr>
    <td align="center" >
      <img src="./resources/Arduino_Uno.png " alt="Arduino Uno" width="300" >
    </td>
    <td>
      <h3>Specifications:</h3>
      <ul>
        <li> Microcontroller: ATmega328P </li>
        <li> Operating Voltage: 5V </li>
        <li> Input Voltage (Recommended): 7V to 12V </li>
        <li> Input Voltage (Limit): 6V to 20V </li>
        <li> Digital I/O Pins: 14 (6 provide PWM output) </li>
        <li> Analog Input Pins: 6 </li>
        <li> DC Current per I/O Pin: 20mA </li>
        <li> Clock Speed: 16MHz </li>
        <li> Flash Memory: 32KB (of which 0.5KB is used by the bootloader) </li>
        <li> SRAM: 2KB </li>
        <li> EEPROM: 1KB </li>
      </ul>
    </td>
  </tr>
</table>

The Arduino Uno is a beginner-friendly, open-source microcontroller board used for building digital devices and interactive projects. It acts as the brain of a project, allowing people to read inputs (like a sensor, button, or temperature reading) and turn them into outputs (like moving a motor or turning on an LED). Since it is our first time participating in this kind of tournaments, we decided to begin trying this model of Arduino. 

<hr>

<h3> Arduino Code (C++) </h3>

The Servo.h library is a built-in library for Arduino that allows people to easily control RC (hobby) servo motors. It simplifies the process by handling the precise pulse-width modulation (PWM) signals in the background, allowing your motor to rotate to specific angles (usually 0 to 180 degrees) or at continuous speeds. <b>We employed this library to manage the angles of our servo motor, depending the instruction to execute. When the microcontroller receives the decision taken by the Raspberry, the Arduino's code checks the action it is going to perform and how, sending small electric pulses to the driver</b>.

// Modify or take as reference
En nuestro carro autónomo, una vez el Arduino Uno haya recibido la cadena de dos caracteres enviada por la Raspberry Pi 4, se procede a procesarla. El código de Arduino escrito en C++, contiene una serie de funciones, ciclos y condicionales necesarias para el procesamiento y ejecución de la instrucción correspondiente, para que la placa Arduino posteriormente posea la capacidad de enviar pequeñas señales de corriente al driver, indicándole a éste la manera en la que va a alimentar con corriente el servo motor, pudiendo así ejecutar de manera eficaz la indicación solicitada. 

<hr>

- **L298N Driver**

<table>
  <tr>
    <td align="center" width="300" >
      <img src="./resources/Driver_L298N.png " alt="Driver L298N" >
    </td>
    <td>
      <h3>Specifications:</h3>
      <ul>
        <li> Driver IC: STMicroelectronics L298N </li>
        <li> Motor Supply Voltage (Vs): 5V to 35V </li>
        <li> Peak Output Current: 2A per channel (4A total max) </li>
        <li> Logic Supply Voltage (Vss): 5V to 7V </li>
        <li> Maximum Power Dissipation: 20W at 75°C </li>
        <li> Control Signal Level: Low (-0.3V to 1.5V), High (2.3V to Vss) </li>
      </ul>
    </td>
  </tr>
</table>

The L298N is a dual H-Bridge motor driver module used to control the direction and speed of DC or stepper motors. It acts as a bridge between the microcontroller, the Arduino Uno, and high-power motors (in our case the servo motor and the encoder motor), supplying the necessary current and voltage. 

- **HC-SR04 Ultrasonic Sensors**



- **Fischertechnik Maker Kit Car**



<h3> Other components the kit contains </h3>

> Servomotor

What it is: A specialized motor designed to turn to a specific, exact angle (usually between 0° and 180°) and hold that position.
Function: It connects directly to the front steering knuckles of the chassis.
Robotics Role: It controls the steering mechanism. Unlike the drive motor, you do not program it to spin continuously. Instead, you command it to change degrees (e.g., "turn 15 degrees left" or "return to 0 degrees to go straight"), giving your robot precise navigation capabilities.

> Encoder Motor or C Motor

What it is: The primary drive engine of the vehicle. It does not just spin; it counts its own rotations.
Function: It provides the driving power (traction) to move the car forward and backward.
Robotics Role: The built-in encoder sends digital pulses back to your controller (like an Arduino). This allows you to measure exactly how far the car has traveled, calculate its speed, and program precise movements (e.g., "move forward exactly 50 centimeters").

> Differential Gear

What it is: A mechanical gearbox located between the two driven wheels.
Function: It allows the left and right wheels to rotate at different speeds while still receiving power from the motor.
Robotics Role: When a car turns, the outside wheel has to travel a longer distance than the inside wheel. Without a differential, the wheels would lock up, slip, or skid during turns. This component ensures smooth, realistic cornering and prevents the robot from losing traction.

## Power Management 🔋

- **LX-2BUPS UPS**



- **Lithium batteries**



- **Micro Protoboard**



## Components abstract

| Component                            | Cantidad | Precio/Unidad ($) | Total ($)   |
|--------------------------------------|----------|-------------------|-------------|
| **Raspberry Pi 4**                   | 1        | **21.42**         | **21.42**   |
| **L298N Driver**                     | 1        | **22.45**         | **22.45**   |
| **Arduino Uno**                      | 1        | **19.92**         | **19.92**   |
| **HC-SR04 Ultrasonic Sensors**       | 4        | **4.05**          | **4.05**    |
| **Micro Protoboard**                 | 1        | **80.00**         | **80.00**   |
| **Fischertechnik Maker Kit Car**     | 1        | **8.50**          | **8.50**    |
| **Logitech C922 Web Camera**         | 1        | **8.50**          | **8.50**    |
| **LX-2BUPS UPS**                     | 2        | **8.50**          | **8.50**    |
| **Lithium batteries**                | 4        | **80.00**         | **80.00**   |
| **Micro Protoboard**                 | 1        | **80.00**         | **80.00**   |

## Obstacle Management

// Explain the function of every component in the challenges

>Propósito del equipo

Nuestro objetivo es crear un carro autónomo con la capacidad de superar las carreras de la competición en la categoría Futuros Ingenieros.

1) Desafío Abierto (Open Challenge): El vehículo autónomo debe completar 3 vueltas en un circuito donde las paredes interiores cambian de posición de forma aleatoria en cada ronda.

2) Desafío de Obstáculos (Obstacle Challenge): El vehículo debe completar 3 vueltas en una pista con obstáculos (postes rojos y verdes) colocados aleatoriamente. Los postes indican el lado del carril por el que debe pasar el coche sin derribarlos, finalizando con un estacionamiento en paralelo.

## Componentes y Hardware ⚙️

### Descripción y funcionalidades

- `Raspberry Pi 4`:

> [!IMPORTANT]
> Specifications
>- Procesador: Broadcom BCM2711, ARM Cortex-A72 de cuatro núcleos.
>- Memoria RAM: Disponible en diferentes capacidades (desde 1 GB hasta 8 GB). /
>- Conectividad: Puertos USB 3.0, Gigabit Ethernet, Wi-Fi de doble banda y Bluetooth.
>- Gráficos: Soporta decodificación de video 4K en hasta dos monitores simultáneamente.
>- Alimentación: Se alimenta a través de un puerto USB-C.

- `Driver L298N`

Es un módulo electrónico basado en un circuito integrado con tecnología de Puente H. Permite controlar la dirección, inversión y velocidad de motores de forma segura desde un microcontrolador, como Arduino. 

- [x] Voltaje de motor (potencia): Desde 5V hasta 35V DC.
- [x] Corriente de salida: Hasta 2A por canal (con picos máximos de hasta 3A a 4A).
- [x] Voltaje lógico: Funciona a 5V para la comunicación con el microcontrolador.
- [x] Consumo de corriente (lógica): Entre 0 y 36mA.
- [x] Potencia máxima: 25W.
- [x] Protección: Incorpora protección térmica para evitar que se queme por sobrecalentamiento y disipador de calor. 

- `Arduino Uno`

Es una placa controladora de electrónica de código abierto. Su función es actuar como el cerebro de circuitos interactivos, permitiendo leer sensores y controlar motores o luces al conectar la placa a una computadora y programarla fácilmente.

- [x] Microcontrolador: ATmega328P de 8 bits.
- [x] Voltaje de Operación: 5V.
- [x] Voltaje de Entrada Recomendado: 7V a 12V (límite de 6V a 20V).
- [x] Pines de E/S Digitales: 14 pines, 6 de ellos ofrecen salida PWM.
- [x] Pines de Entradas Analógicas: 6 pines.
- [x] Velocidad de Reloj: 16MHz.
- [x] Memoria Flash: 32KB, de los cuales 0.5KB son utilizados por el gestor de arranque.
- [x] Memoria SRAM: 2KB.
- [x] Memoria EEPROM: 1KB. 

- `Micro Protoboard`: 


- `Fischertechnik Maker Kit Car`:

El Fischertechnik Maker Kit Car (modelo 571900) es un chasis robótico móvil básico. Funciona como una plataforma abierta y altamente extensible para construir coches robóticos personalizados. El kit proporciona la base mecánica y de tracción del vehículo:

- [x] Motor codificador: Para un control preciso del movimiento y la velocidad.
- [x] Engranaje diferencial: Permite que las ruedas giren a diferentes velocidades en las curvas.
- [x] Mecanismo de dirección: Equipado con un servomotor para un guiado exacto del eje delantero.

A diferencia de otros kits tradicionales de la marca, la línea Maker está pensada para integrarse con tecnologías externas, siendo este factor muy óptimo para nuestro proyecto: 

- [x] Sin controlador incluido: El kit no trae un cerebro electrónico, ya que está diseñado para la implementación de una placa.
- [x] Compatibilidad de hardware: Se adapta de forma ideal a controladores populares como Arduino Uno, Arduino Mega o Raspberry Pi (modelos 3, 4 y 5).
- [x] Soportes en impresión 3D: Fischertechnik proporciona de forma gratuita los archivos y datos 3D para imprimir los soportes específicos de estas placas de desarrollo.
- [x] Diseño Digital: El chasis se puede ampliar con sensores y actuadores adicionales, los cuales se pueden diseñar de forma previa en el software Fischertechnik Design Studio.

## Software / Tecnologías 🖥️

>Python: 
- `Mediapipe`: Es un marco de código abierto desarrollado por Google que permite construir soluciones de inteligencia artificial y aprendizaje automático, principalmente enfocado en el análisis y procesamiento de visión artificial en tiempo real (vídeo, imágenes y audio). Con la implementación de este framework con la finalidad de detección de obstáculos, la cámara logra detectar objetos en tiempo real gracias al dataset clasificador_pista.tflite.

- `OpenCV (Open Source Computer Vision Library)`: Es una librería de código abierto especializada en visión por computadora, procesamiento de imágenes y aprendizaje automático. Permite que las computadoras tengan visión e interpreten información visual a partir de fotografías o videos en tiempo real. Esta librería se tomó en cuenta para nuestro proyecto con el fin de la identificación de colores para realizar acciones específicas:

1) Rojo: Esquivar obstáculo por la derecha.
2) Verde: Esquivar obstáculo por la izquierda.
3) Magenta: Estacionamiento.
4) Naranja: Indicar giro a la derecha.
5) Azul: Indicar giro a la izquierda.

El código escrito en el lenguaje Python envía strings conformados por dos caractares para posteriormente ser procesados en el Arduino, pudiendo estas cadenas variar dependiendo de lo detectado en la cámara y el gestionamiento de dicha información por Mediapipe junto a OpenCV:

- Dirección: F(recto), I(izquierda), D(derecha), 1(giro leve izquierda), 2(giro leve dereche), S(parar).
- Potencia: H(alta/255), M(media/195), L(baja/115).


>Arduino (C++):

- `servo.h`: Esta librería es el archivo de código estándar incluido en el entorno de desarrollo de Arduino que facilita el control preciso de servomotores. Su función es generar las señales eléctricas necesarias (modulación por ancho de pulsos o PWM) para mover el eje del motor a un ángulo exacto.

En nuestro carro autónomo, una vez el Arduino Uno haya recibido la cadena de dos caracteres enviada por la Raspberry Pi 4, se procede a procesarla. El código de Arduino escrito en C++, contiene una serie de funciones, ciclos y condicionales necesarias para el procesamiento y ejecución de la instrucción correspondiente, para que la placa Arduino posteriormente posea la capacidad de enviar pequeñas señales de corriente al driver, indicándole a éste la manera en la que va a alimentar con corriente el servo motor, pudiendo así ejecutar de manera eficaz la indicación solicitada.
