import logging
from datetime import datetime

class Log:
    def __init__(self, name):
        # create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # create console handler and set level to debug
        #ch = logging.StreamHandler()
        #ch.setLevel(logging.DEBUG)
        
        # create file handler and set level to debug
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        fh = logging.FileHandler(f'adecuator_log_{current_time}.log')
        fh.setLevel(logging.DEBUG)
        
        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # add formatter to ch and fh
        #ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        
        # add ch and fh to logger
        #self.logger.addHandler(ch)
        self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)