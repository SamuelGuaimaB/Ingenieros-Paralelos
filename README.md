# WRO2025 Future Engineers – Ingenieros Paralelos

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

Somos un equipo conformado por estudiantes de Ingeniería Informática de la Universidad Gran Mariscal de Ayacucho (UGMA) del núcleo Barcelona.

>Propósito del equipo

Nuestro objetivo es crear un carro autónomo con la capacidad de superar las carreras de la competencia en la categoría Futuros Ingenieros.
- 1. Desafío Abierto (Open Challenge): El vehículo autónomo debe completar 3 vueltas en un circuito donde las paredes interiores cambian de posición de forma aleatoria en cada ronda.

- 2. Desafío de Obstáculos (Obstacle Challenge): El vehículo debe completar 3 vueltas en una pista con obstáculos (postes rojos y verdes) colocados aleatoriamente. Los postes indican el lado del carril por el que debe pasar el coche sin derribarlos, finalizando con un estacionamiento en paralelo.
<img src="pistaObstaculos" alt="Pista con Obstáculos" width="500" height="300">

 
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

### Descripcion y funcionalidades

- `Raspberry Pi 4`: 
- `Driver L298N`: 
- `Arduino Uno`: 
- `Protoboard`: 
- `Kit Fischertechnik Maker Kit Car`: 

## Software / Tecnologías 🖥️

>Python: 
- `Mediapipe`: Es un marco de código abierto desarrollado por Google que permite construir soluciones de inteligencia artificial y aprendizaje automático, principalmente enfocado en el análisis y procesamiento de visión artificial en tiempo real (vídeo, imágenes y audio). Con la implementación de este framework con la finalidad de detección de obstáculos, la cámara logra detectar objetos en tiempo real usando el modelo clasificador_pista.tflite.
- `OpenCV (Open Source Computer Vision Library)`: Es una librería de código abierto especializada en visión por computadora, procesamiento de imágenes y aprendizaje automático. Permite que las computadoras tengan visión e interpreten información visual a partir de fotografías o videos en tiempo real. Permite configurar rangos específicos de color para aislar un tono con máxima precisión. Para lograrlo, no se usa el formato de color común (RGB), sino el espacio de color HSV (Tono, Saturación, Valor). Este formato separa el color puro de la iluminación, lo que evita que las sombras o los brillos confundan al sistema. Esta librería se tomó en cuenta para nuestro proyecto con la finalidad de la identificación de colores para realizar acciones específicas:
--Rojo: Esquivar obstáculo por la derecha.

>C++:

