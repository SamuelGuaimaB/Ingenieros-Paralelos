# WRO2026 Future Engineers – Ingenieros Paralelos

## About us 👥

>Team members
- Samuel Guaimacuto
- Andrés Villareal
- David Xu

_We are a Venezuelan team conformed by Informatic Engineering students of Universidad Gran Mariscal de Ayacucho (UGMA), núcleo Barcelona, being our first time participating in a WRO competition, competing in the Future Engineers category. Our inspiration to be part of this tournament was the desire to learn about robotics' world, wanting to face this challenge in order to achieve it. We are grateful with all our family, professors and classmates, without their support it would not have been possible to achieve what we set out to do._

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


## Component Budget

| Component                    | Quantity | Unit Price | Subtotal |
| ---------------------------- | -------: | ---------: | -------: |
| Raspberry Pi 4               |        1 |     $21.42 |   $21.42 |
| L298N Driver                 |        1 |     $22.45 |   $22.45 |
| Arduino Uno                  |        1 |     $19.92 |   $19.92 |
| HC-SR04 Ultrasonic Sensor    |        4 |      $4.05 |   $16.20 |
| Fischertechnik Maker Kit Car |        1 |    $135.00 |  $135.00 |
| Logitech C922 Web Camera     |        1 |      $8.50 |    $8.50 |
| LX-2BUPS UPS                 |        2 |      $8.50 |   $17.00 |
| Ultrafire Lithium Batteries  |        4 |      $9.00 |   $36.00 |

**Estimated total:** $370.49

> Note: Prices are approximate and may vary depending on the supplier, availability, and country of purchase.


# Explanation of `MainCode.py`

This document explains how the `MainCode.py` file works. It runs on the Raspberry Pi and is responsible for the main decision-making of the autonomous car.

The program observes the track with OpenCV, calculates the driving direction, and sends a serial command to the Arduino with the speed and steering angle.

## General file structure

The file has two main components:

- **`PIDController`**: corrects the steering angle.
- **`WROAutonomousCar`**: contains vision, states, obstacle avoidance, lap counting, and serial communication.

Base fragment:

```python
class PIDController:
    def __init__(self, kp, ki, kd, setpoint=160):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.prev_error = 0
        self.integral = 0


class WROAutonomousCar:
    def __init__(self, serial_port='/dev/ttyACM0', baudrate=115200):
        self.ser = serial.Serial(serial_port, baudrate, timeout=0.1)
```

## 1. PID control

The PID takes a target position and a current position. The difference between them produces a correction.

- **P**: corrects proportionally to the current error.
- **I**: accumulates error over time.
- **D**: reacts to the change in error.

In this project, the target value is the horizontal center of the camera frame (`x = 160`), which represents the desired visual position of the track center.

```python
def compute(self, current_value, dt):
    error = self.setpoint - current_value
    self.integral += error * dt
    derivative = (error - self.prev_error) / dt if dt > 0 else 0
    self.prev_error = error
    return (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
```

If the detected center moves away from `setpoint=160`, the PID returns a positive or negative correction to turn the servo.

## 2. Robot initialization

At startup, the program configures:

- the serial port connected to the Arduino,
- the turning direction in `AUTO` mode,
- corner and lap counters,
- the PID controller,
- the initial speed and steering angle.

```python
self.SENTIDO_GIRO = "AUTO"
self.memoria_muro_exterior = "NINGUNO"
self.MITAD_ANCHO_PISTA_PX = 140

self.vueltas_completadas = 0
self.curvas_superadas = 0
self.en_curva = False

self.pid = PIDController(kp=0.06, ki=0.000, kd=0.20)
self.running = True
self.current_speed = 0
self.current_angle = 86
```

## 3. Image capture and preprocessing

First, the camera is opened and the width and height are set. Then, for each frame:

1. it is converted to grayscale,
2. Gaussian blur is applied,
3. a relevant strip is cropped,
4. the image is converted to black and white.

```python
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (7, 7), 0)

y_arriba = 80
y_abajo = 140
roi_blur = blur[y_arriba:y_abajo, 0:320]

_, binarizada = cv2.threshold(
    roi_blur, 95, 255, cv2.THRESH_BINARY)
```

The `roi_blur` variable is essential. The code analyzes the specific part of the track used for fast decision-making instead of processing the entire image.

## 4. Obstacle detection by color

