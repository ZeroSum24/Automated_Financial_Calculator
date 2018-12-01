
# Plan incorporate sqlite3 specific elements into csv_to_table which handles
# the columns more automatically

# SQL Server database
# https://stackoverflow.com/questions/21257899/writing-a-csv-file-into-sql-server-database-using-python

import csv
import os
import pandas as pd
import logging
from os.path import basename, join, splitext
from sys import exit
import sqlalchemy as db
from sqlalchemy_utils import database_exists, create_database

from proj_code.db_type import db_type
from proj_code.misc_methods import set_up_logging
from proj_code.proj_spec_conversion import table_name_creation

logger = logging.getLogger()

""" Governing funcion call"""
def convert_to_db(path_directories: dict, logger_name="", db_type=db_type.POSTGRES_DB, db_file=""):

    global logger
    logger = set_up_logging(logger_name)

    db_engine_url = form_db_engine(db_file, db_type)

    # for each path_tuple convert the csv to the database
    for path_tuple in path_directories:

        csv_fol = path_tuple[1]
        spreadsheets_tag = path_directories.get(path_tuple)

        convert_all_csv_to_table(db_engine_url, csv_fol, spreadsheets_tag)


""" Converting all found csv files in given location to tables"""
def convert_all_csv_to_table(db_engine_url: str, csv_fol: str, spreadsheets_tag: str, file_extension=".csv"):

    fol_files = os.listdir(csv_fol)

    # calling the csv to table method for each csv file
    for file in fol_files:
        # getting the name of the csv file for the table
        logger.debug(file)

        # checking the file is .csv before converting
        if splitext(file)[1] == file_extension:
        # creating the name of the table with project specific code
            base_csv_name = splitext(basename(file))[0]
            csv_name = table_name_creation(spreadsheets_tag, base_csv_name)

            csv_path = join(csv_fol, file)
            csv_to_table(db_engine_url, csv_path=csv_path, table_name=csv_name)
        else:
            logger.debug("File skipped as not .csv {0}".format(file))


"""Converting the csv to sql and updating the database with the values."""
def csv_to_table(db_engine_url: str, csv_path: str, table_name: str):
    # Connecting to the database and using the pandas method to handle conversion
    # https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_sql.html

    logger.debug("Table name: {0}".format(table_name))

    # Connecting to the database
    connection = init_db_connection(db_engine_url)

    # reads the csv from file
    csv_pd = pd.read_csv(csv_path)
    logger.debug("CSV File: {0}".format(csv_pd))

    # convert the csv to sql, appends values if table is already there
    csv_pd.to_sql(name=table_name, con=connection, if_exists='replace')


"""Forming the appropriate engine string depending on the desired database type"""
def form_db_engine(db_file:str, db_type: db_type):

    engine_url = None

    # Makes the appropriate function call depending on the given desired database value
    if db_type == db_type.SQLITE_DB:
        engine_url = 'sqlite:///{0}'.format(db_file)
    elif db_type == db_type.POSTGRES_DB :
        db_name = splitext(basename(db_file))[0]
        engine_url = 'postgresql://postgres:postgres@localhost/{0}'.format(db_name)

    # Create a database if it doesn't exist
    if not database_exists(engine_url):
        create_database(engine_url)

    logger.debug("Database exists {0}".format(database_exists(engine_url)))
    return engine_url


"""Initialises the database connection using an sqlalchemy engine"""
def init_db_connection(db_engine_url: str):

    connection = None
    # Attempting database connection and catching any errors
    try:
        engine = db.create_engine(db_engine_url)
        connection = engine.connect()
        logger.info("Database connected, engine {0}".format(db_engine_url))
    except Exception as e:
        logger.error(e)
        exit("Fatal Error: {0}".format(e)) # fatal error and exit

    return connection
