-- Outputting a list of everyone who owes money: displaying their name,
-- debt amount and trips debt was accured on
UPDATE trips_table SET name = TRIM(name), email = TRIM(LOWER(email)) ;

CREATE TABLE trip_debts as
with trips as
  (SELECT *, tableoid::regclass::text AS trip_name
   FROM trips_table
   ORDER BY trip_name ),
  debt_list as
    (with debt_list as
        (select LOWER(email) as email, cast(sum(owes) as decimal(10,2) ) as owes
         from trips_table
         where paid is null and owes <> 0
         group by email )
    select names.name, LOWER(debt_list.email) as email, debt_list.owes
    from debt_list
      left join (SELECT DISTINCT(LOWER(email)) as email, Min(name) as name
                 from trips_table
                 group by email) names
        on LOWER(debt_list.email) = LOWER(names.email) )
SELECT debt_list.name, LOWER(debt_list.email) as email,
       COALESCE(debt_list.owes, 0.0) as owes,
       string_agg(trips.trip_name, ', ') as trips
from debt_list, trips
where LOWER(debt_list.email) = LOWER(trips.email) AND (trips.paid IS NULL and trips.owes <> 0)
group by debt_list.name, debt_list.email, debt_list.owes ;
-- ) TO STDOUT (format csv, delimiter ',') ;
