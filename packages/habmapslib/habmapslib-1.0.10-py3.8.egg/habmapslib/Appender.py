class Appender(object):
    """Base para los appenders"""
    def __init__(self):
        super(Appender, self).__init__()

    def getLastLine(self,path):
        with open(path, 'r') as f:
            lines = [line for line in f.read().split('\n') if line.strip() != '']
            last_line = lines[-1]
            return last_line


