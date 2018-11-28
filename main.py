#!/usr/bin/env python3

import logging
from xlsx_to_csv import convert_all_spreadsheets

# Path Directories
excel_fol = "./Spreadsheets/"
csv_fol = "./CSV/"
csv_sheet = "To_CSV"

# Logger set-up
logger = logging.getLogger()


if __name__ == "__main__":
    convert_all_spreadsheets(excel_fol, csv_fol, csv_sheet)
