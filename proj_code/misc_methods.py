from os import mkdir
from os.path import basename, exists, splitext
import inspect
import logging

logger = logging.getLogger()

# Create all desired directories
def create_directories(path_directories: dict, extra_folders = [], logger_name=""):

    # setting up logging
    global logger
    logger = set_up_logging(logger_name)

    # iterating over all the needed directories, extracting the values from path tuples
    for path_tuple in path_directories:

        # initialising source folder
        create_directory(path_tuple[0])
        # initialising output folder
        create_directory(path_tuple[1])

    logger.info("Path directory creation complete")

    # if there are extra folders, loop through and create them
    if extra_folders is not None:

        for folder in extra_folders:
            # initialising extra folder
            create_directory(folder)
        logger.info("Extra folder creation complete")

    logger.info("Directory creation complete")


"""Creates directories using os commands"""
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

"""Converting a dictionary to a string"""
def dict_to_string(dict: dict):

    item_strings = []
    # Iterates over the dictionary items
    for key, val in dict.items():
        dict[key] = str(val)
        item_str = "{0} {1}".format(key, val)
        item_strings.append(item_str)
    overall_str = ", ".join(item_strings)

    logger.debug(overall_str)
    return overall_str

# Commparing if two dictionaries are equal
def dict_equals(d1, d2):

    dict_equal = False

    # converting the dictionary keys to a set
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())

    # building a set of keys for which all the values match
    intersect_keys = d1_keys.intersection(d2_keys)
    same_values = set(o for o in intersect_keys if d1[o] == d2[o])

    if len(same_values) == len(d1_keys) and len(same_values) == len(d2_keys):
        dict_equal = True

    return dict_equal
