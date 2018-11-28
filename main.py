#!/usr/bin/env python3

import logging
from proj_code.convert_to_db import convert_to_db
from proj_code.google_drive_download import download_all_spreadsheets
from proj_code.misc_methods import create_directories
from proj_code.xlsx_to_csv import convert_all_spreadsheets

# Path Directories
excel_fol = "./Spreadsheets/"
csv_fol = "./CSV/"
csv_sheet = "To_CSV"
db_file_location = "./sqlitedb.db"

# drive keys and json storage
json_storage_fol = "./json_storage/"
drive_keys = "g_drive_files_key.json"

# Logger set-up
logger = logging.getLogger()


if __name__ == "__main__":

    # Create all needed directories
    create_directories([excel_fol, csv_fol, json_storage_fol])

    # Download google drive spreadsheets to spreadsheets folder
    # download_all_spreadsheets(drive_keys, json_storage)

    # Converting all spreadsheets to csv
    convert_all_spreadsheets(excel_fol, csv_fol, csv_sheet)

    # Converting all those files into an sqlite database
    # convert_to_db(db_file=db_file_location, csv_fol=csv_fol)

    # Running the database in terminal or asking the user options to run
    # which queries on

    print("*Completed*")
