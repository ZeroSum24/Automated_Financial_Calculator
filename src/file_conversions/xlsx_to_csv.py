
# Dependencies: csv, logger, os, pandas, xlrd

import csv
import logging
import os
import pandas as pd
import xlrd
from os.path import splitext

from src.utils.misc_methods import set_up_logging
from src.utils.proj_spec_conversion import csv_name_creation

logger = logging.getLogger()


def convert_all_spreadsheets(path_directories: dict, logger_name= ""):
    """
    Converting all spreadsheets for each tuple in the path directory

    :param path_directories:
    :param logger_name:
    :return:
    """

    global logger
    logger = set_up_logging(logger_name)

    for spreadsheet_type in path_directories:

        source_fol = spreadsheet_type[0]
        output_fol = spreadsheet_type[1]
        conversion_sheet = spreadsheet_type[2]
        spreadsheets_tag = path_directories.get(spreadsheet_type)

        convert_all_spreadsheets_in_folder(source_fol, output_fol, conversion_sheet, spreadsheets_tag)

    logger.info("All spreadsheets converted across all folders")


def convert_all_spreadsheets_in_folder(source_fol: str, output_fol: str, conversion_sheet: str, spreadsheets_tag: str):
    """
    Searching through the spreadsheets directory and converting all to csv files

    :param source_fol:
    :param output_fol:
    :param conversion_sheet:
    :param spreadsheets_tag:
    :return:
    """

    # listing all spreadsheets in directory
    spreadsheets_fol = os.listdir(source_fol)

    for file in spreadsheets_fol:

        # checking the file is .xlsx before converting
        if splitext(file)[1] == ".xlsx":

            # calculating the file paths for each log book
            wkbk_path, csv_path = calculating_file_paths(source_fol, file, output_fol, spreadsheets_tag)

            # converting to the csv from the workbook, removing null values
            csv_from_excel(workbook=wkbk_path, sheet=conversion_sheet, csv_out=csv_path)
            update_csv(csv_path=csv_path)

            logger.debug("Conversion to .csv completed {0}".format(file))

        else:
            logger.debug("File skipped as not .xlsx {0}".format(file))

    logger.info("All spreadsheets converted in folder: {0}".format(source_fol))


def calculating_file_paths(folder_loc: str, file_name: str, desired_fol: str, spreadsheets_tag: str, file_extension=".csv"):
    """
    Method to calculate the file paths when moving and updating a file to a new folder, added for readability

    :param folder_loc:
    :param file_name:
    :param desired_fol:
    :param spreadsheets_tag:
    :param file_extension:
    :return:
    """

    # getting the workbook path name for conversion
    file_path = os.path.join(folder_loc, file_name)

    # creating variables for created new file location, converting into a readable name
    file_name = os.path.basename(file_name)
    # Path conversion allowing for project specific conversions
    file_to_fol_path = os.path.join(desired_fol, csv_name_creation(spreadsheets_tag, file_name))

    # updating the file type to to desired
    pre, ext = os.path.splitext(file_to_fol_path)
    file_to_fol_path = pre + file_extension

    logger.info("File path {0} and new file path {1} calculated"
            .format(file_path, file_to_fol_path))

    return (file_path, file_to_fol_path)


def csv_from_excel(workbook: str, sheet: str, csv_out: str):
    """
    The xlrd module is used to read the excel and then you can use the csv module to create your own csv.
    Credit to: https://stackoverflow.com/questions/20105118/convert-xlsx-to-csv-correctly-using-python

    :param workbook:
    :param sheet:
    :param csv_out:
    :return:
    """
    wb = xlrd.open_workbook(workbook)
    sh = wb.sheet_by_name(sheet)
    your_csv_file = open(csv_out, 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()


def update_csv(csv_path: str):
    """
    Loads the current csv file into a dataframe and runs methods to update and filter values

    :param csv_path:
    :return:
    """

    # reads the csv from file
    current_csv = pd.read_csv(csv_path)

    modified_df = remove_csv_null_values(dataframe=current_csv)
    modified_df = fix_csv_columns(dataframe=modified_df)

    # Saves the modified dataset to a the original CSV location
    modified_df.to_csv(csv_path,index=False)


def remove_csv_null_values(dataframe: pd.DataFrame):
    """
    Updates any null values in the dataframe

    :param dataframe:
    :return:
    """

    # Drops all null rows in the original DataFrame with an empty space
    modified_df = dataframe.dropna(how='all')
    # Replaces null values with NULL
    modified_df = modified_df.fillna("NULL")

    logger.debug("Amount of null values post-mod: {0}"
                            .format(modified_df.isnull().sum()))

    return modified_df


def fix_csv_columns(dataframe: pd.DataFrame):
    """
    Method to fix the dataframe columns to a more readable style

    :param dataframe:
    :return:
    """

    # performing updates to the column name style style
    dataframe.columns = dataframe.columns.str.strip().str.lower()
    dataframe.columns = dataframe.columns.str.replace(' ', '_')
    dataframe.columns = dataframe.columns.str.replace('(', '')
    dataframe.columns = dataframe.columns.str.replace(')', '')

    return dataframe
