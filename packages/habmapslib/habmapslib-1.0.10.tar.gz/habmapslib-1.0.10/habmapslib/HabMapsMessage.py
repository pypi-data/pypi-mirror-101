from datetime import datetime, timedelta
import os
import json,logging
LOGLEVEL = os.environ.get('HABLIB_LOGLEVEL', 'INFO').upper()
FORMATTER = os.environ.get('HABLIB_FORMAT', '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')
LOGFILE = os.environ.get('HABLIB_LOGFILE', '/tmp/hablibclient.log')
logging.basicConfig(level=LOGLEVEL, format=FORMATTER, handlers=[logging.FileHandler(LOGFILE),logging.StreamHandler()])

class HabMapsMessage(object):
    def __init__(self,
                 TimeStamp='',
                 HabId='',
                 BasestationId='',
                 HabPosition=[-1.0,-1.0],
                 Signals={},
                 BasestationPosition=[0.0,0.0]):
        super(HabMapsMessage, self).__init__()
        self._track = {
            "type": "frame",
            "ftime": '',
            "hab": {
                "id": '',
                "pos": {
                    "lat": -1.0,
                    "lon": -1.0
                },
                "payload": {}
            },
            "basestation": {
                "id": '',
                "pos": {
                    "lat": 0.0,
                    "lon": 0.0
                }
            }
        }
        if TimeStamp != '':
            self.setTimeStamp(TimeStamp)
        self.setHabId(HabId)
        self.setBasestationId(BasestationId)
        self.setHabPosition(HabPosition)
        self.setBasestationPosition(BasestationPosition)
        self._track['hab']['payload'] = Signals

    def getMessage(self):
        return self._track

    def printMessage(self):
        print(json.dumps(self._track))

    def _setTS(self):
        self._track['ftime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def isValidMessage(self):
        valid = True

        if self._track['hab']['pos']['lat'] == -1.0 or self._track['hab']['pos']['lon'] == -1.0:
            logging.error('Please set a valid hab pos with setHabPosition([<float : lat>, <float : lon>])')
            valid = False

        if self._track['hab']['id'] == '':
            logging.error('Please set a habid with setHabId(<string : id>)')
            valid = False

        if self._track['basestation']['id'] == '':
            logging.error('Please set a habid with setBasestationId(<string : id>)')
            valid = False

        if self._track['ftime'] == '':
            self._setTS()

        return valid

    # SETTERS *******
    def setTimeStamp(self, ts):
        try:
            datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
            self._track['ftime'] = ts
        except ValueError:
            logging.error("Invalid date format")
            raise ValueError("Incorrect data format, should be YYYY-mm-dd H:M:S")


    def setHabPosition(self, habpos):
        self._track['hab']['pos']['lat'] = float(habpos[0])
        self._track['hab']['pos']['lon'] = float(habpos[1])

    def setBasestationPosition(self,bspos):
        self._track['basestation']['pos']['lat'] = float(bspos[0])
        self._track['basestation']['pos']['lon'] = float(bspos[1])
        if len(bspos) == 3 and float(bspos[2]) != 0.0:
            self.addSignal('BStationHeight',float(bspos[1]))

    def addSignal(self,key,value):
        self._track['hab']['payload'][key] = value

    def setHabId(self,id):
        self._track['hab']['id'] = id.replace(" ","-")

    def setBasestationId(self,id):
        self._track['basestation']['id'] = id.replace(" ","-")

