
# Plan incorporate sqlite3 specific elements into csv_to_table which handles
# the columns more automatically

# SQL Server database
# https://stackoverflow.com/questions/21257899/writing-a-csv-file-into-sql-server-database-using-python

import csv
import os
import logging
import sqlite3
from sqlite3 import Error
from os.path import basename, join, splitext

from proj_code.misc_methods import set_up_logging
from proj_code.proj_spec_conversion import table_name_creation

logger = logging.getLogger()

""" Governing funcion call"""
def convert_to_db(db_file:str, csv_fol:str, logger_name="", proj_spec=True):

    set_up_logging(logger_name)
    create_database_file(db_file)
    initialise_sqlite_db_connection(db_file)
    convert_all_csv_to_table(db_file, csv_fol, proj_spec)


""" Converting all found csv files in given location to tables"""
def convert_all_csv_to_table(db_file: str, csv_fol: str, proj_spec):

    csv_files = os.listdir(csv_fol)

    # calling the csv to table method for each csv file
    for csv_file in csv_files:
        # getting the name of the csv file for the table
        logger.debug(csv_file)

        # creating the name of the table with project specific code
        csv_name = splitext(basename(csv_file))[0]
        if proj_spec:
            csv_name = table_name_creation(csv_name)

        csv_path = join(csv_fol, csv_file)
        csv_to_table(db_file, csv_file=csv_path, table_name=csv_name)


"""Building the query dynamically to ensure the number of placeholders
    matches your table and CSV file format."""
def csv_to_table(db_file: str, csv_file: str, table_name: str):

    connection = sqlite3.connect(db_file)

    # Reading the csv_file and creating the table
    with open (csv_file, 'r') as f:
        # reading the columns from file
        reader = csv.reader(f)
        columns = next(reader)
        cur = connection.cursor()

        logger.debug("{0}\n{1}".format(table_name, columns))
        # creating the table with correct name and columns
        cur.execute("CREATE TABLE {0} ({1});".format(table_name, ','.join(columns)))

        # Finding and inserting the values into the table
        query = 'INSERT INTO {0} ({1}) VALUES ({2})'
        query = query.format(table_name, ','.join(columns), ','.join('?' * len(columns)))
        cursor = connection.cursor()

        # Looping through each insert statement
        for data in reader:
            print(query, data)
            cursor.execute(query, data)
        # cur.executemany("INSERT INTO t (col1, col2) VALUES (?, ?);", to_db)
        # TODO command above replacement for loop?
        connection.commit()
        connection.close()

# https://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python
# def sqlite_specific_convert():
#
#     con = sqlite3.connect(":memory:")
#     cur = con.cursor()
#     cur.execute("CREATE TABLE t (col1, col2);") # use your column names here
#
#     with open('data.csv','rb') as fin: # `with` statement available in 2.5+
#         # csv.DictReader uses first line in file for column headings by default
#         dr = csv.DictReader(fin) # comma is default delimiter
#         to_db = [(i['col1'], i['col2']) for i in dr]
#
#     con.commit()
#     con.close()

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
