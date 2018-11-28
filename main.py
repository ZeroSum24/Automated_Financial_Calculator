#!/usr/bin/env python3

import logging
from proj_code.google_drive_download import download_all_spreadsheets
from proj_code.xlsx_to_csv import convert_all_spreadsheets

# Path Directories
excel_fol = "./Spreadsheets/"
csv_fol = "./CSV/"
csv_sheet = "To_CSV"

# drive keys and json storage
json_storage = "./json_storage/"
drive_keys = "g_drive_files_key.json"

# Logger set-up
logger = logging.getLogger()


if __name__ == "__main__":

    # Download google drive spreadsheets to spreadsheets folder
    download_all_spreadsheets(drive_keys, json_storage)

    # Converting all spreadsheets to csv
    convert_all_spreadsheets(excel_fol, csv_fol, csv_sheet)

    # Converting all those files into an sqlite database
        ## method fill

    # Running the database in terminal or asking the user options to run
    # which queries on
