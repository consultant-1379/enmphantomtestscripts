import os,sys
import logging
from logging import handlers
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../hwapp')))  # drop from ../hwapp/logger to ../hwapp
import definitions

def activate_logging(logname="hardware_management.log"):
    logging.basicConfig(filename=definitions.LOG_ROOT + logname,
                        filemode='a',
                        format='%(asctime)s:%(msecs)d - %(name)s - %(levelname)s - %(module)s:%(funcName)s - %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
    # Create a logger

            #global logger # TODO revisit why global is needed
    logger = logging.getLogger(__name__)
    # Create a StreamHandler and add it to the console handler and set the format
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        '%(asctime)s:%(msecs)d - %(name)s - %(levelname)s - %(module)s:%(funcName)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    # Create a file handler and set the format
    file_handler = logging.FileHandler(filename=definitions.LOG_ROOT + logname)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(funcName)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    # Add the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    #logging.getLogger().addHandler(console_handler)
    logger.debug(f"activate_logging({logname})")
    return logger
class Logger:
    """
    Singleton Logger class. This class is only instantiated ONCE. It is to keep a consistent
    criteria for the logger throughout the application if need be called upon.
    It serves as the criteria for initiating logger for modules. It creates child loggers.
    It's important to note these are child loggers as any changes made to the root logger
    can be done.

    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.debug_mode = True
            cls.formatter = logging.Formatter(
                "%(asctime)s — %(name)s — %(levelname)s — %(message)s"
            )
            cls.log_file = "application_log_file.log"

        return cls._instance

    def get_console_handler(self):
        """Defines a console handler to come out on the console

        Returns:
            logging handler object : the console handler
        """
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        console_handler.name = "consoleHandler"
        return console_handler

    def get_file_handler(self):
        """Defines a file handler to come out on the console.

        Returns:
            logging handler object : the console handler
        """
        file_handler = handlers.RotatingFileHandler(
            self.log_file, maxBytes=5000, backupCount=1
        )
        file_handler.setFormatter(self.formatter)
        file_handler.name = "fileHandler"
        return file_handler

    def add_handlers(self, logger, handler_list: list):
        """Adds handlers to the logger, checks first if handlers exist to avoid
        duplication

        Args:
            logger: Logger to check handlers
            handler_list: list of handlers to add
        """
        existing_handler_names = []
        for existing_handler in logger.handlers:
            existing_handler_names.append(existing_handler.name)

        for new_handler in handler_list:
            if new_handler.name not in existing_handler_names:
                logger.addHandler(new_handler)

    def get_logger(self, logger_name: str):
        """Generates logger for use in the modules.
        Args:
            logger_name (string): name of the logger

        Returns:
            logger: returns logger for module
        """
        logger = logging.getLogger(logger_name)
        console_handler = self.get_console_handler()
        file_handler = self.get_file_handler()
        self.add_handlers(logger, [console_handler, file_handler])
        logger.propagate = False
        return logger

    def set_debug_mode(self, debug_mode: bool):
        """
        Function to set the root level logging to be debug level to be carried forward throughout
        Args:
            debug_mode (bool): debug mode initiation if true
        """
        if debug_mode:
            logging.root.setLevel(logging.DEBUG)
