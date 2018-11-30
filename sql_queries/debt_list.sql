
-- https://stackoverflow.com/questions/14931001/select-from-all-tables-mysql

select DISTINCT(tbl."Name"), tbl."Email", tbl."Owes"
from (SELECT table_name
      FROM information_schema.tables
      WHERE table_schema='public') tbl
where tbl."Paid" IS NULL ;