In a second region of interest, the program searches for colors in HSV space:

- **Green**: the car must avoid it on the left side.
- **Red**: the car must avoid it on the right side.

Then it finds contours and keeps the most relevant obstacle by area.

```python
roi_color = frame[80:160, 0:320]
hsv = cv2.cvtColor(roi_color, cv2.COLOR_BGR2HSV)

lower_green = np.array([40, 70, 50])
upper_green = np.array([85, 255, 255])
mask_green = cv2.inRange(hsv, lower_green, upper_green)

lower_red1 = np.array([0, 70, 50])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 70, 50])
upper_red2 = np.array([180, 255, 255])
```

### Invisibility layer

When an obstacle is detected, the program temporarily “erases” it from the binary image so the raycasting logic does not confuse it with a wall.

```python
if obstaculo_tipo != "NINGUNO":
    x_inicio = max(0, x_obs - 20)
    x_fin = min(320, x_obs + w_obs + 20)
    binarizada[:, x_inicio:x_fin] = 255
```

This step separates two different tasks:

- where is the track?
- where is the obstacle?

## 5. Raycasting and wall detection

Here, raycasting consists of taking a horizontal line from the binary image and scanning left and right from the center until the walls are found.

With those two points, the program estimates the center of the track.

```python
alto_roi, ancho_roi = binarizada.shape
linea_escaneo = binarizada[alto_roi // 2, :]

muro_izq = -1
muro_der = -1

for x in range(160, -1, -1):
    if linea_escaneo[x] == 0:
        muro_izq = x
        break

for x in range(160, ancho_roi):
    if linea_escaneo[x] == 0:
        muro_der = x
        break
```

## 6. State machine

Main states:

| State | Meaning | How it is produced |
|---|---|---|
| `CENTRADO` | Both walls are detected. | The center is calculated as the average of the left and right walls. |
| `MURO_IZQ` | Only the left wall is visible. | The center is estimated using the expected half-width of the track. |
| `MURO_DER` | Only the right wall is visible. | The center is estimated by shifting to the left. |
| `CEGUERA_BLANCA` | No wall is detected. | The scan line has no references. |
| `MURO_FRONTAL` | The center is blocked. | The center pixel of the scan line is black. |

```python
if linea_escaneo[160] == 0:
    estado = "MURO_FRONTAL"
else:
    if muro_izq != -1 and muro_der != -1:
        centro_pista_x = (muro_izq + muro_der) // 2
        estado = "CENTRADO"
    elif muro_izq != -1 and muro_der == -1:
        centro_pista_x = muro_izq + self.MITAD_ANCHO_PISTA_PX
        estado = "MURO_IZQ"
    elif muro_izq == -1 and muro_der != -1:
        centro_pista_x = muro_der - self.MITAD_ANCHO_PISTA_PX
        estado = "MURO_DER"
```

## 7. Obstacle avoidance

When the car detects an obstacle and is not in an immediate frontal collision, it forces the track center toward one side:

- **Red**: shifts the center to the right.
- **Green**: shifts the center to the left.

Then it applies an “anti-wall shield” so the avoidance maneuver does not push the car outside the lane.

```python
if obstaculo_tipo == "ROJO":
    centro_pista_x = obstaculo_cx + DISTANCIA_EVASION
    estado = "EVADIENDO_ROJO"

elif obstaculo_tipo == "VERDE":
    centro_pista_x = obstaculo_cx - DISTANCIA_EVASION
    estado = "EVADIENDO_VERDE"

if muro_der != -1:
    centro_pista_x = min(centro_pista_x, muro_der - 45)
if muro_izq != -1:
    centro_pista_x = max(centro_pista_x, muro_izq + 45)
```

## 8. Automatic turning-direction detection

If the robot finds a frontal wall and still does not know whether the track is clockwise or counterclockwise, it compares the white free space on the left and right sides.

```python
if self.SENTIDO_GIRO == "AUTO" and es_vertice_curva:
    blancos_izq = np.sum(binarizada[:, :160] == 255)
    blancos_der = np.sum(binarizada[:, 160:] == 255)

    if blancos_der > blancos_izq:
        self.SENTIDO_GIRO = "DERECHA"
    else:
        self.SENTIDO_GIRO = "IZQUIERDA"
```

That logic is used to decide which side to choose for the blind turn during a frontal collision.

## 9. Corner and lap counting

