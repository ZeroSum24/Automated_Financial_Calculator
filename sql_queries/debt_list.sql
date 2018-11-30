
-- https://stackoverflow.com/questions/14931001/select-from-all-tables-mysql
-- https://www.codeproject.com/Questions/385131/run-same-command-for-all-tables-in-a-databse-of-sq

-- Select DISTINCT(name), email, owes
-- from (SELECT table_name
--       FROM information_schema.tables
--       WHERE table_schema='public') tbl
-- where paid IS NULL ;

-- Create parent table and schema get all trips to inherit from this 
