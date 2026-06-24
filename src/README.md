# Technical Documentation of the Implemented System

## Table of Contents

<!-- toc -->

- [1. General Description](#1-general-description)
- [Preview of the Car Performance](#preview-of-the-car-performance)
- [Components Used and Estimated Budget](#components-used-and-estimated-budget)
- [Vision Management](#vision-management)
  - [Logitech C922 Web Camera](#logitech-c922-web-camera)
  - [Raspberry Pi 4](#raspberry-pi-4)
- [Mobility Management](#mobility-management)
  - [Arduino Uno](#arduino-uno)
  - [L298N Driver](#l298n-driver)
  - [Fischertechnik Maker Kit Car](#fischertechnik-maker-kit-car)
  - [Ackermann Mechanism](#ackermann-mechanism)
- [Power Management](#power-management)
  - [LX-2BUPS UPS](#lx-2bups-ups)
  - [Ultrafire TR 18650 Batteries](#ultrafire-tr-18650-batteries)
- <a href="src"> Obstacle Management </a>

<!-- tocstop -->

---

## 1. General Description

This document presents the implemented navigation system of an autonomous robot designed for the **WRO Future Engineers** competition, based on the following files:

- `src/1st_mode.py` (Adaptive vision-based navigation)
- `src/2nd_mode.py` (Choreography-based manual sequence)
- `src/Ino Code/Arduino_Code.ino`

According to the WRO Future Engineers 2026 rules, the vehicle operates in a self-driving car challenge in which it must drive autonomously on a track whose configuration varies between rounds. The official challenge includes Open Challenge rounds and Obstacle Challenge rounds, both based on autonomous track navigation.

The solution is distributed between a **Raspberry Pi**, responsible for vision processing and decision-making, and an **Arduino**, responsible for executing physical actions on the steering and traction system.

This documentation remains aligned with the code currently available in the repository and describes the implemented logic only.

---

## 2. System Objective

The objective of the system is to allow the robot to:

- Observe the track through a camera.
- Detect walls visually.
- Adapt to a round direction that may be clockwise or counterclockwise.
- Complete the required laps on the track autonomously.
- Determine a navigation state.
- Generate speed and steering-angle commands.
- Execute the commands through the Arduino.

In the implemented system, these tasks are addressed through computer vision, time-based choreography, state-based decision logic, and serial communication between the Raspberry Pi and the Arduino. The Raspberry Pi acts as the host computer executing the Python script depending the challenge, while the Arduino operates as an embedded microcontroller executing the `src/Ino Code/Arduino_Code.ino` script code. **They exchange text or binary data bytes through a synchronized speed setting called the baud rate**.

---

## 3. Robot Architecture

### 3.1 Functional Distribution

| Module       | File                            | Main Function                                                                                            |
| ------------ | ------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Raspberry Pi | `src/1st_mode.py`               | Real-time vision processing, adaptive navigation, automatic lap detection, and reactive steering control |
| Raspberry Pi | `src/2nd_mode.py`               | Choreographed sequence execution, pre-programmed motion commands, and time-based navigation              |
| Arduino      | `src/Ino Code/Arduino_Code.ino` | Command reception, servo control, motor control, and physical execution of motion commands               |
| Camera       | Accessed through OpenCV         | Track image acquisition and real-time frame processing                                                   |

### 3.2 Physical System Flow

```text
Camera -> Raspberry Pi -> Serial -> Arduino -> Servo / Motor

```

### 3.3 Software-to-Hardware Connection

The current software connects with the physical components in the following way:

- **USB Camera -> Raspberry Pi:** `1st_mode.py` opens the camera with `cv2.VideoCapture(0)` and reads live frames for track analysis.
- **Raspberry Pi -> Arduino:** Both Python modes open the serial port `/dev/ttyUSB0` at `115200` baud and send movement packets in `<speed,angle>` format.
- **Arduino-side serial input -> Raspberry Pi:** Both Python modes are prepared to listen for the `BTN:1` serial message used as the start signal.
- **Arduino -> Steering Servo:** The steering angle calculated by the Python software is transmitted through the serial packet and then physically applied by the Arduino to the front steering servo.
- **Arduino -> Drive Motor:** The speed value calculated by the Python software is transmitted through the same serial packet and then physically applied by the Arduino to the traction motor.

---

## 4. Python Implementation

### 4.1 Mode 1 Implementation: `src/1st_mode.py`

#### Imported Libraries

```python
import cv2
import numpy as np
import serial
import time
import threading
```

| Library     | Purpose                                                      |
| ----------- | ------------------------------------------------------------ |
| `cv2`       | Image capture and OpenCV processing                          |
| `numpy`     | Pixel counting and matrix operations                         |
| `serial`    | Communication with the Arduino                               |
| `time`      | Timing control                                               |
| `threading` | Parallel execution of vision and serial button reading       |

#### Main Methods

```python
class WROPrimitivoBlindado:
    def __init__(self): # Constructor method, to asign the respective attributes values
    def read_serial_data(self): # Method responsible of initialize and maintain the Raspberry-Arduino communication
    def process_vision(self): # Method to adapt the camera to the Raspberry (to consume fewer resources)
    def main_loop(self): # Main code
```

#### Main Responsibilities

- open serial communication
- capture the camera image
- detect walls and race direction
- compute speed and angle
- count corners and laps
- send commands to Arduino

#### Configuration Parameters

```python
SERIAL_PORT = "/dev/ttyUSB0"
BAUDRATE = 115200
```

#### Important Values

```python
self.current_angle = 86
self.current_speed = 0
self.SENTIDO_GIRO = "AUTO"
self.VER_PANTALLAS = True
```

> [!IMPORTANT]
> The angle was set to 86 because at 90 the wheels were not completely straight.

### 4.2 Mode 2 Implementation: `src/2nd_mode.py`

#### Imported Libraries

```python
import serial
import time
```

| Library  | Purpose                               |
| -------- | ------------------------------------- |
| `serial` | Communication with the Arduino        |
| `time`   | Timing for choreography execution     |

#### Main Methods

```python
class WROCoreografia:
    def __init__(self):
    def esperar_boton(self):
    def ejecutar_rutina(self):
    def run(self):
```

#### Main Responsibilities

- Open serial communication
- Wait for the start button
- Execute `RUTINA_MANUAL`
- Send `<speed,angle>` packets
- Stop the robot at the end

#### Configuration Parameters

```python
SERIAL_PORT = "/dev/ttyUSB0"
BAUDRATE = 115200
RUTINA_MANUAL = [
    (velocity, angle, duration, "description"),
]
```

#### Servo Handshake Sequence

```python
self.ser.write(b"<0,120>\n") # Turn right the wheels
time.sleep(0.3)
self.ser.write(b"<0,60>\n") # Turn left the wheels
time.sleep(0.3)
self.ser.write(b"<0,86>\n") # Straighten the wheels.
```

### 4.3 Arduino Implementation: `src/Ino Code/Arduino_Code.ino`

#### Imported Libraries

```cpp
#include <Servo.h>
#include <stdlib.h>
```

| Library    | Purpose                         |
| ---------- | ------------------------------- |
| `Servo.h`  | Steering servo control          |
| `stdlib.h` | Parsing numeric values from text |

#### Main Hardware Connections

```cpp
const int pinServo = 8;
const int pinMotorPWM = 7;
const int pinMotorDir1 = 9;
const int pinMotorDir2 = 10;
const int pinTrig = 3;
const int pinEcho = 11;
```

| Pin  | Component         | Function                |
| ---- | ----------------- | ----------------------- |
| `8`  | Steering servo    | Steering angle output   |
| `7`  | Motor driver PWM  | Motor speed control     |
| `9`  | Motor driver IN1  | Motor direction line 1  |
| `10` | Motor driver IN2  | Motor direction line 2  |
| `3`  | Ultrasonic Trig   | Trigger pulse output    |
| `11` | Ultrasonic Echo   | Echo pulse input        |

#### Main Responsibilities

- initialize serial communication at `115200`
- receive `<speed,angle>` packets from the Raspberry Pi
- parse and validate the received values
- apply the angle to the steering servo
- apply the speed to the traction motor
- read the ultrasonic sensor periodically
- send ultrasonic telemetry as `US:<distance>`

#### Main Variables

```cpp
int distanciaUS = 200;
int velocidadAuto = 0;
int anguloServo = 86;
unsigned long previousMillisUS = 0;
```

These variables store:

- the last ultrasonic distance
- the current motor speed
- the current steering angle
- the timing reference for ultrasonic sampling

#### Setup Sequence

In `setup()`, the Arduino:

1. starts serial communication
2. attaches the steering servo
3. centers the servo at `86`
4. configures the motor pins as outputs
5. configures the ultrasonic pins

#### Serial Protocol Received by Arduino

The Arduino expects packets with start and end markers:

```text
<speed,angle>
```

Example:

```text
<250,86>
```

The function `recvWithStartEndMarkers()` reads the packet, and `parseData()` converts the values into:

- `velocidadAuto`
- `anguloServo`

#### Applied Limits

The Arduino constrains the parsed values as follows:

- speed is limited to `0..255`
- angle is accepted only in the range `60..120`

#### Movement Execution

The function `ejecutarMovimiento()`:

- writes `anguloServo` to the steering servo
- drives the motor forward when `velocidadAuto > 0`
- stops the motor when `velocidadAuto == 0`

#### Ultrasonic Telemetry

Every 50 ms, the Arduino executes `leerUltrasonido()` and sends the result through serial:

```text
US:<distance>
```

If no echo is received within the timeout, the stored distance falls back to `200`.

This makes the Arduino file the physical execution layer that turns the Raspberry Pi commands into real steering and motor movement while also publishing distance telemetry.

---

## 5. System Structure by Operating Phase

The current Python implementation can be read in three phases:

1. Serial and hardware initialization
2. Mode 1 autonomous execution
3. Mode 2 choreography execution

### 5.1 Initialization

Both Python modes begin by opening the serial connection with the Arduino:

```python
SERIAL_PORT = "/dev/ttyUSB0"
BAUDRATE = 115200
```

After opening the port, each script waits 2 seconds so the Arduino can stabilize after the serial reset.

In both modes, the physical connection at startup is:

- Raspberry Pi -> serial port -> Arduino
- Arduino-side start signal -> Raspberry Pi

Both modes also use an initial steering handshake before the main action starts:

```text
<0,120>
<0,60>
<0,86>
```

This confirms that the steering servo responds correctly.

### 5.2 Mode 1: Adaptive Vision-Based Navigation (`src/1st_mode.py`)

**Class:** `WROPrimitivoBlindado`

Mode 1 is the autonomous camera-based mode. It uses the USB camera as the main physical input and continuously sends steering and speed commands to the Arduino.

#### How Mode 1 Works

The script starts two parallel tasks:

- `read_serial_data()`: waits for the `BTN:1` start signal from the Arduino side
- `process_vision()`: captures and processes frames from the USB camera

The main loop then sends `<speed,angle>` packets to the Arduino while the robot is in race mode.

#### Vision Processing

1. Capture one frame from the camera with `cv2.VideoCapture(0)`
2. Set the resolution to `320x240`, enough to perform the challenge.
3. Convert the frame to grayscale
4. Apply Gaussian blur with a `5x5` kernel
5. Crop the track band using rows `60:150`, as a interest zone
6. Apply threshold `95` to create a binary image (an image with only black and white colors)
7. Apply morphological opening with a `3x3` kernel
8. Split the processed image into:
   - `horizonte` for far-track analysis
   - `linea_escaneo` for near wall detection

#### Physical Connections Used in Mode 1

- The USB camera provides the visual input
- The Raspberry Pi processes the image and computes the steering and speed values
- The serial cable carries commands from Raspberry Pi to Arduino
- The Arduino applies the received values to the steering servo and drive motor
- The start signal is read in Python as `BTN:1`

#### State Machine

The mode uses three states:

- `ESPERA`: the robot is idle, waiting for the start button
- `CARRERA`: the robot is actively navigating the track
- `RETORNO_A_META`: the robot has completed the required laps and executes the stop sequence

#### Direction Detection

At the beginning of the race, the code compares the white pixels on the left and right halves of the horizon:

- more white on the right -> `DERECHA`
- more white on the left -> `IZQUIERDA`

This establishes the corner direction that will be used for the rest of the run.

#### Front and Side Wall Detection

The code detects the front wall from a central box:

```python
caja_central = binarizada[30:70, 120:200]
```

The corner is considered detected when the dark-pixel ratio is greater than `0.55`.

The side walls are detected by scanning from the image center outward:

- left side -> `muro_izq`
- right side -> `muro_der`

These values are used to estimate the track center.

#### Steering and Speed Logic

When a front wall is detected:

- angle `70` for right corners
- angle `104` for left corners
- speed `180`

When no front wall is detected:

- speed `250`
- center the robot using a proportional correction based on track-center error
- keep angle `86` if the error is inside the `22` pixel dead zone
- clamp straight-line steering between `74` and `98`

#### Lap Counting

The code counts one corner only if the robot is not already flagged as being inside a corner and at least 2 seconds have passed since the previous corner.

Every 4 corners:

- `vueltas_completadas += 1`

After 3 completed laps:

- the state changes to `RETORNO_A_META`
- the robot performs a short stop sequence
- the program ends

#### Key Parameters in Mode 1

| Variable               | Value     | Purpose                             |
| ---------------------- | --------- | ----------------------------------- |
| ROI Rows               | 60-150    | Track-focused image band            |
| Binarization Threshold | 95        | White/black separation              |
| Scan Line Position     | Row 65    | Wall detection line                 |
| Straight Speed         | 250       | High-speed on open track            |
| Curve Speed            | 180       | Safe speed through corners          |
| Right Turn Angle       | 70        | Fixed steering angle right          |
| Left Turn Angle        | 104       | Fixed steering angle left           |
| Straight Angle         | 86        | Neutral steering position           |
| Dead Zone              | 22 px     | Straight stability                  |
| Corner Debounce        | 2 seconds | Prevents multiple corner detections |

### 5.3 Mode 2: Choreography-Based Manual Sequence (`src/2nd_mode.py`)

**Class:** `WROCoreografia`

Mode 2 is the fully timed choreography mode. It does not use the camera for control. Instead, it sends a predefined sequence of commands stored in `RUTINA_MANUAL`.

#### How Mode 2 Works

The sequence is:

1. Open serial communication with Arduino
2. Perform the steering handshake
3. Wait for `BTN:1`
4. Execute each tuple in `RUTINA_MANUAL`
5. Stop the robot with `<0,86>`

#### Physical Connections Used in Mode 2

- The physical start button is received through Arduino as `BTN:1`
- The start signal is received in Python as `BTN:1`
- The Raspberry Pi sends only timed serial commands in this mode
- The serial link carries each `<speed,angle>` packet
- The Arduino applies each command to the steering servo and drive motor

#### Choreography Structure

Each instruction uses this format:

```python
(velocity, angle, duration_seconds, "description")
```

Meaning:

- `velocity`: motor command
- `angle`: steering command
- `duration_seconds`: command duration
- `description`: console label

#### Choreography Phases

The current routine contains:

1. Parking exit
2. First lap
3. Second lap
4. Third lap
5. Parking entry
6. Final motor stop

#### Key Parameters in Mode 2

| Parameter         | Example Values | Purpose                   |
| ----------------- | -------------- | ------------------------- |
| Velocity Range    | -140 to 250    | Motor control values      |
| Right Turn Angle  | 60             | Programmed right steering |
| Center Angle      | 86             | Neutral steering          |
| Left Turn Angle   | 120            | Programmed left steering  |
| Turn Duration     | 1.58-1.8s      | Curve execution time      |
| Straight Duration | 0.6-2.8s       | Straight segments         |

### 5.4 Operating Cycle

#### Mode 1 cycle

1. The camera provides a frame
2. The Raspberry Pi processes the image
3. The track walls are estimated
4. Speed and steering are calculated
5. A `<speed,angle>` packet is sent to Arduino
6. The Arduino drives the servo and motor

#### Mode 2 cycle

1. The Raspberry Pi reads the next tuple from `RUTINA_MANUAL`
2. The command is converted into `<speed,angle>`
3. The packet is sent to Arduino
4. The Arduino drives the servo and motor
5. The Raspberry Pi waits for the configured duration

From the hardware perspective, the software currently reads from:

- USB camera
- start button event through Arduino

And writes to:

- steering servo
- drive motor

---

## 6. Conclusion

The current software documented in this repository is centered on two Python control modes:

- `src/1st_mode.py` for autonomous camera-based navigation
- `src/2nd_mode.py` for manual time-based choreography

Both modes use the same physical communication path from the Raspberry Pi to the Arduino and from there to the steering and traction hardware. One mode reacts to live camera input, while the other follows a predefined timed routine.
