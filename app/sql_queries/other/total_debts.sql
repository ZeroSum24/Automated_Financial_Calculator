select SUM(dt_list.owes)
from (select DISTINCT(email), cast(sum(owes) as decimal(10,2) ) as Owes
      from trips_table
      where paid is null and owes <> 0
      group by email) dt_list ;
