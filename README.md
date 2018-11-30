# HW_Data_Management
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

10. Added adaptability of database types and swapped to sqlalchemy to manage these

11. Need to fix appendage of non-unique values to the database
