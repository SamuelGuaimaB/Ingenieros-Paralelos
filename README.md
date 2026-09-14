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
- [Componentes usados y precio estimado](#componentes-usados-y-precio-estimado)
- [Manejo de la visión](#manejo-de-la-visión)
  - [Cámara Web Logitech C922](#cámara-web-logitech-c922)
  - [Raspberry Pi 4](#raspberry-pi-4)
- [Manejo de la movilidad](#manejo-de-la-movilidad)
  - [Arduino Uno](#arduino-uno)
  - [Driver L298N](#driver-l298n)
  - [Fischertechnik Maker Kit Car](#fischertechnik-maker-kit-car)
  - [Mecanismo Ackermann](#mecanismo-ackermann)
  - [Principio Ackermann](#principio-ackermann)
  - [Ackermann en nuestro proyecto](#ackermann-en-nuestro-proyecto)
- [Manejo de las Fuentes de Energia](#manejo-de-las-fuentes-de-energia)
  - [UPS LX-2BUPS](#ups-lx-2bups)
  - [Baterías Ultrafire TR 18650](#baterías-ultrafire-tr-18650)
- [Conexión entre el software de los componentes](#conexión-entre-el-software-de-los-componentes)
  - [Modo 1 Navegación por cámara](#modo-1-navegación-por-cámara)
  - [Modo 2 Secuencia Temporizada](#modo-2-secuencia-temporizada)
  - [Arduino Control de motores](#arduino-control-de-motores)
  - [Calibración de Visión](#calibración-de-visión)
  - [Servicio de arranque y versiones anteriores](#servicio-de-arranque-y-versiones-anteriores)
- [Puntos a mejorar en nuestro proyecto](#puntos-a-mejorar-en-nuestro-proyecto)
- [Nuestras experiencias en las regionales](#nuestras-experiencias-en-las-regionales)

<!-- tocstop -->

<hr>

## Vista previa del carro

<table>
  <tr>
    <td align="center"><b>Superior</b><br><img src="v-photos/vistaSuperior.jpeg" width="300"></td>
    <td align="center"><b>Frontal</b><br><img src="v-photos/vistaDelantera.jpeg" width="300"></td>
    <td align="center"><b>Izquierda</b><br><img src="v-photos/vistaIzquierda.jpeg" width="300"></td>
  </tr>
  <tr>
    <td align="center"><b>Inferior</b><br><img src="v-photos/vistaInferior.jpeg" width="300"></td>
    <td align="center"><b>Trasera</b><br><img src="v-photos/vistaTrasera.jpeg" width="300"></td>
    <td align="center"><b>Derecha</b><br><img src="v-photos/vistaDerecha.jpeg" width="300"></td>
  </tr>
</table>

<hr>

## Componentes usados y precio estimado

| Componente | Cantidad | Precio Estimado por Unidad | Subtotal Estimado | Referencia |
|---|---:|---:|---:|---|
| Raspberry Pi 4 Modelo B 4GB Kit | 1 | $200.00 | $200.00 | MercadoLibre Venezuela |
| Arduino Uno R3 | 1 | $9.99 | $9.99 | MercadoLibre Venezuela |
| Driver de Motor L298N | 1 | $6.99 | $6.99 | MercadoLibre Venezuela |
| Cámara Logitech C922 | 1 | $70.00 | $70.00 | MercadoLibre Venezuela |
| Módulo UPS LX-2BUPS | 2 | $17.80 | $35.60 | MercadoLibre Venezuela |
| Batería 18650 3.7V | 4 | $5.00 | $20.00 | MercadoLibre Venezuela |
| Fischertechnik Maker Kit Car | 1 | $115.33 | $115.33 | eBay |

### Total Estimado: $457.88

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

> [!NOTE]
>- La cámara fue calibrada en el script del modo 1 (en el modo 2 no se le da uso a la cámara) basándose en los valores de los colores obtenidos en el script de calibración.

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

<a href="https://www.youtube.com/watch?v=o2TZHPnM0VQ"> Tutorial para configurar una Raspberry Pi 4 </a> (Si el link no funciona se puede buscar otro tutorial)

> [!NOTE]
>- En las imágenes de nuestro carro se puede apreciar que nuestra Raspberry se encuentra en una carcasa con un mini ventilador.
>- La universidad nos brindó este componente en este estado y tampoco se pudo verificar el origen de esta envoltura.

Se nos hizo más cómodo trabajar desde la terminal de la Raspberry ya que se hacía más lento moverse dentro de la interfaz. Dentro de los comandos que usamos se encuentran los siguientes:

- `sudo find / -name "nombre_del_archivo"`: para buscar dónde se encuentra un archivo.
- `cd nombre_directorio`: para moverse a una carpeta específica.
- `cat archivo`: para ver el contenido de un archivo.
- `nano archivo`: para editar archivo desde la terminal.
- `sudo systemctl start robot.service`: para inciar la ejecución del programa.
- `sudo systemctl stop robot.service`: para parar la ejecución del programa.

> [!IMPORTANT]
>- El archivo robot.service se encuentra en la carpeta src de nuestro repositorio, en ese archivo se puede editar el archivo de Python que se va a ejecutar al presionar el botón, el cual definimos en base al modo que nos estemos enfrentando.

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

> [!NOTE]
>- Nosotros tuvimos que usar una extensión del navegador Google Chrome para poder acceder a la página "arduino.cc" para descargar el software para configurar las instrucciones a ejecutar en el Arduino Uno debido a que no se puede acceder de manera local, este se llama "CyberGhost VPN - Proxy For Chrome". 

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

El Fischertechnik Maker Kit Car es un kit de construcción avanzado diseñado para aficionados de la robótica, que da la libertad de construir un chasis de vehículo robótico móvil personalizable. Incluye piezas para construir estructuras robustas y soportes personalizados, por lo que aprovechamos esto utilizando los bloques del kit como base o esqueleto de nuestro coche para luego ensamblar el resto de los componentes alrededor de ellos.

<h3> Otros componentes que el kit contiene </h3>

> Servomotor

Se trata de un motor especializado diseñado para girar a un ángulo específico, en este caso entre 60° y 120° y mantener dicha posición. Se conecta directamente a las manguetas delanteras de nuestro chasis, y estas a ambas ruedas delanteras, controlando también el mecanismo de dirección. A diferencia del motor de tracción, no está diseñado para girar de manera contínua, en cambio este gira cuando se le ordena cambiar de ángulo, proporcionando al vehículo la capacidad de cambiar de dirección (izquierda-derecha).

<table>
  <tr>
    <td align="center">
      <img src="./resources/servo1.jpeg" alt="Especificaciones del Servo 1" >
    </td>
    <td>
      <img src="./resources/servo2.jpeg" alt="Especificaciones del Servo 2" >
    </td>
  </tr>
</table>

> Motor Codificador o Motor C

Es el motor principal del vehículo. Proporciona la potencia motriz (tracción) para que el coche avance y retroceda. Este motor alimenta las llantas traseras de nuestro vehículo, significando que estas son las que poseen tracción.

<table>
  <tr>
    <td align="center">
      <img src="./resources/encoder1.jpeg" alt="Especificaciones del Motor Codificador 1" >
    </td>
    <td>
      <img src="./resources/encoder2.jpeg" alt="Especificaciones del Motor Codificador 2" >
    </td>
    <td>
      <img src="./resources/torqueEncoder.jpeg" alt="Torque del Motor Codificador" >
    </td>
  </tr>
</table>

> Engranaje Diferencial

Consiste en una caja de cambios mecánica ubicada entre las dos ruedas motrices, en nuestro caso las ruedas traseras. Permite que las ruedas izquierda y derecha giren a velocidades diferentes mientras reciben potencia del motor. Al girar el coche, la rueda exterior recorre una mayor distancia que la interior. Sin un diferencial, las ruedas se bloquearían, patinarían o derraparían durante las curvas. Este componente garantiza un paso por curva suave y realista, y evita que el coche pierda tracción.

> [!NOTE]
>- Al ser nuestra primera vez participando en una competición WRO, usamos los componentes predeterminados del kit.
>- La tracción trasera se conservó debido a que la mayoría de los carros cotidianos la presentan.
>- En cuanto al engranaje diferencial se pudo observar que ayudó a forzar menos las curvas.

<hr>

- #### Mecanismo Ackermann

<img src="./resources/Ackermann_Turning.png " alt="Imagen del mecanismo Ackermann" width="300px" >

Cuando un carro gira, las ruedas delanteras siguen trayectorias con radios diferentes. La rueda interior describe un círculo más cerrado (radio menor), mientras que la exterior describe un arco más amplio (radio mayor). Si ambas ruedas apuntan exactamente en la misma dirección (paralelas entre sí), la rueda interior tiende a arrastrarse o deslizarse lateralmente, ya que se ve forzada a seguir una trayectoria que no le corresponde. Esto genera desgaste prematuro de los neumáticos, mayor esfuerzo de dirección, pérdida de estabilidad y agarre, y mayor radio de giro del vehículo. El mecanismo de Ackermann resuelve este inconveniente haciendo que las ruedas adopten ángulos diferentes automáticamente en el momento cuando las ruedas direccionales giran hacia la izquierda o derecha.

<hr>

- #### Principio Ackermann

El principio de Ackermann se basa en una condición geométrica conocida como la condición de Ackermann. En un giro perfecto, los ejes de todas las ruedas deben intersectarse en un único punto común situado en la prolongación del eje trasero. Este punto es el centro instantáneo de rotación del vehículo. Esto implica que la rueda delantera interior debe girar con un ángulo mayor (αᵢ), mientras que la rueda delantera exterior debe girar con un ángulo menor (αₑ).

La relación entre ambos ángulos viene dada por la fórmula:

```text
cot(αₑ) - cot(αᵢ) = d / L
```

Donde:

d = distancia entre los puntos de pivote de las ruedas (ancho de vía)

L = distancia entre ejes (distancia entre ejes)

Esta relación garantiza que, para cualquier ángulo de giro, el centro de curvatura permanezca sobre la línea del eje trasero, evitando el arrastre lateral de las ruedas.

<hr>

- #### Ackermann en nuestro proyecto

<img src="resources/nuestro_ackermann.jpg" alt="Imagen de nuestro mecanismo Ackermann" width="300px" >

Nuestro coche no cuenta con la presencia de este mecanismo, o también puede ser denominado 0% Ackermann. Esto no afecta mucho al rendimiento, ya que se trata de un vehículo pequeño, pero si lo incluyéramos en el proyecto, nos ayudaría a mejorar los tiempos, por otra parte también se podrían evitar problemas con el desgaste de las llantas. En base a lo investigado, son varias las razones por las que el kit no trae este mecanismo incluido:

1. Es un kit básico de iniciación, pues el Maker Kit Car está diseñado con el propósito de cumplir la función de un chasis base, robusto y fácil de ampliar, no como un modelo a escala de alto rendimiento.

2. Prioridad de funcionalidad educativa: su objetivo principal es servir como plataforma para integrar placas de desarrollo, como Arduino y Raspberry Pi, y aprender sobre robótica y programación, por el hecho de que un sistema de dirección más sencillo, como una mangueta con un servomotor, es más fácil de construir y programar para un individuo no muy conocedor acerca del área.

3. Diferenciación del producto: Fischertechnik reserva el mecanismo Ackermann para sus kits más avanzados, orientados a la competición, como el STEM Coding Competition, que tienen un precio y una complejidad mucho mayores. El Maker Kit Car, con sus 119 piezas, es una opción más accesible y rentable para proyectos creativos.

4. Costo y simplicidad de fabricación: Un mecanismo Ackermann completo requiere más piezas (brazos de dirección angulados, barras de acoplamiento adicionales, geometría precisa) que una simple mangueta con servomotor, lo que aumenta el costo de producción y la complejidad del montaje.

5. Público objetivo: El kit está dirigido a aficionados y creadores que desean experimentar con la electrónica y la programación, no necesariamente a estudiantes de ingeniería que busquen una reproducción exacta de la dinámica de un vehículo.

<hr>

## Manejo de las Fuentes de Energia

- #### UPS LX-2BUPS

<table>
  <tr>
    <td align="center" width="300" >
      <img src="./resources/LX-2BUPS.png " alt="LX-2BUPS" >
    </td>
    <td>
      <h3>Especificaciones:</h3>
      <ul>
        <li> Tipo de batería: Dos baterías de iones de litio 18650 en paralelo (3,7V) </li>
        <li> Voltaje de salida: Generalmente disponible en versiones de 5V, 9V o 12V </li>
        <li> Corriente máxima de salida: 3A </li>
        <li> Potencia máxima de salida: De 15W a 24W </li>
        <li> Voltaje de entrada: CC estándar de 5 V (a través de Micro USB o USB Tipo-C, según la variante de la placa) </li>
      </ul>
    </td>
  </tr>
</table>

El LX-2BUPS es un popular módulo de alimentación ininterrumpida. Funciona con dos baterías de iones de litio 18650 conectadas en paralelo y proporciona un intercambio instantáneo y sin retardo entre la alimentación de red y la batería de respaldo, lo que lo hace ideal para mantener en funcionamiento dispositivos de bajo consumo en el hogar como routers y módems de internet durante cortes de luz. Utilizamos dos piezas de este componente, uno de 5 V para la Raspberry Pi y otro de 12 V para el driver.

<hr>

- #### Baterías Ultrafire TR 18650

<table>
  <tr>
    <td align="center" width="300" >
      <img src="./resources/Ultrafire_TR18650_9800mAh_3.7V.png " alt="Ultrafire TR 18650 9800mAh 3.7V" >
    </td>
    <td>
      <h3>Especificaciones:</h3>
      <ul>
        <li> Factor de forma: Celda cilíndrica estándar 18650. </li>
        <li> Diámetro: 18 mm. </li>
        <li> Longitud: 65 mm (puede alcanzar hasta 68 mm si incluye un polo positivo tipo botón o un circuito de protección no especificado). </li>
        <li> Química: Iones de litio (Li-ion). </li>
        <li> Tipo de terminal: Polo positivo plano o tipo botón (varía según el distribuidor). </li>
        <li> Voltaje nominal: 3,7 V (Curva estándar de iones de litio: 4,2 V con carga completa, ~2,75 V de corte). </li>
        <li> Capacidad declarada: 9800 mAh. </li>
      </ul>
    </td>
  </tr>
</table>

En el proyecto utilizamos cuatro de estas baterías, dos para cada UPS. Son baterías recargables, las recargamos conectándolas al UPS con un cargador USB-C de 20 W (que admite 9 V / 2,22 A).

<hr>

## Conexión entre el software de los componentes

La **Raspberry Pi** ejecuta uno de los modos de conducción y envía instrucciones por el puerto `/dev/ttyUSB0` a `115200` baudios. El **Arduino** recibe el par `<velocidad,ángulo>` y actúa sobre el motor y el servo. Al pulsar el botón físico, el Arduino envía `BTN:1`; cada modo espera esa señal antes de iniciar el movimiento. El calibrador funciona aparte y ayuda a escoger parámetros de visión.

| Archivo | Responsabilidad | Entrada principal | Salida principal |
| --- | --- | --- | --- |
| [`1er_modo.py`](https://github.com/SamuelGuaimaB/Ingenieros-Paralelos/blob/main/src/1er_modo.py) | Conducir según la cámara | Fotogramas y `BTN:1` | Órdenes de motor y dirección |
| [`2do_modo.py`](https://github.com/SamuelGuaimaB/Ingenieros-Paralelos/blob/main/src/2do_modo.py) | Ejecutar una secuencia de movimientos cronometrados | `RUTINA_MANUAL` y `BTN:1` | Órdenes de motor y dirección |
| [`Ino Code/Arduino_code.ino`](https://github.com/SamuelGuaimaB/Ingenieros-Paralelos/blob/main/src/Ino%20Code/Arduino_code.ino) | Accionar el hardware y leer el botón | Órdenes serie y pulsador | Movimiento físico y `BTN:1` |
| [`calibracion.py`](https://github.com/SamuelGuaimaB/Ingenieros-Paralelos/blob/main/src/calibracion.py) | Inspeccionar máscaras de piso y color | Cámara y barras de ajuste | Ventanas de vista previa y valores por consola |
| [`robot.service`](https://github.com/SamuelGuaimaB/Ingenieros-Paralelos/blob/main/src/robot.service) | Configurar el arranque mediante `systemd` | Inicio del sistema | Ejecutar un script local |

**Protocolo serie.** El comando de ejemplo `<250,86>` pide velocidad positiva `250` y dirección `86°` (centro). Un valor negativo invierte el motor; `0` lo detiene. Arduino acepta el carácter inicial `<` y lee dos números con `Serial.parseInt()`, pero **no verifica expresamente** la coma ni `>`. El botón se comunica en sentido inverso mediante la línea `BTN:1`.

<hr>

## Modo 1 Navegación por Cámara

**Archivo:** `src/1er_modo.py` · **Clase:** `WROPrimitivoBlindado`

<img src="resources/diagrama-modo-1.png" alt="Diagrama de Flujo del Modo 1">

El modo 1 toma decisiones a partir de cada imagen. Su bucle de visión calcula las órdenes, mientras el bucle principal las transmite a Arduino durante la carrera. Dos hilos auxiliares permiten analizar la cámara y recibir el botón sin detener la transmisión de comandos.

### Bloques del programa

1. **Inicialización (`__init__`).** Intenta abrir el serial, espera el reinicio del Arduino y prepara el estado `ESPERA`, la velocidad `0`, el centro `86°`, el sentido `AUTO` y los rangos HSV de naranja y azul. Si no hay Arduino, mantiene la visión activa, pero no puede mover el robot.
2. **Botón (`read_serial_data`).** Lee el puerto en un hilo. Una línea `BTN:1` marca el inicio solicitado; `main_loop()` cambia entonces a `CARRERA`.
3. **Máscara de pista (`process_vision`).** Captura a `320 × 240`, convierte a grises, aplica desenfoque, recorta `blur[30:140, :]`, umbraliza con `88` y elimina puntos mediante apertura morfológica. La caja central mide la proporción de píxeles oscuros; una fila de la máscara busca paredes a izquierda y derecha.
4. **Sentido de giro.** Si está en `CARRERA` y aún no se eligió sentido, examina un ROI en HSV. Más píxeles naranja que azul fijan `DERECHA`; de lo contrario, cuando se supera el umbral de color, fija `IZQUIERDA`. Una vez elegido, no vuelve a calcular el color.
5. **Decisión de conducción.** Con muro frontal detectado (`ratio_oscuro > 0.55`), usa velocidad `180` y dirección `65°` a la derecha o `109°` a la izquierda. Sin muro frontal, usa velocidad `250`, estima el centro de la pista con los muros laterales y corrige suavemente el ángulo alrededor de `86°`, limitado a `74°–98°`.
6. **Conteo y fin.** `en_curva` y el tiempo desde la última curva evitan varios conteos de una misma esquina. Al alcanzar `12` curvas, el estado cambia a `RETORNO_A_META`: el programa realiza una secuencia temporizada de avance, contrafreno y parada, y cierra el serial.

### Estados y condiciones

| Estado o marca | Qué significa |
| --- | --- |
| `ESPERA` | Aún no se recibió el botón; el bucle principal no transmite órdenes de carrera. |
| `CARRERA` | Transmite `<velocidad,ángulo>` aproximadamente cada `0,04 s`; visión actualiza esos valores. |
| `RETORNO_A_META` | Ejecuta la maniobra final y termina. |
| `en_curva` | Bloquea temporalmente el conteo de una esquina repetida; **no** es un estado de `estado_general`. |
| `SENTIDO_GIRO` | `AUTO`, `DERECHA` o `IZQUIERDA`; determina hacia dónde se gira. |

Al inicio de `CARRERA`, la detección de muro frontal se desactiva durante `1,5 s`. Una curva nueva se cuenta si `en_curva` está desactivado y han pasado más de `3,2 s` desde la anterior. La marca se libera cuando han pasado más de `4,2 s` sin muro frontal. Cada cuatro curvas el código imprime un aviso; la variable `vueltas_completadas` existe, pero no se incrementa.

**Ajustes relevantes:** umbral de pista `88`; caja central y umbral de muro `0.55`; umbral de color `120` píxeles; centro de servo `86°`; velocidades `180/250`. Están escritos dentro de `process_vision()`, salvo los rangos HSV inicializados en `__init__`. `VER_PANTALLAS = True` abre una ventana de OpenCV; en una Raspberry sin pantalla gráfica se debe revisar esa opción antes de ejecutarlo.

<hr>

## Modo 2 Secuencia Temporizada

**Archivo:** `src/2do_modo.py` · **Clase:** `WROCoreografia`

<img src="resources/diagrama-modo-2.png" alt="Diagrama de Flujo del Modo 2">

Este modo sigue una coreografía fija. Cada elemento activo de `RUTINA_MANUAL` tiene la forma `(velocidad, ángulo, duración_en_segundos, descripción)`. Por ejemplo, `(-140, 86, 0.2, "Retroceso estacionamiento")` manda marcha atrás durante `0,2 s` con las ruedas centradas. Las líneas comentadas en la lista no se ejecutan.

| Bloque | Qué hace |
| --- | --- |
| `__init__()` | Intenta conectar al Arduino y espera `2 s` para su reinicio. |
| `run()` | Comprueba el servo con el barrido `120° → 60° → 86°`, espera el botón y lanza la secuencia. |
| `esperar_boton()` | Envía `<0,86>` y consulta el serial hasta recibir `BTN:1`. |
| `ejecutar_rutina()` | Recorre las tuplas en orden, envía cada instrucción y espera su duración; al final envía `<0,86>` y cierra el serial. |

La velocidad positiva implica avance, la negativa reversa y `0` una pausa del motor; el ángulo determina la orientación del servo. Estas son **fases descriptivas**, no estados formales del programa. Como no usa la cámara ni otro sensor para corregir posición, la trayectoria depende del tiempo programado y del comportamiento físico real. Si el serial no se abre, `esperar_boton()` permanece esperando porque no puede recibir `BTN:1`.

**Para ajustar el recorrido**, se modifica `RUTINA_MANUAL`, especialmente las duraciones y los ángulos de cada paso activo. El programa no mide la distancia realmente recorrida.

<hr>

## Arduino Control de Motores

**Archivo:** `src/Ino Code/Arduino_code.ino`

<img src="resources/diagrama-arduino.png" alt="Diagrama de Flujo del Arduino">

- **`setup()`** abre el serial, configura los pines, centra el servo en `86°` y apaga el motor. Los pines definidos son servo `6`, PWM del motor `3`, dirección `5` y `4`, y botón `2` con resistencia interna `INPUT_PULLUP`.
- **`loop()`** confirma la pulsación después de `50 ms` y envía `BTN:1` una sola vez mediante `botonEnviado`. También escucha el serial: al ver `<`, lee velocidad y ángulo, mueve el motor y limita el servo al intervalo `50°–122°`.
- **`moverMotor()`** limita la velocidad a `-255…255`. Cambia el sentido con los dos pines de dirección y aplica el valor absoluto del PWM en reversa.
- **`detenerMotores()`** baja ambos pines de dirección y escribe PWM `0`.

El Arduino convierte los comandos en acciones, pero no informa de vuelta la velocidad ni el ángulo alcanzados. El botón se informa una vez por arranque del microcontrolador, no una vez por cada ejecución de `RUTINA_MANUAL`.

<hr>

## Calibración de Visión

**Archivo:** `src/calibracion.py`

<img src="resources/diagrama-calibrador.png" alt="Diagrama de Flujo del Calibrador">

El script abre la cámara a `320 × 240` y muestra tres ventanas: región de interés, máscara y resultado. Sus barras permiten escoger **modo 0: piso**, **modo 1: naranja** o **modo 2: azul**, además del umbral o los límites HSV correspondientes.

Para piso toma el ROI `frame[40:180, 0:320]`, aplica escala de grises, suavizado y umbral binario. Para naranja o azul convierte ese ROI a HSV, construye una máscara con los límites seleccionados y quita puntos pequeños mediante apertura morfológica. La tecla `p` imprime los valores mostrados; `q` sale, libera la cámara y cierra las ventanas. **El calibrador no guarda parámetros en archivos ni actualiza automáticamente `1er_modo.py`:** los valores útiles deben trasladarse manualmente. Su ROI y umbral predeterminados tampoco son idénticos a los del modo 1, por lo que conviene contrastarlos antes de copiarlos.

<hr>

## Servicio de arranque y versiones anteriores

`robot.service` declara un servicio de `systemd` que trabaja como `root` desde `/root/Desktop` y ejecuta **`/root/Desktop/2do.py`**, con reinicio si falla. Ese destino no corresponde a `src/2do_modo.py`; para utilizarlo tal como está, el archivo indicado tendría que existir en la Raspberry. Esta descripción documenta la configuración incluida en el repositorio, no confirma que el servicio esté instalado o habilitado en el robot.

En la carpeta `src/Viejos Codigos usados/` se conservan códigos implementados en competiciones anteriores, ayudando a comprender la evolución del proyecto.

<hr>

## Puntos a mejorar en nuestro proyecto

Después de esta primera experiencia en una competición WRO y a lo largo de nuestro camino de preparación para estos torneos, nos pudimos dar cuenta de puntos muy clave que se pueden optimizar del carro desarrollado:

1. Chasis del carro: El chasis de nuestro carro nos trajo una serie de dificultades como la limitación del espacio para ubicar los componentes necesarios, desgaste en los dientes del eje diferencial, en las llantas, entre otros aspectos. Para una futura competición, nos gustaría personalizar más nuestro chasis, diseñando e imprimiendo las piezas en 3D que creamos que sean necesarias para el ensamblaje del vehículo. Nos parece de agrado esta idea debido a que consideramos que planificando el diseño y el uso de cada parte del chasis nos evitaríamos una cantidad considerable de inconvenientes que se nos presentaron en esta jornada.

2. Motor codificador más eficiente: Implementando un motor capaz de girar a mayores revoluciones por minuto para alimentar las ruedas con tracción, conseguiríamos mejorar los tiempos para los desafíos, pues el motor codificador usado en esta temporada nos limitó el logro de mejores tiempos. Consideramos que empleando un motor de este tipo pero que acepte mayor voltaje podría solucionar dicho problema.

3. Posible implementación de un Mecanismo Ackermann: En caso de usar un motor codificador capaz de entregarle una mayor cantidad de revoluciones por minuto a las ruedas de nuestro carro, probablemente diseñemos este mecanismo en 3D como parte de nuestro chasis personalizado, esto con el fin de evitar tanto desgaste en las llantas y hacer más estable el vehículo, de tal manera que no resbale o patine, pudiendo influir en su rendimiento sobre la pista.

4. Posición de la cámara: Después de esta primera experiencia en estas competiciones, también en base a lo aprendido analizando el rendimiento de otros equipos, se llegó a la conclusión que una cámara ubicada a mayor altura puede tener la capacidad de un mayor rango de visión del entorno, punto que puede ser aprovechado como una ventaja para el software implementado.

<hr>

## Nuestras experiencias en las regionales

1. Primera Regional (Hotel Maremares - Anzoátegui, Lechería)

Tras observar fallas en la competencia y experimentar las dinámicas de primera mano, se decidió implementar correcciones y modularizar el código para lograr una estrategia más confiable y segura. Uno de los problemas iniciales identificados fue un "punto ciego" al arrancar demasiado cerca de la pared frontal. Debido a que el robot estaba posicionado muy cerca de la pared interior, su campo de visión y la lógica utilizada para determinar la dirección causaban que eligiera consistentemente el camino equivocado, específicamente el opuesto al correcto. Para corregir esto, primero se dividió el código original en dos archivos separados, separando el Modo 1 del Modo 2, lo que resultó en un mejor rendimiento y un flujo de trabajo más manejable. Para solucionar los errores identificados en el Modo 1, se reestructuró el diseño para minimizar la complejidad, simplificando el código lo más posible y asegurando al mismo tiempo la confiabilidad. Se eliminó el controlador PID y sus componentes asociados en favor de una metodología de control Bang-Bang (o encendido/apagado). Esta había demostrado ser más efectiva para nuestro robot durante la competencia; este enfoque nos permitió completar el primer desafío de manera más consistente y con una configuración más fácil de ajustar. Para el Modo 2, se implementó navegación por estima (Dead Reckoning), la cual ofrece una consistencia mucho mayor que la alcanzada en la última competencia. Sin embargo, dado que este método es susceptible a desviaciones o desfases de tiempo, su implementación final se está evaluando antes de la próxima competencia. Se agregaron nuevos comandos al código para el segundo modo con el fin de crear una base de código que luego pueda ser modificada según sea necesario el día de la competencia. 

2. Segunda Regional (Colegio Guayamurí - Nueva Esparta, Porlamar)

Se presentaron problemas de lentitud a la hora de trabajar con la interfaz gráfica de la Raspberry. Se recurrió a trabajar desde la terminal de Powershell de Windows una vez conectado al Hotspot de la Raspberry para compensarlo. Debido a que la Raspberry se sobresaturó de muchos códigos prueba que no se usaron en la competición, el carro redujo considerablemente su rendimiento. Para solucionar el problema de lentitud y rendimiento en carrera, se decidió formatear la Raspberry, no sin antes hacer un respaldo de todos los archivos.

3. Tercera Regional (Hotel Paradise - Anzoátegui, Puerto la Cruz)

Se encontró que el auto presentaba muchas dificultades para determinar cual era el sentido correcto de la pista. Se corrigió añadiendo un algoritmo el cual usaba las líneas de colores presentes en las esquinas de la pista, dando mejores resultados. Se logró visualizar que por el ángulo y el escaso grado de visibilidad que presenta la cámara el sistema no lograba detectar correctamente en ocasiones las líneas en el suelo. Se corrigió la posición de la cámara y se ajusto el ROI y el umbral de láz en la calibración para compensar este ajuste.

<hr>
