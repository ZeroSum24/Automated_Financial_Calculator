
# Dependencies: csv, logger, os, pandas, xlrd

import csv
import logging
import os
import pandas as pd
import xlrd

from proj_code.misc_methods import set_up_logging
from proj_code.proj_spec_conversion import name_conversion

logger = logging.getLogger()


# Searching through the spreadsheets directory and converting all to csv files
def convert_all_spreadsheets(excel_fol: str, csv_fol: str, csv_sheet:str,
                                            logger_name= "", proj_spec=True):

    set_up_logging(logger_name)

    # listing all spreadsheets in directory
    spreadsheets = os.listdir(excel_fol)

    for workbook in spreadsheets:

        # getting the workbook path name for conversion
        wkbk_path = os.path.join(excel_fol, workbook)

        # creating variables for created csv file, converting into a readable csv name
        wkbk_name = os.path.basename(workbook)

        # Path conversion allowing for project specific conversions
        csv_path = os.path.join(csv_fol, wkbk_name)
        if proj_spec:
            csv_path = os.path.join(csv_fol, name_conversion(wkbk_name))

        # updating the file type to csv
        pre, ext = os.path.splitext(csv_path)
        csv_path = pre + ".csv"

        # converting to the csv from the workbook, removing null values
        csv_from_excel(workbook=wkbk_path, sheet=csv_sheet, csv_out=csv_path)
        remove_csv_null_values(csv_path=csv_path)

        logger.info("Converted {0} and stored in {1}".format(wkbk_name, csv_path))

# The xlrd module is used to read the excel and then you can use the csv module
# to create your own csv.
# https://stackoverflow.com/questions/20105118/convert-xlsx-to-csv-correctly-using-python
def csv_from_excel(workbook: str, sheet: str, csv_out: str):
    wb = xlrd.open_workbook(workbook)
    sh = wb.sheet_by_name(sheet)
    your_csv_file = open(csv_out, 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()

"""Updates any null values in the csv"""
def remove_csv_null_values(csv_path : str):

    # reads the csv from file
    current_csv = pd.read_csv(csv_path)

    # Drops all null rows in the original DataFrame with an empty space
    modified_csv = current_csv.dropna(how='all')
    # Replaces null values with NULL
    modified_csv = modified_csv.fillna("NULL")

    logger.debug("Amount of null values post-mod: {0}"
                            .format(modified_csv.isnull().sum()))
    # Saves the modified dataset to a the original CSV location
    modified_csv.to_csv(csv_path,index=False)
