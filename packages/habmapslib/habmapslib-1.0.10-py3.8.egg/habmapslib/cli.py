import click
from . import confyaml
from . import ConfHandler
from . import Parser
import logging,os
LOGLEVEL = os.environ.get('HABLIB_LOGLEVEL', 'INFO').upper()
FORMATTER = os.environ.get('HABLIB_FORMAT', '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')
LOGFILE = os.environ.get('HABLIB_LOGFILE', '/tmp/hablibclient.log')
logging.basicConfig(level=LOGLEVEL, format=FORMATTER, handlers=[logging.FileHandler(LOGFILE),logging.StreamHandler()])


@click.command()
@click.option('--conffile', help='Fichero de configuración')
@click.option('--genconffile', is_flag=True, help='Muestra un fichero de configuración de ejemplo')
def cline(conffile, genconffile):
    if genconffile:
        print(confyaml.conf)
        return 0
    elif conffile:
        ch = ConfHandler.ConfHandler(file=conffile)
        logging.info("Launching habmapslib parser with the next configuration:")
        logging.info(ch.getConfig())
        p = Parser.Parser(ch)
        p.run()


if __name__ == '__main__':
    cline()