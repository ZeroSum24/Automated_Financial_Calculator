import logging
from os.path import basename, join, splitext
import sqlalchemy as db
from sys import exit

from proj_code.misc_methods import dict_equals, dict_to_string, set_up_logging
from proj_code.proj_spec_conversion import table_name_creation

logger = logging.getLogger()


"""If the parent exists in the database it drops it from the database so it can
 be replaced with updated values"""
def drop_parent_table_if_existing(db_conn: db.engine.base.Connection, spreadsheets_tag: str, logger_name=""):

    # Set up logging
    global logger
    logger = set_up_logging(logger_name)

    # checks if the parent table exists in the database
    parent_name = "{0}_table".format(spreadsheets_tag)
    parent_existing = db_conn.dialect.has_table(db_conn, parent_name)

    # if the parent table exists it drops the table and any linnked with it
    if parent_existing:
        trans = db_conn.begin()
        # execute the command
        drop_table_cmd = 'DROP TABLE {0} CASCADE;'.format(parent_name)
        db_conn.execute(drop_table_cmd)
        logger.info(drop_table_cmd)
        # commit and close the transation
        trans.commit()
        trans.close()
    else:
        logger.info("Parent table {0} does not exist".format(parent_name))


"""Creating a parent table in the database for all the tables of the same type"""
def create_parent_table(db_conn: db.engine.base.Connection, spreadsheets_tag: str, table_names: list, logger_name=""):

    # Set up logging
    global logger
    logger = set_up_logging(logger_name)

    # checks if the parent table exists in the database
    parent_name = "{0}_table".format(spreadsheets_tag)
    parent_existing = db_conn.dialect.has_table(db_conn, parent_name)

    # use the spreadsheets_tag to make a parent name i.e. trips_table
    col_datatypes = get_parent_col_datatypes(db_conn, table_names, spreadsheets_tag)

    # create the parent table and add tables to parent
    create_db_table(db_conn, parent_name, col_datatypes)
    add_tables_to_parent(db_conn, table_names, parent_name)


"""Creates the parent table in the database"""
def create_db_table(db_conn: db.engine.base.Connection, table_name: str, column_datatypes: str):

    # runs create table command in the database
    create_table_cmd = "CREATE TABLE {0} ( {1} );".format(table_name, column_datatypes)

    # Begin transaction
    trans = db_conn.begin()
    db_conn.execute(create_table_cmd)
    logger.info(create_table_cmd)
    trans.commit()
    trans.close()


"""Adding all the tables to the parent table"""
def add_tables_to_parent(db_conn: db.engine.base.Connection, table_names: list, parent_name: str):

    for table_name in table_names:

        # Begin transaction
        trans = db_conn.begin()
        # sql command to alter table to inherit from parent
        add_to_parent_cmd = 'ALTER TABLE {0} INHERIT {1} ;'.format(table_name, parent_name)
        db_conn.execute(add_to_parent_cmd)

        logger.info(add_to_parent_cmd)
        logger.info("Table {0} added to parent {1}".format(table_name, parent_name))

        trans.commit()
        trans.close()


"""Create trips_table using the schema from one of the trips"""
def get_parent_col_datatypes(db_conn: db.engine.base.Connection, table_names: list, spreadsheets_tag: str):

    # getting the database metadata to check the table values
    db_metadata = db.MetaData(bind=db_conn, reflect=db_conn)
    tables_details = get_table_colmn_details(db_metadata, table_names)
    tables_columns = list(tables_details.values())
    column_types = dict_to_string(tables_columns[0])

    # If the tables don't have the same types log an error message and close the program
    if not check_all_col_datatypes_same(tables_columns, column_types):

        error_message = " ".join(["Remote database is inconsistent with the",
                         "application set-up. The {0} tables do not all have".format(spreadsheets_tag),
                         "the same column datatypes."])
        logger.error(error_message)
        exit("Fatal Error: {0}".format(error_message)) # fatal error and exit

    return column_types


"""Checking the schene of all the table names is the same"""
def check_all_col_datatypes_same(tables_columns: list, column_types: str):

    logger.debug(tables_columns)
    # converting each dictionary to a string and checking they all match
    all_datatypes_same = all(column_types==dict_to_string(cols_types) for cols_types in tables_columns)

    logger.debug("Check_all_cols_string: {0}".format(column_types))
    return all_datatypes_same


"""Getting the column details (name and type) for each table with the same table type"""
def get_table_colmn_details(db_metadata: db.MetaData, table_names: list):

    tables_details = {}
    table_names_set = set(table_names)

    # looping over every table, building a dictionary of the tables and columns
    for table in db_metadata.tables.values():

        # checking the remote table is in the applications table list
        if table.name in table_names_set:
            # building a dictionary of the columns and types
            table_columns = {}
            for c in table.columns.values():
                table_columns[c.name] = c.type

            # adding the column dictionary to the table dictionary
            tables_details[table.name] = table_columns
        else:
            logger.debug("Passing {} from details check".format(table.name))

    logger.debug(tables_details)
    return tables_details
