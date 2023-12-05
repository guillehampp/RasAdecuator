import logging

class Log:
    def __init__(self, name):
        # create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # create console handler and set level to debug
        #ch = logging.StreamHandler()
        #ch.setLevel(logging.DEBUG)
        
        # create file handler and set level to debug
        fh = logging.FileHandler('arch_logfile.log')
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