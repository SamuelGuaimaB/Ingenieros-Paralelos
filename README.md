# WRO2026 Futuros Ingenieros – Ingenieros Paralelos

## Acerca de Nosotros

>Integrantes del equipo
- Samuel Guaimacuto
- Andrés Villareal
- David Xu

_Somos un equipo venezolano conformado por estudiantes de ingeniería informática de la Universidad Gran de Ayacucho (UGMA), núcleo Barcelona, siendo esta nuestra primera vez participando en una competición WRO, compitiendo en la categoría Futuros Ingenieros. Nuestra inspiración de formar parte de este torneo fue el deseo de aprender acerca del mundo de la robótica, queriendo enfrentarnos a desafíos para lograrlo. Estamos agradecidos con toda nuestra familia, profesores y compañeros, ya que sin el apoyo de ellos no hubiésemos logrado lo que nos propusimos_.

<img src="./t-photos/igshiix0ajvkbmse051z.jpeg" alt="Foto de Nosotros" width="500">

<hr>

## Tabla de Contenido

<!-- toc -->

- [Vista previa del carro](#vista-previa-del-carro)
- [Clip del carro en acción](#clip-del-carro-en-acción)
- [Componentes usados y precio estimado](#componentes-usados-y-precio-estimado)
- [Vision Management](#vision-management)
  - [Logitech C922 Web Camera](#logitech-c922-web-camera)
  - [Raspberry Pi 4](#raspberry-pi-4)
- [Mobility Management](#mobility-management)
  - [Arduino Uno](#arduino-uno)
  - [L298N Driver](#l298n-driver)
  - [Fischertechnik Maker Kit Car](#fischertechnik-maker-kit-car)
  - [Ackermann Mechanism](#ackermann-mechanism)
  - [Ackermann Principle](#ackermann-principle)
  - [Ackermann in our project](#ackermann-in-our-project)
- [Power Management](#power-management)
  - [LX-2BUPS UPS](#lx-2bups-ups)
  - [Ultrafire TR 18650 Batteries](#ultrafire-tr-18650-batteries)
- <a href="src"> Obstacle Management </a>

<!-- tocstop -->

<hr>

## Vista previa del carro

<table>
  <tr>
    <td align="center"><b>Superior</b><br><img src="./v-photos/IMG_5101.JPG" width="300"></td>
    <td align="center"><b>Frontal</b><br><img src="./v-photos/IMG_5102.JPG" width="300"></td>
    <td align="center"><b>Izquierda</b><br><img src="./v-photos/IMG_5103.JPG" width="300"></td>
  </tr>
  <tr>
    <td align="center"><b>Inferior</b><br><img src="./v-photos/IMG_5104.JPG" width="300"></td>
    <td align="center"><b>Trasera</b><br><img src="./v-photos/IMG_5105.JPG" width="300"></td>
    <td align="center"><b>Derecha</b><br><img src="./v-photos/IMG_5100.JPG" width="300"></td>
  </tr>
</table>

<hr>

## Clip del carro en acción

<img src="/resources/Car Preview.gif" alt="Car Preview" width="80%">

<a href="https://www.youtube.com/watch?v=6vZ5giluS2M"> Presiona aquí para ver el video completo </a>

<hr>

## Componentes usados y precio estimado

| Componente | Cantidad | Precio Estimado por Unidad | Subtotal Estimado | Referencia |
|---|---:|---:|---:|---|
| Raspberry Pi 4 Modelo B 4GB Kit | 1 | $200.00 | $200.00 | MercadoLibre Venezuela |
| Arduino Uno R3 | 1 | $9.99 | $9.99 | MercadoLibre Venezuela |
| Driver de Motor L298N | 1 | $6.99 | $6.99 | MercadoLibre Venezuela |
| Cámara Logitech C922 | 1 | $70.00 | $70.00 | MercadoLibre Venezuela |
| Módulo UPS LX-2BUPS | 1 | $17.80 | $17.80 | MercadoLibre Venezuela |
| Batería 18650 3.7V | 4 | $5.00 | $20.00 | MercadoLibre Venezuela |
| Fischertechnik Maker Kit Car | 1 | $115.33 | $115.33 | eBay |

### Total Estimado: $443.10

<hr>

## Manejo de la visión

- #### Cámara Web Logitech C922

<table>
  <tr>
    <td align="center" width="300" >
      <img src="./resources/Logitech C922.png" alt="Logitech C922 Webcam" >
    </td>
    <td>
      <h3>Especificaciones:</h3>
      <ul>
        <li>Resolución máxima: 1080p a 30 fps (Full HD) o 720p a 60 fps (HD)</li>
        <li>Campo de visión (FoV): 78° en diagonal</li>
        <li>Tipo de enfoque: Enfoque automático</li>
        <li>Tecnología de la lente: Lente de cristal Full HD con corrección automática de la luz</li>
        <li>Audio: Micrófonos estéreo omnidireccionales duales</li>
        <li>Conectividad: USB 2.0 con cable (incluye un cable de 1,5 m)</li>
      </ul>
    </td>
  </tr>
</table>

La Logitech C922 es una cámara web de gran popularidad con alta definición diseñada especialmente para creadores de contenido, streamers y profesionales. Ofrece una resolución de video nítida, una velocidad de fotogramas fluida para un movimiento sin interrupciones y la capacidad de corrección en baja iluminación. <b>En nuestro proyecto, la utilizamos como el ojo del carro, capturando la vista del entorno para que se pudiesen realizar acciones como la identificación de esquinas y detección de objetos, de tal manera que las fotos tomadas por la cámara pudiesen ser procesadas posteriormente por el software presente en la Raspberry. Se decidió optar por esta como el ojo del vehículo debido a las buenas reseñas que encontramos investigando acerca de posibles cámaras que se podían emplear.</b>

<hr>

- #### Raspberry Pi 4

<table>
  <tr>
    <td align="center" width="300" >
      <img src="./resources/Raspberry Pi 4.png " alt="Raspberry Pi 4" >
    </td>
    <td>
      <h3>Especificaciones:</h3>
      <ul>
        <li>Procesador: SoC Cortex-A72 de cuatro núcleos (ARM v8) de 64 bits a 1,5–1,8 GHz</li>
        <li>Memoria: 4 GB de SDRAM LPDDR4-3200</li>
        <li>Vídeo: Dos puertos micro-HDMI compatibles con 4K a 60 fps</li>
        <li>Conectividad: Gigabit Ethernet, Wi-Fi de 2,4/5,0 GHz y Bluetooth 5.0</li>
        <li>USB: 2 puertos USB 3.0 y 2 puertos USB 2.0</li>
        <li>Alimentación: Compatible con USB-C (5 V/3 A) o alimentación a través de Ethernet (PoE)</li>
      </ul>
    </td>
  </tr>
</table>

La Raspberry Pi 4 Modelo B es una computadora de placa única del tamaño de una tarjeta de crédito. Funciona como una computadora de bajo costo totalmente operativa, capaz de realizar tareas de computación de escritorio, transmisión de contenido multimedia, automatización del hogar y de robótica, utilizando solo una fracción de la potencia de una computadora de escritorio estándar. <b>Este componente actúa como el cerebro del vehículo, con el software implementado tiene la capacidad de procesar las imágenes de la cámara web, decidiendo cual es la acción más apropiada a ejecutar dependiendo del entorno en el que se encuentre el carro, para que luego nuestro microcontrolador, el Arduino Uno, la ejecute</b>.

<a href="src"> Ver el código implementado en la Raspberry </a>

<hr>

## Manejo de la movilidad

- #### Arduino Uno

<table>
  <tr>
    <td align="center" >
      <img src="./resources/Arduino_Uno.png " alt="Arduino Uno" width="300" >
    </td>
    <td>
      <h3>Especificaciones:</h3>
      <ul>
        <li> Microcontrolador: ATmega328P </li>
        <li> Voltaje de funcionamiento: 5 V </li>
        <li> Voltaje de entrada (recomendado): 7 V a 12 V </li>
        <li> Voltaje de entrada (límite): 6 V a 20 V </li>
        <li> Pines de E/S digitales: 14 (6 proporcionan salida PWM) </li>
        <li> Pines de entrada analógica: 6 </li>
        <li> Corriente continua por pin de Entrada/Salida: 20 mA </li>
        <li> Velocidad de reloj: 16 MHz </li>
        <li> Memoria flash: 32 KB (de los cuales 0,5 KB son utilizados por el gestor de arranque) </li>
        <li> SRAM: 2 KB </li>
        <li> EEPROM: 1 KB </li>
      </ul>
    </td>
  </tr>
</table>

El Arduino Uno es una placa microcontroladora de código abierto, ideal para principiantes, que se utiliza para construir dispositivos digitales y proyectos interactivos. Permite leer entradas como las de un sensor, un botón o la lectura de temperatura, y convertirlas en salidas, como mover un motor o encender un LED. <b>Este hardware actúa como el sistema nervioso de nuestro coche debido a que este es el componente que recibe todas las decisiones tomadas por el cerebro, la Raspberry, enviando pequeños impulsos eléctricos al driver para indicarle cuándo y de qué manera debe mover los motores. Dado que es nuestra primera vez participando en este tipo de torneos, decidimos empezar probando este modelo de Arduino</b>.

<a href="src"> Ver el código implementado en el Arduino </a>

<hr>

- #### Driver L298N

<table>
  <tr>
    <td align="center" width="300" >
      <img src="./resources/Driver_L298N.png " alt="Driver L298N" >
    </td>
    <td>
      <h3>Especificaciones:</h3>
      <ul>
        <li> Driver IC: STMicroelectronics L298N </li>
        <li> Tensión de alimentación del motor (Vs): 5 V a 35 V </li>
        <li> Corriente de salida máxima: 2 A por canal (4 A máx. total) </li>
        <li> Tensión de alimentación lógica (Vss): 5 V a 7 V </li>
        <li> Disipación de potencia máxima: 20 W a 75 °C </li>
        <li> Nivel de señal de control: Bajo (-0,3 V a 1,5 V), Alto (2,3 V a Vss) </li>
      </ul>
    </td>
  </tr>
</table>

El L298N es un módulo controlador de motor de doble Puente H, que se utilizan para manejar la dirección del flujo de corriente elétrica, permitiendo que nuestro vehículo de desplace izquierda-derecha o de reversa y no solo hacia adelante. Sirve como puente entre el microcontrolador, el Arduino Uno, y los motores de alta potencia (en nuestro caso, el servomotor y el motor del codificador), suministrando la corriente y el voltaje necesarios. <b>Este componente actúa como los músculos del coche, proporcionando el voltaje necesario a los motores, pero dado que el Arduino y la Raspberry Pi manejan un voltaje bajo (insuficiente para alimentar el controlador), es necesaria la implementación de una fuente de alimentación adicional para este componente</b>.

<hr>

- #### Fischertechnik Maker Kit Car

<img src="./resources/Fischertechnik_Maker_Kit_Car.png " alt="Fischertechnik Maker Kit Car" width="300px" >

The Fischertechnik Maker Kit Car is an advanced construction kit designed for makers, hobbyists, and robotic enthusiasts to build a highly customizable, mobile robotic vehicle chassis. Includes pieces for building sturdy structural superstructures and custom mounts, so we took advantage of this by using the blocks as the base or skeleton of our car to later assembly the other components around it.

<h3> Other components the kit contains </h3>

> Servomotor

<a href="schemes/Fistchertechnik Maker Kit Car/BA_DATENBLATT_MAKER_KIT_CAR_ENCODERMOTOR.pdf">Check specifications</a>

Is a specialized motor designed to turn to a specific angle (in this case between 60° and 120°) and hold that position. It connects directly to the front steering knuckles of the chassis and it controls the steering mechanism. Unlike the drive motor, it is not programmed to spin continuously. Instead, it is commanded to change degrees, giving the car precise navigation capabilities.

> Encoder Motor or C Motor

<a href="schemes/Fistchertechnik Maker Kit Car/BA_DATENBLATT_MAKER_KIT_CAR_ENCODERMOTOR.pdf">Check specifications</a>

Is the primary drive engine of the vehicle. It does not just spin; it counts its own rotations. It provides the driving power (traction) to move the car forward and backward. The built-in encoder sends digital pulses back to our controller, the Arduino Uno. This allows us to measure exactly how far the car has traveled, calculate its speed, and program precise movements.

> Differential Gear

Is a mechanical gearbox located between the two driven wheels. It allows the left and right wheels to rotate at different speeds while still receiving power from the motor. When the car turns, the outside wheel has to travel a longer distance than the inside wheel. Without a differential, the wheels would lock up, slip, or skid during turns. This component ensures smooth, realistic cornering and prevents our car from losing traction.

<hr>

- #### Ackermann Mechanism

<img src="./resources/Ackermann_Turning.png " alt="Fischertechnik Maker Kit Car" width="300px" >

When a vehicle takes a turn, the front wheels follow paths with different radii. The inner wheel follows a tighter circle (smaller radius) while the outer wheel describes a wider arc (larger radius). If both wheels point in exactly the same direction (parallel to each other), the inner wheel tends to drag or slip sideways because it is geometrically forced to follow a path that does not correspond to it. This generates: Premature tire wear, Greater steering effort, Loss of stability and grip, Larger turning radius of the vehicle. The Ackermann mechanism solves this problem by making the wheels adopt different angles automatically when the steering wheel is turned.

<hr>

- #### Ackermann principle

The Ackermann principle is based on a geometric condition known as the "Ackermann condition":

In a perfect turn, the axes of all wheels must intersect at a single common point located on the extension of the rear axle. That point is the instantaneous center of rotation of the vehicle.

This implies that:

Inner front wheel → must turn at a larger angle (αᵢ)

Outer front wheel → must turn at a smaller angle (αₑ)

The relationship between both angles is given by the formula:

```text
cot(αₑ) - cot(αᵢ) = d / L
```

Where:

d = distance between the wheel pivot points (track width)

L = distance between axles (wheelbase)

This relationship ensures that, for any steering angle, the center of curvature remains on the line of the rear axle, preventing lateral dragging of the wheels.

<hr>

- #### Ackermann in our project

In our car there is not presence of this mechanism, or it is called a 0% Ackermann, this does not affect a lot the performance since is a small vehicle, but if there was presence of this in the project it would help us improve the times. There are some reasons the kit does not includes it:

1. It is a basic or "entry-level" kit – The Maker Kit Car is designed for the maker market as a base chassis, robust and easy to expand, not as a high-performance scale model.

2. Priority on educational functionality – Its main objective is to serve as a platform for integrating development boards (Arduino, Raspberry Pi) and learning about robotics and programming. A simpler steering system, such as a steering knuckle with a servo motor, is easier to build and program for a beginner user.

3. Product differentiation – fischertechnik reserves the Ackermann mechanism for its more advanced kits focused on competition, such as the STEM Coding Competition, which have a much higher price and complexity. The Maker Kit Car, with its 119 pieces, is a more affordable and versatile option for creative projects.

4. Cost and manufacturing simplicity – A complete Ackermann mechanism requires more parts (angled steering arms, additional track rods, precise geometry) than a simple steering knuckle with a servo, which increases production cost and assembly complexity.

5. Target audience – The kit is aimed at makers and hobbyists who want to experiment with electronics and programming, not necessarily at automotive engineering students who require an exact reproduction of vehicle dynamics.

<hr>

## Power Management

- #### LX-2BUPS UPS

<table>
  <tr>
    <td align="center" width="300" >
      <img src="./resources/LX-2BUPS.png " alt="LX-2BUPS" >
    </td>
    <td>
      <h3>Specifications:</h3>
      <ul>
        <li> Battery Type: Two parallel 18650 lithium-ion batteries (3.7V) </li>
        <li> Output Voltage: Typically available in 5V, 9V, or 12V versions </li>
        <li> Max Output Current: Up to 3A </li>
        <li> Max Output Power: 15W to 24W </li>
        <li> Input Voltage: Standard DC 5V (via Micro USB or USB Type-C depending on the board variant) </li>
      </ul>
    </td>
  </tr>
</table>

The LX-2BUPS is a popular DIY-style universal uninterruptible power supply (UPS) module. It runs on two parallel-connected 18650 lithium-ion batteries and provides seamless, zero-delay switching between mains power and battery backup, making it ideal for keeping low-power devices like internet routers and modems running during outages. We employed two pieces of this component, one of 5V to the Raspberry and another of 12V for the driver.

<hr>

- #### Ultrafire TR 18650 Batteries

<table>
  <tr>
    <td align="center" width="300" >
      <img src="./resources/Ultrafire_TR18650_9800mAh_3.7V.png " alt="Ultrafire TR 18650 9800mAh 3.7V" >
    </td>
    <td>
      <h3>Specifications:</h3>
      <ul>
        <li> Form Factor: Standard 18650 cylindrical cell. </li>
        <li> Diameter: 18 mm. </li>
        <li> Length: 65 mm (can reach up to 68mm if it includes a button-top or an unlisted protection circuit). </li>
        <li> Chemistry: Lithium-ion (Li-ion). </li>
        <li> Terminal Type: Flat top or Button top (varies by distributor). </li>
        <li> Nominal Voltage: 3.7V advertised (Standard Li-ion curve: 4.2V fully charged, ~2.75V cut-off). </li>
        <li> Stated Capacity: 9800 mAh. </li>
      </ul>
    </td>
  </tr>
</table>

In the project we used four of these batteries, two for each UPS. They are rechargeable, we recharge them by plugging in the UPS with a USB-C charger of 20W (admitting 9V / 2.22A).

<hr>

### End of the main section, <a href="src"> click here to see implemented software details </a>.
