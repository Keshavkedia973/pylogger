import logging
import os
import datetime


class LoggerSet(object):
    """
    LoggerSet object allows for multiple logger creation at the same time.
    """

    def __init__(self, *args, log_directory: str, printed: bool = False, traceback_log: bool = False):
        """
        Initializer method for LoggerSet to define the name of the log files and the directory holding the files.
        :param args: Holding the name of all the logger instances
        :type name: tuple
        :param log_directory: Directory to store the log files (either relevant to the code constructing Logger object
        or absolute path).
        :type log_directory: str
        """
        self.loggers = {name: Logger(name, log_directory=log_directory, printed=printed, traceback_log=traceback_log)
                        for name in args}

    def __getattr__(self, item):
        return self.loggers.get(item, None)

    def __str__(self):
        return f"LoggerSet object with {self.loggers} loggers: {tuple(self.loggers.keys())}"


class _LoggerBase(object):
    def __init__(self, name: str, log_directory: str):
        """
        Initializer method for Logger base to define the name of the log file and the directory holding the file.
        :param name: Name of the log file or the log types intended for each instance.
        :type name: str
        :param log_directory: Directory to store the log file (either relevant to the code constructing Logger object or
        absolute path).
        :type log_directory: str
        """
        self.name = name
        self.log_directory = log_directory


class Logger(_LoggerBase):
    """
    Class of the logger to log different handled errors in the code.
    """
    LOG_TYPES = {'info': logging.info, 'debug': logging.debug, 'warning': logging.warning, 'critical': logging.critical}
    logger_instances = {}

    def __init__(self, name: str, log_directory: str, printed: bool = False, traceback_log: bool = False):
        """
        Initializer method
        :param printed: Whether the log message should be printed or not.
        :type printed: bool
        :return: None
        :rtype: None
        """
        # Calling the superclass init
        super(Logger, self).__init__(name=name, log_directory=log_directory)

        # Logging setup
        self.log_directory = log_directory
        self.printed = printed
        self.name = name
        self.traceback_log = traceback_log
        try:
            logging.basicConfig(filename=f'{self.log_directory}/{self.name}.log', level=logging.DEBUG)
        except FileNotFoundError:
            os.mkdir(f'{self.log_directory}/')
            logging.basicConfig(filename=f'{self.log_directory}/{self.name}.log', level=logging.DEBUG)

    def log(self, msg, log_type, error):
        """
        This is a function for logging success and failures

        :param msg: The message to be logged
        :type msg: str
        :param log_type: The type of log (either info or critical)
        :type log_type: str
        :param error: The error captured in the code
        :type error: Exception
        :return: None
        :rtype: NoneType
        """
        log_time = datetime.datetime.now()

        # Creating the string for the basic info
        basic_info = f"{log_time.date()} {log_time.hour}:{log_time.minute} | " + msg

        # Creating the string for the extra info
        if self.traceback_log:
            extra_info = f"\nOriginal Error: {error} in: \n"
            frame = error.__traceback__.tb_frame
            indentation = len(extra_info)
            print(indentation)

            while frame:
                extra_info += " " * indentation + f"- Line {frame.f_lineno} at {frame.f_code.co_name} function of " \
                                                  f"file {frame.f_code.co_filename} --> \n"
                frame = frame.f_back
            extra_info = extra_info.rstrip(" --> \n") + "\n"
        else:
            extra_info = ""

        # Creating the final message to be logged
        output_msg = basic_info + extra_info
        output_msg += "-" * 20

        if self.printed:
            print(output_msg)

        self.LOG_TYPES[log_type](output_msg)


class LogFetch(_LoggerBase):
    def __init__(self, name, log_directory):
        """
        Initializer method to determine the name of the log file and the directory holding the file.
        :param name: Name of the log file
        :type name: str
        :param log_directory: Directory to store the log file (either relevant to the code constructing Logger object or
        absolute path).
        :type log_directory: str
        """
        super(LogFetch, self).__init__(name=name, log_directory=log_directory)
