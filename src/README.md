# Documentación del software del robot

Esta guía describe los archivos de [`src/`](https://github.com/SamuelGuaimaB/Ingenieros-Paralelos/tree/main/src) en la rama `main`, revisados el 13 de septiembre de 2026. Explica el comportamiento implementado en el código, para que se pueda entender, calibrar y mantener sin tener que leer cada línea. Los programas de `Viejos Codigos usados/` son versiones históricas.

## Cómo se conectan los componentes

La **Raspberry Pi** ejecuta uno de los modos de conducción y envía instrucciones por el puerto `/dev/ttyUSB0` a `115200` baudios. El **Arduino** recibe el par `<velocidad,ángulo>` y actúa sobre el motor y el servo. Al pulsar el botón físico, el Arduino envía `BTN:1`; cada modo espera esa señal antes de iniciar el movimiento. El calibrador funciona aparte y ayuda a escoger parámetros de visión.

| Archivo | Responsabilidad | Entrada principal | Salida principal |
| --- | --- | --- | --- |
| [`1er_modo.py`](https://github.com/SamuelGuaimaB/Ingenieros-Paralelos/blob/main/src/1er_modo.py) | Conducir según la cámara | Fotogramas y `BTN:1` | Órdenes de motor y dirección |
| [`2do_modo.py`](https://github.com/SamuelGuaimaB/Ingenieros-Paralelos/blob/main/src/2do_modo.py) | Ejecutar una secuencia de movimientos cronometrados | `RUTINA_MANUAL` y `BTN:1` | Órdenes de motor y dirección |
| [`Ino Code/Arduino_code.ino`](https://github.com/SamuelGuaimaB/Ingenieros-Paralelos/blob/main/src/Ino%20Code/Arduino_code.ino) | Accionar el hardware y leer el botón | Órdenes serie y pulsador | Movimiento físico y `BTN:1` |
| [`calibracion.py`](https://github.com/SamuelGuaimaB/Ingenieros-Paralelos/blob/main/src/calibracion.py) | Inspeccionar máscaras de piso y color | Cámara y barras de ajuste | Ventanas de vista previa y valores por consola |
| [`robot.service`](https://github.com/SamuelGuaimaB/Ingenieros-Paralelos/blob/main/src/robot.service) | Configurar el arranque mediante `systemd` | Inicio del sistema | Ejecutar un script local |

**Protocolo serie.** El comando de ejemplo `<250,86>` pide velocidad positiva `250` y dirección `86°` (centro). Un valor negativo invierte el motor; `0` lo detiene. Arduino acepta el carácter inicial `<` y lee dos números con `Serial.parseInt()`, pero **no verifica expresamente** la coma ni `>`. El botón se comunica en sentido inverso mediante la línea `BTN:1`.

## Modo 1: navegación por cámara

**Archivo:** `src/1er_modo.py` · **Clase:** `WROPrimitivoBlindado`

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

## Modo 2: secuencia temporizada

**Archivo:** `src/2do_modo.py` · **Clase:** `WROCoreografia`

Este modo sigue una coreografía fija. Cada elemento activo de `RUTINA_MANUAL` tiene la forma `(velocidad, ángulo, duración_en_segundos, descripción)`. Por ejemplo, `(-140, 86, 0.2, "Retroceso estacionamiento")` manda marcha atrás durante `0,2 s` con las ruedas centradas. Las líneas comentadas en la lista no se ejecutan.

| Bloque | Qué hace |
| --- | --- |
| `__init__()` | Intenta conectar al Arduino y espera `2 s` para su reinicio. |
| `run()` | Comprueba el servo con el barrido `120° → 60° → 86°`, espera el botón y lanza la secuencia. |
| `esperar_boton()` | Envía `<0,86>` y consulta el serial hasta recibir `BTN:1`. |
| `ejecutar_rutina()` | Recorre las tuplas en orden, envía cada instrucción y espera su duración; al final envía `<0,86>` y cierra el serial. |

La velocidad positiva implica avance, la negativa reversa y `0` una pausa del motor; el ángulo determina la orientación del servo. Estas son **fases descriptivas**, no estados formales del programa. Como no usa la cámara ni otro sensor para corregir posición, la trayectoria depende del tiempo programado y del comportamiento físico real. Si el serial no se abre, `esperar_boton()` permanece esperando porque no puede recibir `BTN:1`.

**Para ajustar el recorrido**, se modifica `RUTINA_MANUAL`, especialmente las duraciones y los ángulos de cada paso activo. El programa no mide la distancia realmente recorrida.

## Arduino: botón, motor y servo

**Archivo:** `src/Ino Code/Arduino_code.ino`

- **`setup()`** abre el serial, configura los pines, centra el servo en `86°` y apaga el motor. Los pines definidos son servo `6`, PWM del motor `3`, dirección `5` y `4`, y botón `2` con resistencia interna `INPUT_PULLUP`.
- **`loop()`** confirma la pulsación después de `50 ms` y envía `BTN:1` una sola vez mediante `botonEnviado`. También escucha el serial: al ver `<`, lee velocidad y ángulo, mueve el motor y limita el servo al intervalo `50°–122°`.
- **`moverMotor()`** limita la velocidad a `-255…255`. Cambia el sentido con los dos pines de dirección y aplica el valor absoluto del PWM en reversa.
- **`detenerMotores()`** baja ambos pines de dirección y escribe PWM `0`.

El Arduino convierte los comandos en acciones, pero no informa de vuelta la velocidad ni el ángulo alcanzados. El botón se informa una vez por arranque del microcontrolador, no una vez por cada ejecución de `RUTINA_MANUAL`.

## Calibración de visión

**Archivo:** `src/calibracion.py`

El script abre la cámara a `320 × 240` y muestra tres ventanas: región de interés, máscara y resultado. Sus barras permiten escoger **modo 0: piso**, **modo 1: naranja** o **modo 2: azul**, además del umbral o los límites HSV correspondientes.

Para piso toma el ROI `frame[40:180, 0:320]`, aplica escala de grises, suavizado y umbral binario. Para naranja o azul convierte ese ROI a HSV, construye una máscara con los límites seleccionados y quita puntos pequeños mediante apertura morfológica. La tecla `p` imprime los valores mostrados; `q` sale, libera la cámara y cierra las ventanas. **El calibrador no guarda parámetros en archivos ni actualiza automáticamente `1er_modo.py`:** los valores útiles deben trasladarse manualmente. Su ROI y umbral predeterminados tampoco son idénticos a los del modo 1, por lo que conviene contrastarlos antes de copiarlos.

## Servicio de arranque y versiones anteriores

`robot.service` declara un servicio de `systemd` que trabaja como `root` desde `/root/Desktop` y ejecuta **`/root/Desktop/2do.py`**, con reinicio si falla. Ese destino no corresponde a `src/2do_modo.py`; para utilizarlo tal como está, el archivo indicado tendría que existir en la Raspberry. Esta descripción documenta la configuración incluida en el repositorio, no confirma que el servicio esté instalado o habilitado en el robot.

`src/README.md` presenta la carpeta. `src/Viejos Codigos usados/` conserva programas de competiciones anteriores: ayudan a estudiar la evolución del proyecto, pero esta guía se centra en los archivos activos enumerados arriba.
