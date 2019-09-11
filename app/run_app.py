#!/usr/bin/env python3

import configparser

from app.app_src.database.convert_to_db import convert_to_db
from app.app_src.file_conversions.csv_to_xlsx import convert_all_csv_to_excel
from app.app_src.utils.databasetype import DatabaseType
from app.app_src.utils.misc_methods import create_directories, init_logger
from app.app_src.utils.proj_spec_conversion import path_directories
from app.app_src.database.run_sql import run_all_sql
from app.app_src.file_conversions.xlsx_to_csv import convert_all_spreadsheets

# Configuration Parser
config = configparser.ConfigParser()
config.read('../config/config.ini')
default_config = config['DEFAULT']

# Path Directories
path_directories = path_directories(config['EUHWC'])
output_folders = default_config['output_folders'].split()

# Logger set-up
logger = init_logger(logger_name=default_config['logger_name'],
                     log_path=default_config['log_path'])

if __name__ == "__main__":

    logger.info("Running main")
    # Create all needed directories
    create_directories(path_directories=path_directories,
                       output_folders=output_folders,
                       logger_name=default_config['logger_name'])

    # Download google drive spreadsheets to spreadsheets folder
    # download_all_spreadsheets(keys_location=default_config['drive_keys'],
    #                           json_storage=default_config['json_storage'],
    #                           logger_name=default_config['logger_name'])

    # Converting all spreadsheets to csv
    convert_all_spreadsheets(path_directories=path_directories,
                             logger_name=default_config['logger_name'])

    # Converting all those files into an sqlite database
    db_engine_url = convert_to_db(path_directories=path_directories,
                                  logger_name=default_config['logger_name'],
                                  db_file=default_config['db_file_location'],
                                  db_type=DatabaseType[default_config['DatabaseType']])

    # Automatically running all needed database queries
    run_all_sql(main_sql_folder=default_config['sql_folder'],
                db_engine_url=db_engine_url,
                output_folder=output_folders[1],
                logger_name=default_config['logger_name'])

    # Converting all the created csv into a xlsx file
    convert_all_csv_to_excel(source_folder=output_folders[1],
                             output_folder=output_folders[2],
                             workbook_name=default_config['output_workbook_name'],
                             logger_name=DatabaseType[default_config['DatabaseType']])

    print("Financial Calculations Completed")
