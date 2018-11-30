from os import mkdir
from os.path import basename, splitext
import logging

logger = logging.getLogger()

# Create all desired directories
def create_directories(list_dir: list, logger_name=""):

    set_up_logging(logger_name)
    # iterating over all the needed directories
    for dirName in list_dir:
        try:
            # Create target Directory
            mkdir(dirName)
            logger.info("Directory " , dirName ,  " Created ")
        except FileExistsError:
            logger.info("Directory " , dirName ,  " already exists")

    logger.info("Directory creation complete")

# Sets up consistent logging across library
def set_up_logging(logger_name: str):

    if logger_name != "":

        # create the updated file names for the logger
        file_name = splitext(basename(__file__))[0]
        logger_full_name = "{0}.{1}".format(logger_name, file_name)
        # update global logger with correct name
        global logger
        logger = logging.getLogger(logger_full_name)

        logger.info("Logging was set up correctly")
    else:
        logger.info("Global Logging was not set up")

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
