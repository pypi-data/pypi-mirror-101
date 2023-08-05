# habmapslib

Librería para el uso de [habmaps](https://github.com/alpeza/habmaps)

* [GitHub](https://github.com/alpeza/habmapsgateway)
* [Pypi](https://pypi.org/project/habmapslib/#description)

## Quick Start

__1.- Instalamos el cliente de habmaps con__

Opción 1

```bash
pip3 install habmapslib
# para el upgrade pip3 install --upgrade habmapslib
```

Opción 2, instalación manual

```bash
git clone https://github.com/alpeza/habmapsgateway.git
cd habmapsgateway/habmapslib
sudo python3 setup.py install
```

__2.- Envíamos información a la plataforma__

```python
from habmapslib import MapTracker, HabMapsMessage
import time

mt = MapTracker.MapTracker(id="default-station-id", #Nombre de la estación base
                           mqtt_url="localhost",    #DNS o IP del servidor MQTT
                           mqtt_port=1883,          #Puerto del servidor MQTT
                           user='habmaps',          #Credenciales de acceso al broker MQTT
                           password='root')

mt.startAlive() #Iniciamos la señal de alive que se enviará cada n minutos 

while True:
    mt.sendHabMessage(HabMapsMessage.HabMapsMessage(
        TimeStamp='2021-04-02 15:33:43', #El timestamp del hab en formato string datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        HabId='Mi-Hab', #Nombre del hab que se esta monitorizando, vendrá de la traza q transmita el hab
        HabPosition=[5, 3], #Array de [ latitud, longitud]
        Signals={ #Payload de sensores clave: Nombre del sensor, valor: valor del sensor
            "miSensorUno": 122.4,
            "miSensorDos": 400.5
        },
        BasestationPosition=[5, 3])) #Array opcional de [ latitud, longitud] de posición de la estacion base
    time.sleep(5)
```

## Logging

La configuración de los logs se realiza a través de variables de entorno

```bash
export HABLIB_LOGLEVEL=DEBUG #INFO,ERROR
export HABLIB_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
export HABLIB_LOGFILE="/tmp/hablibclient.log"
```

## Error Handling

```python
    rc = mt.sendHabMessage(HabMapsMessage.HabMapsMessage(
    TimeStamp='2021-04-02 15:33:43',
    HabId='Mi-Hab',
    HabPosition=[5, 3],
    Signals={
        "miSensorUno": 122.4,
        "miSensorDos": 400.5
    },
    BasestationPosition=[5, 3]))
if rc['isOK']:
    print("El mensaje se ha enviado correctamente ... ")
else:
    print("Ha existido algun error en la transmision ...")
    print(rc['reason'])
```

## CLI FileParser

La librería también se puede emplear a modo de _daemon_ que va leyendo
de un fichero y transmitiéndolo a habmaps.

```bash
python3 -m habmapslib.cli --help
```

1.- Configuramos el programa:

```bash
python3 -m habmapslib.cli --genconffile > miConfig.yaml
#Editamos la configuración
nano miConfig.yaml
```
2.- Lanzamos el programa

```bash
python3 -m habmapslib.cli --conffile miConfig.yaml
```

### Configuración del CLI FileParser

La configuración se define a través de un fichero YAML.

```yaml
basestation:
  id: "id-de-mi-estacion"
  appenders:
    gpsappender:
      file: '/Users/tests/ArchLab/habmapsgateway/demotraces/gps.appender'
      regexselect: '\[.*\]\|(.*)\|(.*),(.*)\|.*\|'
      mapping:
        - "height"
        - "lat"
        - "lon"
mqtt:
  url: "localhost"
  topic: "hablistener"
  port: 1883
  user: "habmaps"
  password: "root"
  alive: 60
frame:
  # Definición de la trama donde
  # $time : Es la hora expresada en HHMMSS
  # $pos : Es la posición gps del hab expresada en lat,lon
  # $id  : Es el identificador del hab
  format: "$time|AlturaGPS|$pos|VelocidadHorizontalGPS|Temperatura|Presion|AlturaBarometrica|$id|"
  # Fichero donde se van insertando las trazas de LoRa
  file: "/Users/tests/ArchLab/habmapsgateway/demotraces/out.log"
  # Cada cuantos segundos se mira el fichero de envio
  refresh: 1
``` 

Nos resultarán de mayor interés las siguientes secciones:

#### Appender GPS

Se trata de un fichero donde el programa espera encontrar la posición GPS de la
antena.

```yaml
  ...
  appenders:
    gpsappender:
      file: '/Users/tests/ArchLab/habmapsgateway/demotraces/gps.appender'
      regexselect: '\[.*\]\|(.*)\|(.*),(.*)\|.*\|'
      mapping:
        - "height"
        - "lat"
        - "lon"
```

En caso de no disponer de un módulo gps. Se puede dejar a blancos:

```yaml
  ...
  gpsappender:
    file: ''
```

El GPS appender funciona del siguiente modo:

- 1.- Filtra la última línea del fichero indicado en el campo `gpsappender.file`.
- 2.- Sobre esta última línea aplicará el filtro que se le haya indicado mediante la expresión
  regular definida en `gpsappender.regexselect`.
- 3.- Los __grupos__ que salgan de esta expresión regular los mapeará según defina el orden de la lista `mapping.mapping`.
  En este caso el grupo 1 se corresponderá con el campo `height` mientras que el grupo 3 con `lon`.

> Podemos validar la expresión regular en [regex101](https://regex101.com/). La expresión regular
> del ejemplo se corresponde con la trama `[2021-03-28 18:49:02][INFO]|1129|42.3074,2.2111|0.1187|`


#### Trama de la sonda

El programa tratará de realizar un envío a mqtt por cada línea nueva que detecte en el fichero `frame.file`.
Este interpretará y mapeará  la línea a json según se le especifique en `frame.format`. Cada campo vendrá separado por el caracter `|`.

Existen campos de mapeo reservados:

* `$time`: Se interpreta como el _timestamp_ de la sonda especificado en forma `HHMMSS`.
* `$pos` : Se interpreta como la posición gps de la sonda expresada como `lat,lon`.
* `$id`: Se interpreta como el `id` de la sonda.

```yaml
...
frame:
  format: "$time|AlturaGPS|$pos|VelocidadHorizontalGPS|Temperatura|Presion|AlturaBarometrica|$id|"
  file: "/Users/tests/ArchLab/habmapsgateway/demotraces/out.log"
```

El resto de campos se interpretarán como valores de sensor.

Un ejemplo de trama de sonda para este formato es el siguiente:

```
185359|1127|4.3074,2.2111|0.1717|22.64|900.5943|983|HABCAT2|
```
