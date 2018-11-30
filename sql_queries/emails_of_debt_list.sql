-- Outputting a list of everyone who owes money: displaying their name,
-- debt amount and trips debt was accured on

with trips as
  (SELECT *, tableoid::regclass::text AS trip_name
   FROM trips_table
   ORDER BY trip_name ),
  debt_list as
    (with debt_list as
        (select email, cast(sum(owes) as decimal(10,2) ) as owes
         from trips_table
         where paid is null and owes <> 0
         group by email )
    select names.name, debt_list.email, debt_list.owes
    from debt_list
      left join (SELECT DISTINCT(email), Min(name) as name
                 from trips_table
                 group by email) names
        on debt_list.email = names.email )
SELECT debt_list.email
from debt_list, trips
where debt_list.email = trips.email AND (trips.paid IS NULL and trips.owes <> 0)
group by debt_list.name, debt_list.email, debt_list.owes ;
