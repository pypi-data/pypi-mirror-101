import logging, os
from datetime import datetime
from . import HMTail
from . import HabMapsMessage
from . import MapTracker
from . import GPSAppender
LOGLEVEL = os.environ.get('HABLIB_LOGLEVEL', 'INFO').upper()
FORMATTER = os.environ.get('HABLIB_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOGFILE = os.environ.get('HABLIB_LOGFILE', '/tmp/hablibclient.log')
logging.basicConfig(level=LOGLEVEL, format=FORMATTER, handlers=[logging.FileHandler(LOGFILE), logging.StreamHandler()])
import traceback

class Parser(object):
    """docstring for Parser."""

    def __init__(self, confHandler):
        super(Parser, self).__init__()
        self.ch = confHandler.getConfig()
        self.mt = MapTracker.MapTracker(id=self.ch['basestation']['id'],
                                        mqtt_url=self.ch['mqtt']['url'],
                                        mqtt_port=int(self.ch['mqtt']['port']),
                                        user=self.ch['mqtt']['user'],
                                        publish=self.ch['mqtt']['topic'],
                                        alive=int(self.ch['mqtt']['alive']),
                                        password=self.ch['mqtt']['password']
                                        )
        self.gps_appender = GPSAppender.GPSAppender(self.ch)
        self.mt.startAlive()

    def parseline(self, line, definition):
        """ Core de parseo, aqui realiza la serialización a json de la traza retornando un HabMapsMessage"""
        trace = line.split('|')
        definitions = definition.split('|')
        i = 0
        hm = HabMapsMessage.HabMapsMessage()

        if len(trace) != len(definitions):
            logging.error("Invalid frame: " + str(len(trace)) + " != " + str(len(definitions)))
            logging.error(line)
            return None

        for el in definitions:
            if el != '':
                if el == '$time':
                    date_composed = datetime.now().strftime("%Y-%m-%d") + " " + trace[i][0:2] + ":" + trace[i][
                                                                                                      2:4] + ":" + \
                                    trace[i][4:6]
                    hm.setTimeStamp(date_composed)
                elif el == '$pos':
                    pos = trace[i].split(',')
                    hm.setHabPosition([float(pos[0]), float(pos[1])])
                elif el == '$id':
                    hm.setHabId(trace[i])
                # Parseo de señales
                else:
                    try:
                        hm.addSignal(el, float(trace[i]))
                    except Exception as e:
                        logging.info("Not a float signal")
                        hm.addSignal(el, trace[i])
            i += 1
        return hm

    def _print_line(self, txt):
        """ Call back, funcion que se llama por cada linea que se lee"""
        logging.debug(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "  --> Nueva linea:")
        logging.debug(txt)
        # 1.- Parseamos la traza que nos llega de lora
        try:
            hm = self.parseline(txt, self.ch['frame']['format'])
            if hm:
                # 2.- Obtenemos la ultima traza de gps
                pos_gps = self.gps_appender.getValueAsArray()
                hm.setBasestationPosition(pos_gps)
                # 3.- Transmitimos el mensaje
                self.mt.sendHabMessage(hm)
        except Exception as e:
            logging.error("Something went wrong ...")
            logging.error(e)
            logging.error(traceback.format_exc())


    def run(self):
        """ Función que lanza el parser """
        t = HMTail.Tail(self.ch['frame']['file'])
        t.register_callback(self._print_line)
        t.follow(s=float(self.ch['frame']['refresh']))