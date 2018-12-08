#!/usr/bin/env python3

import logging
from proj_code.convert_to_db import convert_to_db
from proj_code.csv_to_xlsx import convert_all_csv_to_excel
from proj_code.db_type import db_type
from proj_code.google_drive_download import download_all_spreadsheets
from proj_code.misc_methods import create_directories, init_logger
from proj_code.proj_spec_conversion import path_directories
from proj_code.run_sql import run_all_sql
from proj_code.xlsx_to_csv import convert_all_spreadsheets

# Path Directories
path_dir = path_directories()

db_file_location = "./trip_financials.db"
sql_folder = "./sql_queries/"
db_type = db_type.POSTGRES_DB

# Output folders
extra_folders = ["./Output", "./Output/csv/", "./Output/xlsx"]
output_name = "Treasury_Sheets"

# drive keys and json storage
json_storage_fol = "./json_storage/"
drive_keys = "g_drive_files_key.json"

# Logger set-up
logger_name = "SQL_Data_Convert"
logger = init_logger(logger_name, log_path="./test.log")

if __name__ == "__main__":

    logger.info("Running main")
    # Create all needed directories
    create_directories(path_directories=path_dir, extra_folders=extra_folders,
                                                    logger_name=logger_name)

    # Download google drive spreadsheets to spreadsheets folder
    # download_all_spreadsheets(keys_location=drive_keys,
                            # json_storage=json_storage, logger_name=logger_name)

    # Converting all spreadsheets to csv
    convert_all_spreadsheets(path_directories=path_dir, logger_name=logger_name)

    # Converting all those files into an sqlite database
    db_engine_url = convert_to_db(path_directories=path_dir, logger_name=logger_name,
                                     db_file=db_file_location, db_type=db_type)

    # Automatically running all needed database queries
    run_all_sql(main_sql_folder=sql_folder, db_engine_url=db_engine_url,
                        logger_name=logger_name)

    # Converting all the created csv into a xlsx file
    convert_all_csv_to_excel(source_folder=extra_folders[1], output_folder=extra_folders[2],
                                workbook_name=output_name, logger_name=logger_name)

    print("*Completed*")
