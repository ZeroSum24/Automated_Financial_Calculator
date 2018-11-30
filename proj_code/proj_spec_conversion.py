
import logging
from proj_code.misc_methods import set_up_logging

logger = logging.getLogger()

# Converting the name of the files to a more readable format
# Example: 6. Nov Sun Day Trip - 25%2F11%2F18.xlsx
#          -> 6. Nov Sun Day Trip - 25_11_18.csv
def name_conversion(workbook: str, logger_name=""):

    global logger
    logger = set_up_logging(logger_name)

    # updating the date values
    wkbk_updated = workbook.replace('%2F', '_')

    # renaming the file
    logger.debug("Workbook name {0}".format(workbook))
    logger.debug("Workbook name updated {0}".format(wkbk_updated))

    return wkbk_updated

"""Taking specic csv files and creating table names from them"""
def table_name_creation(csv_name: str, logger_name=""):

    global logger
    logger = set_up_logging(logger_name)

    # Creating a dictionary to store all values
    trip_info = {}

    # Doing string manipulation to extract correct values
    trip_info["No"] = int(csv_name.split('.')[0])
    trip_info["Name"] = csv_name.split('.')[1].split('-')[0][1:-1]
    trip_info["Date"] = csv_name.split('.')[1].split('-')[1][1:]

    # Manipulating values to make them more Sqlite compatible
    trip_info["Name"] = trip_info["Name"].replace(" ", "_")
    trip_info["Date"] = trip_info["Date"].replace("_", "/")

    logger.debug("Trip info: {0}".format(trip_info))

    # returned as lowered to help with databaes such as postgres
    return trip_info["Name"].lower()

"""Intention is to create database table with all the trip values"""
def create_trip_table():
    pass
