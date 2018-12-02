-- check there is only one name per email in the database
select *
from members_list t1
  JOIN members_list t2
    ON t1.name = t2.name
WHERE LOWER(t1.email) != LOWER(t2.email) ;
