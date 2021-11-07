import logging
import os
import datetime


class Logger(object):
    """
    Class of the logger to log different handled errors in the code.
    """
    LOG_TYPES = {'info': logging.info, 'debug': logging.debug, 'warning': logging.warning, 'critical': logging.critical}

    def __init__(self, name: str, log_directory: str, printed: bool = False):
        """
        Initializer method
        :param name: Name of the log file or the log types intended for each instance.
        :type name: str
        :param log_directory: Directory to store the log file (either relevant to the code constructing Logger object or
        absolute path).
        :type log_directory: str
        :param printed: Whether the log message should be printed or not.
        :type printed: bool
        """

        # Logging setup
        self.log_directory = log_directory
        self.printed = printed
        self.name = name
        try:
            logging.basicConfig(filename=f'{self.log_directory}/{self.name}.log', level=logging.DEBUG)
        except FileNotFoundError:
            os.mkdir(f'{self.log_directory}/')
            logging.basicConfig(filename=f'{self.log_directory}/{self.name}.log', level=logging.DEBUG)

    def log(self, msg, log_type):
        """
        This is a function for logging success and failures

        :param msg: The message to be logged
        :type msg: str
        :param log_type: The type of log (either info or critical)
        :type log_type: str
        :return: None
        :rtype: NoneType
        """
        log_time = datetime.datetime.now()
        if self.printed:
            print(f"{log_time} - {log_type} - {msg}")
        self.LOG_TYPES[log_type](f"{log_time.date()} {log_time.hour}:{log_time.minute} | " + msg)
