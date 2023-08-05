from . import Appender
import os,logging,traceback
LOGLEVEL = os.environ.get('HABLIB_LOGLEVEL', 'INFO').upper()
FORMATTER = os.environ.get('HABLIB_FORMAT', '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')
LOGFILE = os.environ.get('HABLIB_LOGFILE', '/tmp/hablibclient.log')
logging.basicConfig(level=LOGLEVEL, format=FORMATTER, handlers=[logging.FileHandler(LOGFILE),logging.StreamHandler()])

class GPSAppender(Appender.Appender):
    """docstring for GPSAppender."""
    def __init__(self, chandler):
        super(GPSAppender, self).__init__()
        self.file = chandler['basestation']['appenders']['gpsappender']['file']
        self.regex = chandler['basestation']['appenders']['gpsappender']['regexselect']
        self.mapping = chandler['basestation']['appenders']['gpsappender']['mapping']

    def readValue(self):
        retval = {
            'lat': 0.0,
            'lon': 0.0,
            'height': 0.0
        }
        if self.file == '':
            logging.debug(" GPS Appender is not configured ...")
            return retval
        try:
            #1.- Obtenemos la ultima linea
            logging.debug("GPS Appender is trying to read the file: " + str(self.file) )
            values = self.getLastLine(self.file)
            logging.debug("Last GPS Appender line readed : " + values)
            #2.- Parseamos la linea
            ret=self.mapRegex(self.regex,values, self.mapping)
            logging.debug(" Parsed frame: ")
            logging.debug(ret)
            if ret['isOK']:
                retval = {
                    'lat': float(ret['out']['lat']),
                    'lon': float(ret['out']['lon']),
                    'height': float(ret['out']['height']),
                }
            return retval
        except Exception as e:
            logging.error("Something went wrong parsing the GPS frame ...")
            logging.error(e)
            logging.error(traceback.format_exc())
            return retval

    def getValueAsArray(self):
        val = self.readValue()
        return [val['lat'], val['lon'], val['height']]