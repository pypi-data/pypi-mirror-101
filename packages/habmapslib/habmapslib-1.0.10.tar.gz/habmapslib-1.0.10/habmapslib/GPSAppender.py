from . import Appender
import os,logging
LOGLEVEL = os.environ.get('HABLIB_LOGLEVEL', 'INFO').upper()
FORMATTER = os.environ.get('HABLIB_FORMAT', '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')
LOGFILE = os.environ.get('HABLIB_LOGFILE', '/tmp/hablibclient.log')
logging.basicConfig(level=LOGLEVEL, format=FORMATTER, handlers=[logging.FileHandler(LOGFILE),logging.StreamHandler()])

class GPSAppender(Appender.Appender):
    """docstring for GPSAppender."""
    def __init__(self, chandler):
        super(GPSAppender, self).__init__()
        self.path = chandler['basestation']['appenders']['gpsappender']

    def readValue(self):
        if self.path == '':
            return {
                'lat': 0.0,
                'lon': 0.0,
                'height': 0.0
            }
        try:
            values = self.getLastLine(self.path)
            logging.debug("Readed gps base statio pos: " )
            logging.debug(values)
            splt = values.split(",")
            return {
                'lat': splt[0],
                'lon': splt[1],
                'height': splt[2]
            }
        except Exception as e:
            raise e

    def getValueAsArray(self):
        val = self.readValue()
        return [val['lat'], val['lon'], val['height']]