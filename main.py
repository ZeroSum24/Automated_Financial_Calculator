#!/usr/bin/env python3

import logging
from proj_code.convert_to_db import convert_to_db
from proj_code.google_drive_download import download_all_spreadsheets
from proj_code.misc_methods import create_directories, init_logger
from proj_code.xlsx_to_csv import convert_all_spreadsheets

# Path Directories
excel_fol = "./Spreadsheets/"
csv_fol = "./CSV/"
csv_sheet = "To_CSV"
db_file_location = "./trip_financials.db"

# drive keys and json storage
json_storage_fol = "./json_storage/"
drive_keys = "g_drive_files_key.json"

# Logger set-up
logger_name = "SQL_Data_Convert"
logger = init_logger(logger_name, log_path="./test.log")

if __name__ == "__main__":

    logger.info("Running main")
    # Create all needed directories
    create_directories(list_dir=[excel_fol, csv_fol, json_storage_fol],
                            logger_name=logger_name)

    # Download google drive spreadsheets to spreadsheets folder
    # download_all_spreadsheets(keys_location=drive_keys,
                            # json_storage=json_storage, logger_name=logger_name)

    # Converting all spreadsheets to csv
    convert_all_spreadsheets(excel_fol=excel_fol, csv_fol=csv_fol,
                                csv_sheet=csv_sheet, logger_name=logger_name)

    # Converting all those files into an sqlite database
    convert_to_db(db_file=db_file_location, csv_fol=csv_fol,
                                    logger_name=logger_name)

    # Running the database in terminal or asking the user options to run
    # which queries on

    print("*Completed*")
