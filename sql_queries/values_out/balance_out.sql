COPY
(SELECT *
FROM balance_sheet
WHERE balance <> 0) TO STDOUT (format csv, delimiter ',') ;

-- TODO output all with csv headers
-- https://stackoverflow.com/questions/1120109/export-postgresql-table-to-csv-file-with-headings
