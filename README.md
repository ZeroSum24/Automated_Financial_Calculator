# EUHWC Automated Financial Calculator
Project to convert spreadsheets into a usable database to run database queries on the values and cut down cross-referencing time.

1. Downloading the spreadsheet files from google drive into a single folder - [InProgress]
2. Convert the spreadsheets into a sql convertable format (.csv) - [DONE]
    -- includes filtering out null values csv values - [DONE]
3. Standardising file names for ease of queries - [DONE]
4. Project specific code consolidated into a discrete module - [DONE]
4. Set-up a mysql database (sqlite3) to use - [DONE]
https://docs.python.org/2/library/sqlite3.html
5. Implemented full application logging, which also for the reuse of modules - [DONE]
    -- includes application level logging set up, in a standarised  format

6. Add update functionality, i.e. only download spreadsheets or update sql if spreadsheets have changed
      -- sql is only updated if changed - [DONE]
      -- only downloaded if changed - [TODO]
7. Better/more consistent code commenting such as in the numpy format - [TODO]
8. Write sql queries on the database - [TODO]
9. Should add a config file to handle config set-up like db type including password and user values
 -- https://docs.python.org/3/library/configparser.html
  -- use this to remove ubiquitous hard coded variables into a config file

10. Added adaptability of database types and swapped to sqlalchemy to manage these - [DONE]
  -- To resolve problem with column altering, don't change [enter values] boxes of sheets until first payment
12. Added ablity to handle multiple types of sheets with unique name conversion happening with each - [DONE]
      -- update proj_spec_methods path directories to add a new type of spreadsheet to be added
      11. Need to fix appendage of non-unique values to the database - [DONE]
13. Added ability for a parent method to be automatically built from all sheets in a specific folder to allow queries to be run on all
    i.e. of the same "type" - [DONE] N.B only works if all sheets have the same columns and types
14. Application now runs queries in the sql_queries folder automatically - [DONE]
15. Wrote all the queries needed for the application - [DONE]
16. Need to output the out set of queries to csv and make this automatic as part of the appliation - [DONE]
17. update create folders method with the ability to create the sql folder, the output folder and the json storage folder - [DONE]


18. make csv output command based on folder name last four letters being '\_out' - [DONE]
19. add program part that converts csv to back to xlsx for readability in conversion - [DONE]
https://stackoverflow.com/questions/17684610/python-convert-csv-to-xlsx

20. Added budget calculation query based on labelled expenses data - [DONE]
  -- add trip income and label refund data for trips - [DONE]
