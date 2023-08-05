conf='''basestation:
  id: "id-de-mi-estacion"
  appenders:
    gpsappender: "/Users/alvaroperis/ArchLab/habmapsgateway/demotraces/gps.appender"
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
  file: "/Users/alvaroperis/ArchLab/habmapsgateway/demotraces/out.log"
  # Cada cuantos segundos se mira el fichero de envio
  refresh: 1
'''