import logging
import sys
from logging.handlers import TimedRotatingFileHandler
FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOG_FILE = "my_app.log"

def get_console_handler():
    #UNIX VERSION
    console_handler = logging.handlers.SysLogHandler(facility=logging.handlers.SysLogHandler.LOG_DAEMON, address="/dev/log")
    #OSX VERSION
    #console_handler = logging.handlers.SysLogHandler(address='/var/run/syslog', facility='local1')
    console_handler.setFormatter(FORMATTER)
    return console_handler

def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler

def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())

    logger.propagate = False
    return logger

"""
my_logger = get_logger("my module name")
my_logger.debug("a debug message!!!")
"""


"""
gclass_logger = logging.getLogger('gclass_logger')

console_handler = logging.StreamHandler()
gclass_logger.addHandler(console_handler)

gclass_logger.setLevel(logging.INFO)
gclass_logger.info("you will see this")
"""





