import logging
from datetime import datetime


class Log:
    """
    A class for logging messages to a file.

    Attributes:
        logger (logging.Logger): The logger object for logging messages.
    """

    def __init__(self, name):
        """
        Initializes a Log object.

        Args:
            name (str): The name of the logger.

        """
        # create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # create file handler and set level to debug
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        fh = logging.FileHandler(f"log/adecuator_log_{current_time}.log")
        fh.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # add formatter to fh
        fh.setFormatter(formatter)

        # add fh to logger
        self.logger.addHandler(fh)

    def debug(self, message):
        """
        Logs a debug message.

        Args:
            message (str): The message to be logged.

        """
        self.logger.debug(message)

    def info(self, message):
        """
        Logs an info message.

        Args:
            message (str): The message to be logged.

        """
        self.logger.info(message)

    def warning(self, message):
        """
        Logs a warning message.

        Args:
            message (str): The message to be logged.

        """
        self.logger.warning(message)

    def error(self, message):
        """
        Logs an error message.

        Args:
            message (str): The message to be logged.

        """
        self.logger.error(message)

    def critical(self, message):
        """
        Logs a critical message.

        Args:
            message (str): The message to be logged.

        """
        self.logger.critical(message)
