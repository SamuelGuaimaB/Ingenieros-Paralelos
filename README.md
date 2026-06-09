# WRO2026 Future Engineers – Ingenieros Paralelos

## Table of Contents

<!-- toc -->

1. [About us](#about-us)
2. [Vision Management](#vision-management)

- [1. About us](#1-about-us)
- [2. Vision Management](#2-vision-management)
  - [2.1 Logitech C922 Web Camera](#21-logitech-c922-web-camera)
  - [2.2 Raspberry Pi 4](#22-raspberry-pi-4)
- [3. Mobility Management ⚙️](#3-mobility-management-⚙️)
  - [3.1 Arduino Uno](#31-arduino-uno)
  - [3.2 L298N Driver](#32-l298N-driver)
  - [3.3 HC-SR04 Ultrasonic Sensors](#33-hc-sr04-ultrasonic-sensors)
  - [3.4 Fischertechnik Maker Kit Car](#34-fischertechnik-maker-kit-car)
- [4. Power Management 🔋](#4-power-management)
  - [4.1 LX-2BUPS UPS](#41-lx-2bups-ups)
  - [4.2 Ultrafire TR 18650 9800mAh 3.7V batteries](#42-ultrafire-tr-18650-9800mah-3.7v-batteries)
- [5. Obstacle Management](#5-obstacle-management)
  - [5.1🔵 Part 1: System Initialization](#51-system-initialization)
  - [5.2 🟢 Part 2: First Challenge – The Open Challenge](#52-first-challenge)
  - [5.3 🔴 Block 3: Second Challenge – Obstacle Challenge](#53-second-challenge)

<!-- tocstop -->


## About us

>Team members
- Samuel Guaimacuto
- Andrés Villareal
- David Xu

_We are a Venezuelan team conformed by Informatic Engineering students of Universidad Gran Mariscal de Ayacucho (UGMA), núcleo Barcelona, being our first time participating in a WRO competition, competing in the Future Engineers category. Our inspiration to be part of this tournament was the desire to learn about robotics' world, wanting to face this challenge in order to achieve it. We are grateful with all our family, professors and classmates, without their support it would not have been possible to achieve what we set out to do._

## Vision Management

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

<table>
  <tr>
    <td align="center" width="300" >
      <img src="./resources/HC-SR04_Ultrasonic_Sensor.png " alt="HC-SR04 Ultrasonic Sensor" >
    </td>
    <td>
      <h3>Specifications:</h3>
      <ul>
        <li> Measuring Range: 2 cm to 400 cm (about 1 inch to 13 feet) </li>
        <li> Accuracy: ±3mm </li>
        <li> Operating Frequency: 40kHz </li>
        <li> Sensing Angle: 15° to 30° cone effect </li>
        <li> Operating Voltage: Typically 5V DC (though some newer variants like the HC-SR04+ support 3.3V) </li>
        <li> Operating Current: ~15mA </li>
      </ul>
    </td>
  </tr>
</table>

The HC-SR04 is a widely used, budget-friendly ultrasonic sensor that measures distance by emitting high-frequency sound waves and calculating the time it takes for the echo to bounce back. It is a staple in robotics for obstacle avoidance and proximity sensing.

- **Fischertechnik Maker Kit Car**

<img src="./resources/Fischertechnik_Maker_Kit_Car.png " alt="Fischertechnik Maker Kit Car" width="300px" >

The Fischertechnik Maker Kit Car is an advanced construction kit designed for makers, hobbyists, and robotic enthusiasts to build a highly customizable, mobile robotic vehicle chassis. Includes pieces for building sturdy structural superstructures and custom mounts, so we took advantage of this by using the blocks as the base or skeleton of our car to later assembly the other components around it.

<h3> Other components the kit contains </h3>

> Servomotor

<a href="schemes/Fistchertechnik Maker Kit Car/BA_DATENBLATT_MAKER_KIT_CAR_ENCODERMOTOR.pdf">Check specifications</a>

Is a specialized motor designed to turn to a specific, exact angle (usually between 0° and 180°) and hold that position. It connects directly to the front steering knuckles of the chassis and it controls the steering mechanism. Unlike the drive motor, it is not programmed to spin continuously. Instead, you command it to change degrees, giving your robot precise navigation capabilities.

> Encoder Motor or C Motor

<a href="schemes/Fistchertechnik Maker Kit Car/BA_DATENBLATT_MAKER_KIT_CAR_ENCODERMOTOR.pdf">Check specifications</a>

Is the primary drive engine of the vehicle. It does not just spin; it counts its own rotations. It provides the driving power (traction) to move the car forward and backward. The built-in encoder sends digital pulses back to our controller, the Arduino Uno. This allows us to measure exactly how far the car has traveled, calculate its speed, and program precise movements.

> Differential Gear

Is a mechanical gearbox located between the two driven wheels. It allows the left and right wheels to rotate at different speeds while still receiving power from the motor. When the car turns, the outside wheel has to travel a longer distance than the inside wheel. Without a differential, the wheels would lock up, slip, or skid during turns. This component ensures smooth, realistic cornering and prevents our car from losing traction.

## Power Management 🔋

- **LX-2BUPS UPS**

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

- **Ultrafire TR 18650 9800mAh 3.7V batteries**

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

In the project we used four of these batteries, two for each UPS.


## Estimated Component Budget

> Estimated prices in USD.  
> Most prices were taken as reference from MercadoLibre Venezuela, since the majority of components were provided by our university.
> The **Fischertechnik Maker Kit Car** price was taken from eBay with an estimated cost of **$115.33**.

| Component | Quantity | Estimated Unit Price | Estimated Subtotal | Reference |
|---|---:|---:|---:|---|
| Raspberry Pi 4 Model B 4GB Kit | 1 | $200.00 | $200.00 | MercadoLibre Venezuela |
| Arduino Uno R3 | 1 | $9.99 | $9.99 | MercadoLibre Venezuela |
| L298N Motor Driver | 1 | $6.99 | $6.99 | MercadoLibre Venezuela |
| HC-SR04 Ultrasonic Sensor | 1 | $2.99 | $2.99 | MercadoLibre Venezuela |
| Logitech C922 Camera | 1 | $70.00 | $70.00 | MercadoLibre Venezuela |
| LX-2BUPS UPS Module / 18650 UPS Module | 1 | $17.80 | $17.80 | MercadoLibre Venezuela |
| 18650 3.7V Battery | 1 | $5.00 | $5.00 | MercadoLibre Venezuela |
| Fischertechnik Maker Kit Car | 1 | $115.33 | $115.33 | eBay |

### Estimated Total

| Concept | Total |
|---|---:|
| Total estimated budget | $428.10 |

> The final budget may vary depending on availability, seller, shipping cost, and product condition.


## Obstacle Management

<h3> 🔵 Part 1: System Initialization </h3>

<br><h3> 1.1 Power-on and serial connection </h3>

<hr>

> [!IMPORTANT]
> On Raspberry Pi:
>- Creates an instance of the WROAutonomousCar class.
>- Attempts to open the serial port (/dev/ttyACM0, /dev/ttyUSB0, or COM3) at 115200 baud.
>- Waits 2 seconds for the Arduino to stabilize.
>- Starts a thread (process_vision) that will capture and process the camera in parallel.
>- The main thread (main_loop) is responsible for sending commands to the Arduino continuously.

<hr>

> [!IMPORTANT]
> On Arduino:
>- Configures the servo on pin 8, initial position at 86° (straight).
>- Configures the DC motor: pins 9 and 10 for direction, pin 7 for PWM.
>- Configures the ultrasonic sensor: pin 3 (Trig) and pin 11 (Echo).
>- Initializes serial communication at 115200 baud.
>- Enters the main loop(), ready to receive commands.

<hr>

<h3> 1.2 Camera configuration and initial parameters </h3>

> [!IMPORTANT]
> Raspberry Pi:
>- Opens the camera at 320×240 pixels (low resolution for higher speed).
>- Defines fixed parameters:
>  1. MITAD_ANCHO_PISTA_PX = 140 pixels (estimated width from one wall to the track center).
>  2. Binarization threshold: 95 (pixels brighter than that are white floor).
>  3. Region of interest: rows 80 to 140 (where the track is expected to be seen).
>  4. PID with kp=0.06, ki=0, kd=0.20.
>- State variables:
>  1. SENTIDO_GIRO = "AUTO" (will be auto-detected at the first curve).
>  2. vueltas_completadas = 0, curvas_superadas = 0, en_curva = False.
>  3. current_speed = 0, current_angle = 86.

<hr>

<h3> 1.3 Bidirectional communication </h3>

<b>Raspberry → Arduino:</b>

- The main thread sends commands in <speed,angle> format every 50 ms.
- Example: <250,86> means speed 250, angle 86 degrees.

<b>Arduino → Raspberry:</b>

- Every 50 ms, the Arduino reads the ultrasonic sensor and sends US:distance.
- The Raspberry does not use this data in this code (although it receives it).

<hr>

<h3> 1.4 Initial car state </h3>

- The car starts stopped (current_speed = 0).
- The steering is centered (current_angle = 86).
- The vision thread is already processing the camera, but has not yet detected the track direction.
- The car waits to find the first curve to auto-determine whether the circuit is clockwise or counterclockwise.

<hr>

<h3> 🟢 Part 2: First Challenge – The Open Challenge </h3>

<p> The Open Challenge focuses strictly on lane-keeping, speed, wall avoidance, and endurance. The main objective is to establish a solid baseline for autonomous navigation before adding complex objects to the track. </p>

<hr>

<h3> 2.1 Main vision flow </h3>

> [!IMPORTANT]
> <b> Step 1: Capture and preprocessing </b>
>- One frame is captured from the camera.
>- It is converted to grayscale.
>- Gaussian blur (7×7) is applied to reduce noise.
>- The region of interest (rows 80 to 140) is extracted.
>- Binarization with threshold 95: bright pixels (floor) → 255, dark pixels (walls) → 0.

<hr>

> [!IMPORTANT]
> <b> Step 2: Raycasting to find walls </b>
>- The center row of the binarized region is taken.
>- It scans from the center (pixel 160) to the left looking for the first black pixel → muro_izq.
>- It scans to the right looking for the first black pixel → muro_der.

<hr>

> [!IMPORTANT]
> <b> Step 3: Auto-detection of track direction (first time only) </b>
>- The first time "MURO_FRONTAL" (a closed corner) is detected:
>  1. It counts white pixels in the left and right halves of the image.
>  2. If there are more white pixels on the right, SENTIDO_GIRO = "DERECHA" (clockwise circuit).
>  3. If there are more white pixels on the left, SENTIDO_GIRO = "IZQUIERDA" (counterclockwise circuit).
>- This happens only once and is used for decisions in subsequent curves.

<hr>

> [!IMPORTANT]
> <b> Step 4: Steering control (PID) </b>
>- error = 160 - centro_pista_x is calculated.
>- Dead zone: If |error| < 15, the angle is fixed at 86° (straight).
>- Otherwise:
>  1. PID is applied: correction = kp * error + kd * (error - prev_error) / dt.
>  2. angulo_pid = 86 + correction.>  3. If there are more white pixels on the left, SENTIDO_GIRO = "IZQUIERDA" (counterclockwise circuit).
>- Limits by state:
>  1. In "CENTRADO" (straight): angle between 76° and 96° (smooth turns).
>  2. In other states: angle between 60° and 120° (more aggressive turns).

<hr>

> [!IMPORTANT]
> <b> Step 5: Speed control</b>
>- In "CENTRADO" with small error → speed 250 (maximum).
>- In "MURO_FRONTAL" → speed 220.
>- In any other case → speed 250.
>- Note: In the first challenge, speed is always high; there is no reduction for obstacles.

<hr>

> [!IMPORTANT]
> <b> Step 6: Curve and corner handling </b>
>- If the state is "MURO_IZQ" or "MURO_DER" (one wall lost):
>  1. The PID has more steering freedom (up to 60° or 120°).
>  2. The car turns toward the side where the wall disappeared.
>- If the state is "MURO_FRONTAL" (closed corner):
>  1. If SENTIDO_GIRO == "DERECHA" → angle 73° (turns right).
>  2. If SENTIDO_GIRO == "IZQUIERDA" → angle 103° (turns left).
>  3. Speed 220.

<hr>

> [!IMPORTANT]
> <b> Step 7: Lap counting </b>
>- Every time "MURO_FRONTAL" is detected and more than 2.5 seconds have passed since the last curve:
>  1. curvas_superadas is incremented.
>  2. en_curva = True is set (prevents counting the same curve multiple times).
>- When curvas_superadas % 4 == 0 (4 corners = 1 lap):
>  1. vueltas_completadas is incremented.
>  2. "VUELTA X/3 COMPLETADA" is printed.
>- When vueltas_completadas >= 3:
>  1. current_speed = 0 is set.
>  2. current_angle = 86.
>  3. running = False, program terminates.

<hr>

> [!IMPORTANT]
> <b> Step 8: Sending to Arduino </b>
>- The main thread sends <speed,angle> every 50 ms.
>- Example during a straight: <250,86>.
>- Example during a right turn: <250,73>.
>- Example at the end: <0,86>.

<hr>

<h3> 2.2 Expected behavior (first challenge) </h3>

1. The car starts centered on the track.
2. On straights, the PID keeps the angle between 76° and 96° (minimal oscillations).
3. When entering a curve, it loses one wall, the PID releases the angle, and the car turns until both walls are visible again.
4. At closed corners, it detects "MURO_FRONTAL" and turns sharply.
5. It completes 3 laps counting 4 corners per lap.
6. It stops by sending <0,86>.


<h3> 🔴 Block 3: Second Challenge – Obstacle Challenge </h3>

The Obstacle Challenge introduces dynamic object detection and real-time path planning. The track geometry remains the same, but it is now populated with randomly placed traffic signs represented by colored pillars. Here the car must avoid the blocks following the WRO rules: Red → pass on the right. Green → pass on the left. (specify more the rules if it is neccessary).

<hr>

> [!IMPORTANT]
> <b> Key differences in Python file: </b>
>- At startup it detects if the car is in parked obstacle mode (dist_F < 40).
>- Evasion logic (inside the main loop):
>  1. If local_scenario == "RIGHT_OBSTACLE" and red is detected, calculate angle to pass on the right.
>  2. If local_scenario == "LEFT_OBSTACLE" and green is detected, calculate angle to pass on the left.
>  3. Speed is reduced to 'L' (low) during evasion.
>- Invisibility mask injection (in the second code WROAutonomousCar): When an obstacle (red/green) is detected, that area is painted white in the binarized image so the wall-following algorithm ignores it.
>- Lap control:
>  1. Also counts 4 corners of the first color detected, but the finish line is magenta.
>  2. It stops after completing 3 laps (configurable).

<hr>

> [!IMPORTANT]
> <b> On Arduino (no significant changes) </b>
>  1. Only receives speed and angle commands.
>  2. Does not distinguish between challenges.

<hr>

<p> This is just a theoretical interpretation of our code, here is <a href="src"> detailed information about our code </a> . </p>
