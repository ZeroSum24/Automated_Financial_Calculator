
# Dependencies: csv, logger, os, pandas, xlrd
import csv
import glob
import logging
import os
from xlsxwriter.workbook import Workbook

from os.path import join, splitext

from proj_code.misc_methods import set_up_logging
from proj_code.proj_spec_conversion import csv_name_creation

logger = logging.getLogger()

""" Converts all csv files in a folder to excel workbooks. If a workbook_name is
given it adds all sheets to be to a single workbook, else it creates a new
workbook per csv sheet."""
def convert_all_csv_to_excel(source_folder: str, output_folder: str, workbook_name="", logger_name=""):

        # set up logging
        global logger
        logger = set_up_logging(logger_name)

        if workbook_name != "":
            convert_all_csv_to_one_excel(source_folder, output_folder, workbook_name)
        else:
            convert_all_csv_to_multiple_excel(source_folder, output_folder)

        logger.info("Convert all function call completed")

"""Converting all the csv to multiple excel files with the same name"""
def convert_all_csv_to_multiple_excel(source_folder: str, output_folder: str):

        # listing all spreadsheets in directory
        csv_fol = os.listdir(source_folder)

        for file in csv_fol:
            # checking the file is .csv before converting
            if splitext(file)[1] == ".csv":
                # calculating the file paths for each log book
                csv_path, wkbk_path, sheet_name = calculating_file_paths(source_folder, file, output_folder)
                # converting to the csv from the workbook, removing null values
                workbook = Workbook(wkbk_path)
                csv_to_excel_workbook(csv_file=csv_path, workbook=workbook, sheet_name=sheet_name)
                workbook.close()
                logger.debug("Conversion to .xlsx completed {0}".format(file))
            else:
                logger.debug("File skipped as not .xlsx {0}".format(file))
        logger.info("All csv converted in folder: {0}".format(source_folder))


"""Converting all the csv to one excel files with the given name"""
def convert_all_csv_to_one_excel(source_folder: str, output_folder: str, workbook_name: str):

        # listing all spreadsheets in directory
        csv_fol = os.listdir(source_folder)

        # calculating the path of the workbook
        workbook_path = os.path.join(output_folder, workbook_name + ".xlsx")
        workbook = Workbook(workbook_path)

        for file in csv_fol:
            # checking the file is .csv before converting
            if splitext(file)[1] == ".csv":

                # calculating the file paths for each log book
                csv_path, _, sheet_name = calculating_file_paths(source_folder, file, output_folder, workbook_name)
                # converting to the csv from the workbook, removing null values
                csv_to_excel_workbook(csv_file=csv_path, workbook=workbook, sheet_name=sheet_name)
                logger.debug("Conversion to .xlsx completed {0}".format(file))
            else:
                logger.debug("File skipped as not .xlsx {0}".format(file))

        # close workbook file
        workbook.close()
        logger.info("All csv converted in folder: {0}".format(source_folder))


"""Method to calculate the file paths when moving and updating
  a file to a new folder, added for readability"""
def calculating_file_paths(folder_loc: str, file_name: str, desired_fol: str, workbook_name="", file_extension=".xlsx"):

        # getting the workbook path name for conversion
        file_path = os.path.join(folder_loc, file_name)
        # creating variables for created new file location, converting into a readable name
        file_name = os.path.basename(file_name)

        # folder path creation depending on multiple or not
        if workbook_name == "":
            file_to_fol_path = os.path.join(desired_fol, file_name[:-4] + file_extension)
            sheet_name = ""
        else:
            file_to_fol_path = os.path.join(desired_fol, workbook_name + file_extension)
            sheet_name = file_name[:-4]

        # updating the file type to to desired
        pre, ext = os.path.splitext(file_to_fol_path)
        file_to_fol_path = pre + file_extension
        logger.info("File path {0} and new file path {1} calculated"
                .format(file_path, file_to_fol_path))

        return (file_path, file_to_fol_path, sheet_name)

# Converts a csv file into a excel workbook
# https://stackoverflow.com/questions/17684610/python-convert-csv-to-xlsx
"""Creates one overall workbook and adds a new sheet for each file"""
def csv_to_excel_workbook(csv_file: str, workbook: Workbook, sheet_name: str):

    # Workbook path includes the name of the sheet
    worksheet = workbook.add_worksheet(name=sheet_name)

    # instantiating each workbook with unique path
    with open(csv_file, 'rt', encoding='utf8') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                worksheet.write(r, c, col)
