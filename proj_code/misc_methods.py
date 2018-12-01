from os import mkdir
from os.path import basename, exists, splitext
import inspect
import logging

logger = logging.getLogger()

# Create all desired directories
def create_directories(path_directories: dict, logger_name=""):

    # setting up logging
    global logger
    logger = set_up_logging(logger_name)

    # iterating over all the needed directories, extracting the values from path tuples
    for path_tuple in path_directories:

        # initialising source folder
        create_directory(path_tuple[0])
        # initialising output folder
        create_directory(path_tuple[1])

    logger.info("Directory creation complete")


def create_directory(directory_path : str):

    # adding the directory if it doesn't exist
    if not exists(directory_path):
        try:
            # Create target Directory
            mkdir(directory_path)
            logger.info("Directory created: {0} ".format(directory_path))
        except Exception:
            logger.error("During directory creation exception occured")
    else:
        logger.info("Directory already exists: {0} ".format(directory_path))


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
