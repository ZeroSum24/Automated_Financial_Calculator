
# Plan incorporate sqlite3 specific elements into csv_to_table which handles
# the columns more automatically

# SQL Server database
# https://stackoverflow.com/questions/21257899/writing-a-csv-file-into-sql-server-database-using-python

import os
import pandas as pd
import logging
from os.path import basename, join, splitext
from sys import exit
import sqlalchemy as db
from sqlalchemy_utils import database_exists, create_database

from app.app_src.utils.databasetype import DatabaseType
from app.app_src.database.db_organisation import drop_parent_table_if_existing, create_parent_table
from app.app_src.utils.misc_methods import set_up_logging
from app.app_src.utils.proj_spec_conversion import table_name_creation

logger = logging.getLogger()


def convert_to_db(path_directories: dict,
                  database_config: dict,
                  db_type: DatabaseType = DatabaseType.POSTGRES_DB,
                  file_extension: str = ".csv",
                  logger_name: str = ""):
    """
    Converting all the csv files to the database and creating a parent table for them if desired

    :param path_directories:
    :param logger_name:
    :param database_config:
    :param db_type:
    :param file_extension:
    :return:
    """

    global logger
    logger = set_up_logging(logger_name)

    db_engine_url = form_db_engine(database_config, db_type)

    # for each path_tuple convert the csv to the database
    for spreadsheet_type in path_directories:

        csv_fol = spreadsheet_type[1]
        spreadsheets_tag = path_directories.get(spreadsheet_type)
        create_parent_table_for_type = spreadsheet_type[3]

        convert_all_csv_to_table(db_engine_url, csv_fol, spreadsheets_tag, file_extension)
        # if a parent table is required, create one for the tables
        if create_parent_table_for_type:
            db_connection = init_db_connection(db_engine_url)
            drop_parent_table_if_existing(db_connection,  spreadsheets_tag, logger_name)
            table_names = convert_all_csv_to_table(db_engine_url, csv_fol, spreadsheets_tag, file_extension)
            create_parent_table(db_connection, spreadsheets_tag, table_names, logger_name)
            db_connection.close()

    logger.info("Database conversion completed")
    
    return db_engine_url


def convert_all_csv_to_table(db_engine_url: str, csv_fol: str, spreadsheets_tag: str, file_extension: str):
    """
    Converting all found csv files in given location to tables

    :param db_engine_url:
    :param csv_fol:
    :param spreadsheets_tag:
    :param file_extension:
    :return:
    """

    table_names = []

    # calling the csv to table method for each csv file
    for file in os.listdir(csv_fol):
        # getting the name of the csv file for the table
        logger.debug(file)

        # checking the file is .csv before converting
        if splitext(file)[1] == file_extension:
            # creating the name of the table with project specific code
            base_csv_name = splitext(basename(file))[0]
            table_name = table_name_creation(spreadsheets_tag, base_csv_name)
            table_names.append(table_name)

            csv_path = join(csv_fol, file)
            csv_to_table(db_engine_url, csv_path=csv_path, table_name=table_name)
        else:
            logger.debug("File skipped as not .csv {0}".format(file))

    return table_names


def csv_to_table(db_engine_url: str, csv_path: str, table_name: str):
    """
    Converting the csv to sql and updating the database with the values.
    # Connecting to the database and using the pandas method to handle conversion
    # https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_sql.html

    :param db_engine_url:
    :param csv_path:
    :param table_name:
    :return:
    """

    logger.debug("Table name: {0}".format(table_name))

    # Connecting to the database
    connection = init_db_connection(db_engine_url)

    # reads the csv from file
    csv_pd = pd.read_csv(csv_path)
    logger.debug("CSV File: {0}".format(csv_pd))

    # convert the csv to sql, appends values if table is already there
    csv_pd.to_sql(name=table_name, con=connection, if_exists='replace')


def form_db_engine(db_config: dict, db_type: DatabaseType):
    """
    Forming the appropriate engine string depending on the desired database type

    :param db_config:
    :param db_type:
    :return:
    """

    engine_url = None

    # Makes the appropriate function call depending on the given desired database value
    if db_type == db_type.SQLITE_DB:
        engine_url = 'sqlite:///{0}'.format(db_config['database_file_location'])
    elif db_type == db_type.POSTGRES_DB:
        engine_url = 'postgresql://{0}:{1}@{2}/{3}'.format(db_config['username'], db_config['password'],
                                                           db_config['host'], db_config['database_name'])

    # Create a database if it doesn't exist
    if not database_exists(engine_url):
        create_database(engine_url)

    logger.debug("Database exists {0}".format(database_exists(engine_url)))
    return engine_url


def init_db_connection(db_engine_url: str):
    """
    Initialises the database connection using an sqlalchemy engine
    :param db_engine_url:
    :return:
    """

    connection = None
    # Attempting database connection and catching any errors
    try:
        engine = db.create_engine(db_engine_url)
        connection = engine.connect()
        logger.info("Database connected, engine {0}".format(db_engine_url))
    except Exception as e:
        logger.error(e)
        # fatal error and exit
        exit("Fatal Error: {0}".format(e))

    return connection
