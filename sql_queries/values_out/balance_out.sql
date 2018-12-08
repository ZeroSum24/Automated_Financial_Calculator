COPY
(SELECT *
FROM balance_sheet
WHERE balance <> 0) TO STDOUT (format csv, delimiter ',') ;
