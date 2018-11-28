
# Dependencies: csv, logger, os, xlrd

import csv
import logging
import os
import xlrd

from proj_code.misc_methods import set_up_logging

logger = logging.getLogger()


# Searching through the spreadsheets directory and converting all to csv files
def convert_all_spreadsheets(excel_fol: str, csv_fol: str, csv_sheet:str, logger_name= ""):

    set_up_logging(logger_name)

    # listing all spreadsheets in directory
    spreadsheets = os.listdir(excel_fol)

    for workbook in spreadsheets:

        # getting the workbook path name for conversion
        wkbk_path = os.path.join(excel_fol, workbook)

        # creating variables for created csv file, converting into a readable csv name
        wkbk_name = os.path.basename(workbook)
        csv_path = os.path.join(csv_fol, name_conversion(wkbk_name))

        # updating the file type to csv
        pre, ext = os.path.splitext(csv_path)
        csv_path = pre + ".csv"

        # converting to the csv from the workbook
        csv_from_excel(workbook=wkbk_path, sheet=csv_sheet, csv_out=csv_path)

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

# Converting the name of the files to a more readable format
# Example: 6. Nov Sun Day Trip - 25%2F11%2F18.xlsx
#          -> 6. Nov Sun Day Trip - 25%2F11%2F18.xlsx
def name_conversion(workbook: str):

    # replacing the spaces and the date values
    wkbk_updated = workbook.replace(' ', '_')
    wkbk_updated = wkbk_updated.replace('%2F', '-')

    # renaming the file
    logger.debug("Workbook name {0}".format(workbook))
    logger.debug("Workbook name updated {0}".format(wkbk_updated))

    return wkbk_updated
