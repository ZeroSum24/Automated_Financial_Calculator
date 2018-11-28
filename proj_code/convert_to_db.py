
# Plan incorporate sqlite3 specific elements into csv_to_table which handles
# the columns more automatically

# SQL Server database
# https://stackoverflow.com/questions/21257899/writing-a-csv-file-into-sql-server-database-using-python

import csv
import os
import logging
import sqlite3
from sqlite3 import Error

logger = logging.getLogger()

""" Governing funcion call"""
def convert_to_db(db_file:str, csv_fol:str ):

    create_database_file(db_file)
    initialise_sqlite_db_connection(db_file)
    convert_all_csv_to_table(db_file, csv_fol)


""" Converting all found csv files in given location to tables"""
def convert_all_csv_to_table(db_file: str, csv_fol:str ):

    csv_files = os.listdir(csv_fol)

    # calling the csv to table method for each csv file
    for csv_file in csv_files:
        # getting the name of the csv file for the table
        csv_name = os.basename(csv_file)
        csv_to_table(db_file, csv_file=csv_file, table_name=csv_name)


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

        # creating the table with correct name and columns
        cur.execute("CREATE TABLE {0} ({1});".format(table_name, ", ".join(columns)))

        # Finding and inserting the values into the table
        query = 'INSERT INTO ' + table_name + '({0})' + ' VALUES ({1})'
        query = query.format(','.join(columns), ','.join('?' * len(columns)))
        cursor = connection.cursor()

        # Looping through each insert statement
        for data in reader:
            cursor.execute(query, data)
        # cur.executemany("INSERT INTO t (col1, col2) VALUES (?, ?);", to_db)
        # TODO command above replacement for loop?
        cursor.commit()

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

    if !os.path.exists(db_file):
        file = open(db_file,"w+")
