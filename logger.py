import logging
import os
import datetime
import traceback


class Logger(object):
    """
    Class of the logger to log different handled errors in the code.
    """
    LOG_TYPES = {'info': logging.info, 'debug': logging.debug, 'warning': logging.warning, 'critical': logging.critical}

    def __init__(self, name: str, log_directory: str, printed: bool = False, traceback_log: bool = False):
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
                extra_info += " " * indentation + f"- Line {frame.f_lineno} of file {frame.f_code.co_filename} --> \n"
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
