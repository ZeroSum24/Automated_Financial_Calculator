from os import mkdir, remove
from os.path import basename, exists, splitext
import inspect
import logging

logger = logging.getLogger()


def create_directories(path_directories: dict, output_folders: list = list, logger_name=""):
    """
    Create all desired directories

    :param path_directories:
    :param output_folders:
    :param logger_name:
    :return:
    """

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
    if output_folders is not None:

        for folder in output_folders:
            # initialising extra folder
            create_directory(folder)
        logger.info("Extra folder creation complete")

    logger.info("Directory creation complete")


def create_directory(directory_path: str):
    """
    Creates directories using os commands

    :param directory_path:
    :return:
    """

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


def set_up_logging(logger_name: str):
    """
    Sets up consistent logging across library

    :param logger_name:
    :return:
    """

    if logger_name != "":

        # create the updated file names for the logger
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        # gets file name of method caller
        file_name = splitext(basename(module.__file__))[0]

        logger_full_name = "{0}.{1}".format(logger_name, file_name)
        # update global logger with correct name
        global logger
        logger = logging.getLogger(logger_full_name)

        logger.info("Logging was set up correctly")
    else:
        logger = logging.getLogger("")
        logger.info("Global Logging was not set up")

    return logger


def init_logger(logger_name: str, level=logging.DEBUG, log_path=None,
                logging_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"):
    """
    Initialise main app logger

    :param logger_name:
    :param level:
    :param log_path:
    :param logging_format:
    :return:
    """

    # initialise the logging object and setting the logging level
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # setting up the handler to stream or file
    handler = logging.StreamHandler()

    if log_path is not None:
        handler = logging.FileHandler(log_path)

    # Set the log level
    handler.setLevel(level)

    # add formatter to handler
    formatter = logging.Formatter(logging_format)
    handler.setFormatter(formatter)

    # attaching the handler to the logger
    logger.addHandler(handler)

    return logger


def create_file(file: str):
    """
    Creating a file if doesn't already exist
    :param file:
    """
    if not exists(file):
        open(file, "w+")


def save_text_to_file(filename: str, text: str):
    """
    Creating a file and adding all the text to it

    :param filename:
    :param text:
    :return:
    """

    # splitting the text into lines and creating txt file
    txt_lines = text.split("\n")
    f = open(filename, "w+")

    # Writing each line to the file
    for line in txt_lines:
        f.write(line)

    # closing the file
    f.close()


def merge_files(merged_file_path: str, list_of_files: list, remove_merged=True):
    """
    Python script to concatenate a list of files files into a single new file.

    :param merged_file_path:
    :param list_of_files:
    :param remove_merged:
    :return:
    """

    with open(merged_file_path, 'w') as outfile:
        for file_name in list_of_files:
            with open(file_name) as infile:
                outfile.write("{0}\n".format(infile.read()))
            # remove unneeded merged files
            if remove_merged:
                remove(file_name)


def dict_to_string(dictionary: dict):
    """
    Converting a dictionary to a string

    :param dictionary:
    :return:
    """
    item_strings = []
    # Iterates over the dictionary items
    for key, val in dictionary.items():
        dictionary[key] = str(val)
        item_str = "{0} {1}".format(key, val)
        item_strings.append(item_str)
    overall_str = ", ".join(item_strings)

    logger.debug(overall_str)
    return overall_str


def dict_equals(d1: dict, d2: dict) -> bool:
    """
    Commparing if two dictionaries are equal

    :param d1:
    :param d2:
    :return:
    """

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