The algorithm uses the appearance of a strong corner or frontal wall to count corners. To avoid counting the same corner multiple times, it applies a time-based lockout window.

- Every 4 corners = 1 lap.
- After 3 laps, the robot stops.

```python
if es_vertice_curva:
    if not self.en_curva and (current_time - self.ultimo_tiempo_curva > 2.5):
        self.en_curva = True
        self.ultimo_tiempo_curva = current_time
        self.curvas_superadas += 1

        if self.curvas_superadas % 4 == 0:
            self.vueltas_completadas += 1

            if self.vueltas_completadas >= 3:
                self.current_speed = 0
                self.current_angle = 86
                self.running = False
```

## 10. Steering and speed calculation

Main rules:

- If there is `MURO_FRONTAL`, the car turns with a fixed angle.
- If the error is small, it stays straight.
- If it is avoiding an obstacle, it reduces speed.
- On straight sections, the steering range is tighter to reduce zig-zag.
- In curves or when one wall is lost, the steering is allowed more freedom.

```python
if estado == "MURO_FRONTAL":
    if self.SENTIDO_GIRO == "DERECHA":
        self.current_angle = 73
    else:
        self.current_angle = 103
    self.current_speed = 220

else:
    error_absoluto_real = 160 - centro_pista_x

    if abs(error_absoluto_real) < 150:
        self.current_angle = 86
        self.pid.integral = 0
    else:
        correccion_pid = self.pid.compute(centro_pista_x, dt)
        angulo_pid = int(86 + correccion_pid)
```

This dead-zone condition defines when the car keeps the steering centered before applying PID correction.

## 11. Serial communication with Arduino

The main thread does not process vision. It takes the latest calculated command and packs it into a string:

```text
<speed,angle>
```

That packet is read by the Arduino to move the motor and servo.

```python
while self.running:
    paquete = f"<{self.current_speed},{self.current_angle}>\n"
    self.ser.write(paquete.encode('utf-8'))
    time.sleep(0.05)
```

Example:

- `<250,86>` means high speed with centered steering.

## 12. Visual summary of the complete flow

| Step | Action | Result |
|---|---|---|
| 1 | Frame capture | Current image of the track |
| 2 | Preprocessing | Binary image that is easier to analyze |
| 3 | Color detection | Position of red and green posts |
| 4 | Raycasting | Left and right walls |
| 5 | State machine | Decision about the current track context |
| 6 | PID + rules | Desired angle and speed |
| 7 | Serial | Command sent to the Arduino |

## Conclusion

`MainCode.py` works as the high-level brain of the car. The Raspberry Pi interprets the track and generates the decision, and the Arduino executes the received movement.

The most important part of the design is that it combines three layers:

- computer vision,
- state logic to understand the track,
- PID control to smooth steering.

The file integrates perception, decision-making, and control in the same driving loop.


###########################################################
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

> [!IMPORTANT]
> <b> Main logic (Python file – Main Loop) </b>
>- Image capture and reduction to 160x120.
>- Color detection (in LAB space):
>  1. MAGENTA = finish line.
>  2. ORANGE and BLUE = corner start points (to detect clockwise/counterclockwise direction).
>  3. //RED and GREEN = pillars (in the first challenge they shouldn't exist, they are ignored or used as visual references).
>- //AI classification (MediaPipe) asynchronously: Returns Straight, Near-Curve, etc.
>- Steering control in Straight:
>  1. Uses calculate_pd_steering_angle(dist_L, dist_R) (PD control with lateral ultrasonics).
>  2. If no functional ultrasonics, the code has a vision fallback.
>- //Steering control in Near-Curve:
>  1. Reduces speed (M).
>  2. Uses red/green pillar detection to calculate the turn.
>  3. If no pillar is detected, it turns fixed according to the track direction.
>- Lap detection:
>  1. Counts 4 corners (orange or blue) to add 1 lap.
>  2. When reaching 4 laps, sends stop command (A090PS or A090S).

<hr>

> [!IMPORTANT]
> <b> On Arduino (responds to commands) </b>
>  1. Receives <speed,angle>.
>  2. Speeds: speedAuto (0..255) – although in the Python file letters are used (H, M, L, S, P), in the final version it's converted to a number.
>  3. The servo moves to angleServo (60..120°).
>  4. The motor moves forward with PWM.

<hr>

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
