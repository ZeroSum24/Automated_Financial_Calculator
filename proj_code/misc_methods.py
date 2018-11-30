from os import mkdir
from os.path import basename, exists, splitext
import inspect
import logging

logger = logging.getLogger()

# Create all desired directories
def create_directories(list_dir: list, logger_name=""):

    global logger
    logger = set_up_logging(logger_name)

    # iterating over all the needed directories, adding them if they don't exist
    for dirName in list_dir:

        if not exists(dirName):
            try:
                # Create target Directory
                mkdir(dirName)
                logger.info("Directory created: {0} ".format(dirName))
            except Exception:
                logger.error("During directory creation exception occured")
        else:
            logger.info("Directory already exists: {0} ".format(dirName))

    logger.info("Directory creation complete")

# Sets up consistent logging across library
def set_up_logging(logger_name: str):

    if logger_name != "":

        # create the updated file names for the logger
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0]) # gets file name of method caller
        file_name = splitext(basename(module.__file__))[0]

        logger_full_name = "{0}.{1}".format(logger_name, file_name)
        # update global logger with correct name
        global logger
        logger = logging.getLogger(logger_full_name)

        logger.info("Logging was set up correctly")
    else:
        logger.info("Global Logging was not set up")

    return logger

# initialise main app logger
def init_logger(logger_name: str, level=logging.DEBUG, log_path=None,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"):

    # initialise the logging object and setting the logging level
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # setting up the handler to stream or file
    hdlr = logging.StreamHandler()
    if log_path != None:
        hdlr = logging.FileHandler(log_path)

    # Set the log level
    hdlr.setLevel(level)

    # add formatter to handler
    formatter = logging.Formatter(format)
    hdlr.setFormatter(formatter)

    # attaching the handler to the logger
    logger.addHandler(hdlr)

    return logger

def create_file(file: str):
    """Creating a file if doesn't already exist"""

    if not os.path.exists(file):
        file = open(file,"w+")
