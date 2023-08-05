"""Modulo que se encarga de validar que todo esta listo para funcionar"""
import os,logging,traceback
LOGLEVEL = os.environ.get('HABLIB_LOGLEVEL', 'INFO').upper()
FORMATTER = os.environ.get('HABLIB_FORMAT', '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')
LOGFILE = os.environ.get('HABLIB_LOGFILE', '/tmp/hablibclient.log')
logging.basicConfig(level=LOGLEVEL, format=FORMATTER, handlers=[logging.FileHandler(LOGFILE),logging.StreamHandler()])
import time

def createFile(file):
    f = open(file, "w+")
    f.write("\n")
    f.close()

def checkIfFileExists(file,autoCreate=False):
    isOK = False
    try:
        with open(file) as f:
            return True
    except IOError as e:
        logging.error("==> Please create the file: " + file)
        logging.error(e)
        if autoCreate:
            logging.info("Autocreate is enabled, creating the file ..." + file)
            createFile(file)
        return False


def checkConfigs(ch):
    logging.info("Checking configs ...")
    isOK = False
    while not isOK:
        okarr=[]
        #1.- Validación del fichero de gps
        if ch['basestation']['appenders']['gpsappender']['file'] != '':
            okarr.append(checkIfFileExists(ch['basestation']['appenders']['gpsappender']['file'],autoCreate=True))

        #2.- Validación del fichero de trazas lora
        okarr.append(checkIfFileExists(ch['frame']['file']))

        #Chequeamos si todo esta correcto
        if False in okarr:
            logging.error("Please check that all files exist ...")
            time.sleep(5)
        else:
            logging.info("Checks are ok, starting de program ...")
            isOK = True

