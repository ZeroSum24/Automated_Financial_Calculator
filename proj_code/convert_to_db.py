
# Plan incorporate sqlite3 specific elements into csv_to_table which handles
# the columns more automatically

# SQL Server database
# https://stackoverflow.com/questions/21257899/writing-a-csv-file-into-sql-server-database-using-python

import csv
import os
import pandas as pd
import logging
import sqlite3
from sqlite3 import Error
from os.path import basename, join, splitext

from proj_code.misc_methods import set_up_logging
from proj_code.proj_spec_conversion import table_name_creation

logger = logging.getLogger()

""" Governing funcion call"""
def convert_to_db(db_file:str, csv_fol:str, logger_name="", proj_spec=True):

    global logger
    logger = set_up_logging(logger_name)

    create_database_file(db_file)
    initialise_sqlite_db_connection(db_file)
    convert_all_csv_to_table(db_file, csv_fol, proj_spec)


""" Converting all found csv files in given location to tables"""
def convert_all_csv_to_table(db_file: str, csv_fol: str, proj_spec):

    fol_files = os.listdir(csv_fol)

    # calling the csv to table method for each csv file
    for file in fol_files:
        # getting the name of the csv file for the table
        logger.debug(file)

        # checking the file is .csv before converting
        if splitext(file)[1] == ".csv":
        # creating the name of the table with project specific code
            csv_name = splitext(basename(file))[0]
            if proj_spec:
                csv_name = table_name_creation(csv_name)

            csv_path = join(csv_fol, file)
            csv_to_table(db_file, csv_path=csv_path, table_name=csv_name)
        else:
            logger.debug("File skipped as not .csv {0}".format(file))


"""Converting the csv to sql and updating the database with the values."""
def csv_to_table(db_file: str, csv_path: str, table_name: str):
    # Connecting to the database and using the pandas method to handle conversion
    # https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_sql.html

    logger.debug("Table name: {0}".format(table_name))

    # Connecting to the database
    connection = sqlite3.connect(db_file)

    # reads the csv from file
    csv_pd = pd.read_csv(csv_path)
    logger.debug("CSV File: {0}".format(csv_pd))

    # convert the csv to sql, appends values if table is already there
    csv_pd.to_sql(name=table_name, con=connection, if_exists='append')


def initialise_sqlite_db_connection(db_file: str):
    # Tutorial for initialising database
    # http://www.sqlitetutorial.net/sqlite-python/creating-database/
    """ create a database connection to a SQLite database """

    try:
        conn = sqlite3.connect(db_file)
        logger.info(sqlite3.version)
    except Error as e:
        logger.error(e)
    finally:
        conn.close()

def create_database_file(db_file: str):
    """Creating the database file if none already exist"""

    if not os.path.exists(db_file):
        file = open(db_file,"w+")
