# HW_Data_Management
Project to convert spreadsheets into a usable database to run database queries on the values and cut down cross-referencing time.

1. Convert the trip template forms into a bare template - [DONE]
2. Download the trip templates as .csv files into a single folder - [ERRORS]
3. Set-up a mysql server to use - [InProgress]
4. Connect to the server and run the code in the first answer
https://stackoverflow.com/questions/21257899/writing-a-csv-file-into-sql-server-database-using-python
NB: have to replace the MYTABLE with the table name (which should be the trip name)

5. Trip Table names might have to be standarised to allow import for sql queries - [DONE]
    -- done with project specific editing in a seperate library for modularity

NB: Can use sqllite to create a local database in python
https://docs.python.org/2/library/sqlite3.html

6. Update loggin in the main libary function calls so log cascading from main is option, and logging in general is optional - [DONE]
    -- Needs integration testing
    -- Logging needs high level main setup

7. Consolidate project specific code such as name_conversion and specific table creation  - [DONE]

8. Add update functionality, i.e. only download spreadsheets or update sql if spreadsheets have changed
      -- only update the ones which have

9. Remove blank/null values from the csv in conversion - [DONE]
