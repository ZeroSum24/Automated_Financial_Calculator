import logging
import os
from os.path import basename, join, splitext
import sqlalchemy as db
from sqlalchemy_utils import database_exists, create_database

from proj_code.convert_to_db import init_db_connection
from proj_code.misc_methods import set_up_logging

logger = logging.getLogger()

"""Run all the sql scripts in the folder according to folder ordering if desired"""
def run_all_sql(main_sql_folder: str, db_engine_url: str, num_ordered=True, logger_name=""):

    global logger
    logger = set_up_logging(logger_name)

    # initalise connection and sort folders
    connection = init_db_connection(db_engine_url)
    sorted_sql_folders = sorted(os.listdir(main_sql_folder))

    # run through all the folders according to order
    for sql_folder in sorted_sql_folders:

        sql_folder_path = join(main_sql_folder, sql_folder)
        if num_ordered:
            # only run folders with specifc names
            if check_folder_names(sql_folder):
                run_all_sql_fol_cmds(sql_folder_path, connection)
        else:
            run_all_sql_fol_cmds(sql_folder_path, connection)

    connection.close()
    logger.info("All sql run on the database")

"""Run all the sql commands in the current sql folder"""
def run_all_sql_fol_cmds(sql_folder: str, db_connection: db.engine.base.Connection):

    for script in os.listdir(sql_folder):
        script_path = join(sql_folder, script)

        table_name = splitext(script)[0]
        logger.info("Table name from file name: {0}".format(table_name))

        drop_table_if_existing(table_name, db_connection)
        init_from_script(script_path, db_connection)

"""Opening and reading the script before running the script on the database"""
def init_from_script(script, db_connection: db.engine.base.Connection):

    # read the script
    f = open(script)
    script_str = f.read().strip()

    # begin transation and close the script
    trans = db_connection.begin()
    db_connection.execute(script_str)

    # commit and close the transation
    trans.commit()
    trans.close()

"""If the table exists in the database it drops it from the database so it can
 be replaced with updated values"""
def drop_table_if_existing(table_name: str, db_conn: db.engine.base.Connection):

    # checks if the table exists in the database
    table_existing = db_conn.dialect.has_table(db_conn, table_name)
    logger.debug("{0} exists: {1}".format(table_name, table_existing))
    # if the parent table exists it drops the table and any linnked with it
    if table_existing:
        trans = db_conn.begin()
        # execute the command
        drop_table_cmd = 'DROP TABLE {0} ;'.format(table_name)
        db_conn.execute(drop_table_cmd)
        logger.info(drop_table_cmd)
        # commit and close the transation
        trans.commit()
        trans.close()
    else:
        logger.info("Table {0} does not exist".format(table_name))

"""Checking if the folder name has a number at the start"""
def check_folder_names(folder_name:str):

    is_folder_num_ordered = False
    name_split = basename(folder_name).split("_")

    # checking the split has worked
    if len(name_split) > 0:
        base_num = name_split[0]
        is_folder_num_ordered = str.isdigit(base_num)

    logger.info("Folder is num ordered: {0}".format(is_folder_num_ordered))
    return is_folder_num_ordered
