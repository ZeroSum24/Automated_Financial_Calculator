import logging
import os
from os.path import abspath, basename, join, splitext
from re import match
import sqlalchemy as db

from app.app_src.database.convert_to_db import init_db_connection
from app.app_src.utils.misc_methods import merge_files, set_up_logging

logger = logging.getLogger()


def run_all_sql(main_sql_folder: str, db_engine_url: str, num_ordered=True, output_folder=None, logger_name=""):
    """
    Run all the sql scripts in the folder according to folder ordering if desired

    :param main_sql_folder:
    :param db_engine_url:
    :param num_ordered:
    :param output_folder:
    :param logger_name:
    :return:
    """

    global logger
    logger = set_up_logging(logger_name)

    # initalise connection and sort folders
    connection = init_db_connection(db_engine_url)
    sorted_sql_folders = sorted(os.listdir(main_sql_folder))

    # run through all the folders according to order
    for sql_folder in sorted_sql_folders:

        sql_folder_path = join(main_sql_folder, sql_folder)

        # Only run the correct folders if number ordering is on, else run all folders
        if not num_ordered or (num_ordered and check_folder_names(sql_folder)):

            # Check if the command contents are to be outputted or just run
            if is_out_folder(sql_folder) and output_folder is not None:
                output_all_in_folder_to_csv(sql_folder_path, output_folder, connection)
            else:
                run_all_sql_fol_cmds(sql_folder_path, connection)
        else:
            logger.debug("Folder is not numbered")

    connection.close()
    logger.info("All sql run on the database")


def run_all_sql_fol_cmds(sql_folder: str, db_connection: db.engine.base.Connection):
    """
    Run all the sql commands in the current sql folder

    :param sql_folder:
    :param db_connection:
    :return:
    """

    for script in os.listdir(sql_folder):
        script_path = join(sql_folder, script)

        table_name = splitext(script)[0]
        logger.info("Table name from file name: {0}".format(table_name))

        drop_table_if_existing(table_name, db_connection)
        init_from_script(script_path, db_connection)


def init_from_script(script_path: str, db_connection: db.engine.base.Connection):
    """
    Opening and reading the script before running the script on the database

    :param script_path:
    :param db_connection:
    :return:
    """

    # read the script
    f = open(script_path)
    script_str = f.read().strip()

    # begin transation and close the script
    trans = db_connection.begin()
    db_connection.execute(script_str)

    # commit and close the transation
    trans.commit()
    trans.close()


def drop_table_if_existing(table_name: str, db_connection: db.engine.base.Connection):
    """
    If the table exists in the database it drops it from the database so it can be replaced with updated values

    :param table_name:
    :param db_connection:
    :return:
    """

    # checks if the table exists in the database
    table_existing = db_connection.dialect.has_table(db_connection, table_name)
    logger.debug("{0} exists as table: {1}".format(table_name, table_existing))
    # if the parent table exists it drops the table and any linnked with it
    if table_existing:
        trans = db_connection.begin()
        # execute the command
        drop_table_cmd = 'DROP TABLE {0} ;'.format(table_name)
        db_connection.execute(drop_table_cmd)
        logger.info(drop_table_cmd)
        # commit and close the transation
        trans.commit()
        trans.close()
    else:
        logger.info("Table {0} does not exist as a table".format(table_name))


def check_folder_names(folder_name:str):
    """
    Checking if the folder name has a number at the start

    :param folder_name:
    :return:
    """

    is_folder_num_ordered = False
    name_split = basename(folder_name).split("_")

    # checking the split has worked
    if len(name_split) > 0:
        base_num = name_split[0]
        is_folder_num_ordered = str.isdigit(base_num)

    logger.info("Folder is num ordered: {0}".format(is_folder_num_ordered))
    return is_folder_num_ordered


def output_all_in_folder_to_csv(folder_name:str, output_folder:str, db_connection: db.engine.base.Connection):
    """
    # TODO incorporate the file output regex so folders are only outputtted if they match
    # then match all folders to regex and run this function rather than init_from_script function

    Running all the commands in a given folder and outputting their results to csv
    :param folder_name:
    :param output_folder:
    :param db_connection:
    :return:
    """

    for file in os.listdir(folder_name):

        file_path = join(folder_name, file)
        output_sql_statements_to_csv(file_path, output_folder, db_connection)

    logger.info("All files output to csv")


def output_sql_statements_to_csv(script_path: str, output_folder: str, db_connection: db.engine.base.Connection):
    """
    Running all the sql statements in a given file and outputting their results to a matching csv file

    :param script_path:
    :param output_folder:
    :param db_connection:
    :return:
    """

    # read the script and split into queries
    f = open(script_path)
    script_str = f.read().strip()
    sql_queries = script_str.split("\n\n")

    # initialise output
    fin_out_file = join(output_folder, basename(script_path)[:-4] + ".csv")
    statement_output = ""

    # begin transation and close the script
    trans = db_connection.begin()

    # iterating for each sql statement in the file and updating the output
    for idx, sql_statement in enumerate(sql_queries):

        # including the sql command from script in a to csv command
        sql_statement = sql_statement.replace(" ;", "")

        # sets up the correct output file based on amount of sql queries
        if len(sql_queries) > 1:
            output_file = join(output_folder, "file{0}.csv".format(str(idx)))
        else:
            output_file = fin_out_file
        output_file = os.path.abspath(output_file)
        logger.debug(output_file)

        # initialise db method connection
        cur = db_connection.connection.cursor()
        to_csv_cmd = 'COPY ({0}) TO STDOUT WITH (format csv, HEADER, delimiter \',\') ;'.format(sql_statement)

        # writing the database output to file
        with open(output_file, 'w') as f:
            db_out = cur.copy_expert(sql=to_csv_cmd, file=f)

        logger.debug("Statement completed")

    # commit and close the transation
    trans.commit()
    trans.close()

    # merging into one file, the output of any sql file with more than one statement
    if len(sql_queries) > 1:
        files_list = list(map(lambda x: abspath(join(output_folder, "file{0}.csv".format(str(x)))),
                              range(len(sql_queries))))
        merge_files(fin_out_file, files_list)

    logger.debug("SQL File completed")


def is_out_folder(path: str, str_pattern=".+_out$"):
    """
    Checks whether a given directory matches a string pattern

    :param path:
    :param str_pattern:
    :return:
    """

    fol_path = basename(path)
    is_out = bool(match(str_pattern, fol_path))

    logger.debug("{0} is an output folder: {1}".format(fol_path, is_out))

    return is_out
