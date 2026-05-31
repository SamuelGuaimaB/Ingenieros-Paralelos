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

>Propósito del equipo

Nuestro objetivo es crear un carro autónomo con la capacidad de superar las carreras de la competición en la categoría Futuros Ingenieros.

1) Desafío Abierto (Open Challenge): El vehículo autónomo debe completar 3 vueltas en un circuito donde las paredes interiores cambian de posición de forma aleatoria en cada ronda.

2) Desafío de Obstáculos (Obstacle Challenge): El vehículo debe completar 3 vueltas en una pista con obstáculos (postes rojos y verdes) colocados aleatoriamente. Los postes indican el lado del carril por el que debe pasar el coche sin derribarlos, finalizando con un estacionamiento en paralelo.
<img src="pistaObstaculos" alt="Pista con Obstáculos" width="500" height="300">

## Hardware and Software employed to Vision Management

- **Logitech C922**:

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

- **Raspberry Pi 4**:

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

The Raspberry Pi 4 Model B is a credit card-sized, single-board computer. It functions as a fully operational, low-cost computer capable of desktop computing, media streaming, home automation, and robotics, while using only a fraction of the power of a standard desktop. 

> <h3> Mediapipe </h3>

<hr>

_Is an open-source, cross-platform framework developed by Google that allows developers to build high-performance machine learning (ML) pipelines for processing "streaming" media like video and audio. It is specifically optimized for real-time performance on edge devices such as mobile phones (Android, iOS), web browsers, and embedded systems like Raspberry Pi. With the implementation of this framework with the purpose of obstacles detection, the camera is able to detect objets in real time supported by the dataset clasificador_pista.tflite._

> OpenCV

_OpenCV (Open Source Computer Vision Library) is a massive, free, and open-source software library packed with tools for real-time computer vision, image processing, and machine learning. It is designed to act as the eyes of a system, allowing computers to read, analyze, and understand visual data like images and videos. Computers do not see images, they interpret them as huge numeric matrices of pixels. OpenCV provides functions to manipulate these numbers rapidly, that is the reason why we applied this library, allowing the autonomous car to detect colors, performing mathematical operations to achieve it._

## Mobility Management



## Componentes y Hardware ⚙️

| Componentes                          | Cantidad | Precio/Unidad ($) | Total ($)   |
|--------------------------------------|----------|-------------------|-------------|
| **Raspberry Pi 4**                   | 1        | **21.42**         | **21.42**   |
| **Driver L298N**                     | 1        | **22.45**         | **22.45**   |
| **Arduino Uno**                      | 1        | **19.92**         | **19.92**   |
| **Sensores de Ultrasonido**          | 4        | **4.05**          | **4.05**    |
| **Micro Protoboard**                 | 1        | **80.00**         | **80.00**   |
| **Fischertechnik Maker Kit Car**     | 1        | **8.50**          | **8.50**    |
| **Cámara Logitech C922**             | 1        | **8.50**          | **8.50**    |
| **UPS ----           .**             | 1        | **8.50**          | **8.50**    |


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
