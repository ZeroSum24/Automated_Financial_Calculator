
import logging
from proj_code.misc_methods import set_up_logging

logger = logging.getLogger()

"""Setting up the desired path directories for each type of file to be converted"""
def path_directories():

    # Setting up the correct extensions
    excel_fol = "./Spreadsheets/"
    csv_fol = "./CSV/"
    trips_ext = "trips/"
    finances_ext = "finances/"
    format = "{0}{1}"

    # Initalising the specific sheet names for the conversions
    trips_sheet = "To_CSV"
    finances_sheet = "Form Responses 1"

    # Setting up the trips
    trip_fol = format.format(excel_fol, trips_ext)
    trip_csv_fol = format.format(csv_fol, trips_ext)

    # Setting up the finances
    finances_fol = format.format(excel_fol, finances_ext)
    finances_csv_fol = format.format(csv_fol, finances_ext)

    # Creating a dictionary of the tuples of the desired paths with tags
    path_dict = {(trip_fol, trip_csv_fol, trips_sheet): "trips" , (finances_fol, finances_csv_fol, finances_sheet): "finances"}

    return path_dict

def csv_name_creation(workbook_tag: str, workbook: str, logger_name=""):

    # Set up logging
    global logger
    logger = set_up_logging(logger_name)

    # If the workbook corresponds with a tag then run the appropriate csv name
    # conversion on that workbook
    if workbook_tag == "trips":
        workbook = create_trips_csv_name(workbook)
    elif workbook_tag == "finances":
        workbook = create_finances_csv_name(workbook)

    # return the updated or default workbook
    return workbook

# Converting the name of the trip files to a more readable format
# Example: 6. Nov Sun Day Trip - 25%2F11%2F18.xlsx
#          -> 6. Nov Sun Day Trip - 25_11_18.csv
def create_trips_csv_name(workbook: str):

    # updating the date values
    wkbk_updated = workbook.replace('%2F', '_')

    # renaming the file
    logger.debug("Workbook name {0}".format(workbook))
    logger.debug("Workbook name updated {0}".format(wkbk_updated))

    return wkbk_updated

# Converting the name of the trip files to a more readable format
# Example: 6. Nov Sun Day Trip - 25%2F11%2F18.xlsx
#          -> 6. Nov Sun Day Trip - 25_11_18.csv
def create_finances_csv_name(workbook:str):
    pass



"""Taking specic csv files and creating table names from them"""
def table_name_creation(spreadsheets_tag: str, csv_name: str, logger_name=""):

    # Set up logging
    global logger
    logger = set_up_logging(logger_name)

    # If the workbook corresponds with a tag then run the appropriate table name
    # conversion on that workbook
    if spreadsheets_tag == "trips":
        workbook = create_trips_table_name(csv_name)
    elif spreadsheets_tag == "finances":
        workbook = create_finances_table_name(csv_name)

    return csv_name

def create_trips_table_name(csv_name: str):
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

def create_finances_table_name(csv_name: str):
    pass

"""Intention is to create database table with all the trip values"""
def create_trip_table():
    pass
