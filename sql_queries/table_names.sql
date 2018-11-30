-- SELECT DISTINCT tbl_name
-- FROM sqlite_master ;

SELECT table_name FROM information_schema.tables WHERE table_schema='public' ;
