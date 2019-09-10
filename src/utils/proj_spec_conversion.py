
import logging

from src.utils.misc_methods import set_up_logging

logger = logging.getLogger()


def path_directories(path_dirs: dict):
    """
    Setting up the desired path directories for each type of file to be converted
    :return:
    """
    # Setting up the finances
    trips_tuple = (path_dirs['trips_path'], path_dirs['trips_csv_folder'], path_dirs['trips_sheet_tab'],
                   path_dirs['trips_create_parent_table']  == "True", path_dirs['trips_name'])
    finances_tuple = (path_dirs['finances_path'], path_dirs['finances_csv_folder'], path_dirs['finances_sheet_tab'],
                      path_dirs['finances_create_parent_table'] == "True", path_dirs['finances_name'])

    # Creating a dictionary of the tuples of the desired paths with tags
    path_dict = {trips_tuple: path_dirs['trips_name'], finances_tuple: path_dirs['finances_name']}

    return path_dict


def csv_name_creation(workbook_tag: str, workbook_name: str, logger_name=""):
    """

    :param workbook_tag:
    :param workbook_name:
    :param logger_name:
    :return:
    """

    # Set up logging
    global logger
    logger = set_up_logging(logger_name)

    # If the workbook corresponds with a tag then run the appropriate csv name
    # conversion on that workbook
    if workbook_tag == 'trips':
        workbook_name = create_trips_csv_name(workbook_name)
    elif workbook_tag == 'finances':
        workbook_name = create_finances_csv_name(workbook_name)

    # return the updated or default workbook
    return workbook_name


def create_trips_csv_name(workbook_name: str):
    """
    Getting a readable csv file name from the finances spreadsheets
    Example: 6. Nov Sun Day Trip - 25%2F11%2F18.xlsx
              -> 6._Nov_Sun_Day_Trip_-_25?11?18.csv
    :param workbook_name:
    :return:
    """

    # updating the date values
    workbook_name = workbook_name.replace('%2F', '?')
    workbook_name = workbook_name.replace(' ', '_')

    # renaming the file
    logger.debug("Workbook name {0}".format(workbook_name))
    logger.debug("Workbook name updated {0}".format(workbook_name))

    return workbook_name


def create_finances_csv_name(workbook_name: str):
    """
    Getting a readable csv file name from the finances spreadsheets
    Example: EUHWC - Expense Claims (Responses)
            EUHWC_-_Expense_Claims_(Responses)
    :param workbook_name:
    :return:
    """

    workbook_name = workbook_name.replace(" ", "_")
    return workbook_name


def table_name_creation(spreadsheets_tag: str, csv_name: str, logger_name=""):
    """
    Taking specic csv files and creating table names from them
    :param spreadsheets_tag:
    :param csv_name:
    :param logger_name:
    :return:
    """

    # Set up logging
    global logger
    logger = set_up_logging(logger_name)

    # If the workbook corresponds with a tag then run the appropriate table name conversion on that workbook
    if spreadsheets_tag == 'trips':
        csv_name = create_trips_table_name(csv_name)
    elif spreadsheets_tag == 'finances':
        csv_name = create_finances_table_name(csv_name)

    return csv_name


def create_trips_table_name(csv_name: str):
    """
    Getting a readable table name from the trips csv
    Example: 6._Nov_Sun_Day_Trip_-_25?11?18.csv
                -> nov_sun_day_trip
    :param csv_name:
    :return:
    """
    # Creating a dictionary to store all values
    trip_info = dict()

    # Doing string manipulation to extract correct values
    trip_info["No"] = int(csv_name.split('.')[0])
    trip_info["Name"] = csv_name.split('.')[1].split('-')[0][1:-1]
    trip_info["Date"] = csv_name.split('.')[1].split('-')[1][1:]

    # Manipulating values to make them more Sqlite compatible
    trip_info["Date"] = trip_info["Date"].replace("?", "/")

    logger.debug("Trip info: {0}".format(trip_info))

    # returned as lowered to help with databases such as postgres
    return trip_info["Name"].lower()


def create_finances_table_name(csv_name: str):
    """
    Getting a readable table name from the finances csv
    Example: EUHWC_-_Expense_Claims_(Responses)
            expenses
    :param csv_name:
    :return:
    """

    # table replacements
    table_name = csv_name.split("_-_")[1]
    table_name = table_name.split("_(")[0]
    table_name = table_name.split("_")[0]
    table_name = "{0}s".format(table_name)

    # returned as lowered to help with databases such as postgres
    return table_name.lower()


def create_trip_table():
    """
    Intention is to create database table with all the trip values
    :return:
    """
    pass
