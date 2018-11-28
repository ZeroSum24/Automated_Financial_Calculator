from os import mkdir
import logging

logger = logging.getLogger()


# Create all desired directories
def create_directories(list_dir: list):

    # iterating over all the needed directories
    for dirName in list_dir:
        try:
            # Create target Directory
            mkdir(dirName)
            logger.info("Directory " , dirName ,  " Created ")
        except FileExistsError:
            logger.info("Directory " , dirName ,  " already exists")

    logger.info("Directory creation complete")
