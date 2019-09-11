CREATE TABLE expenses_owed as
with expenses_list as
    (with expenses_list as
      (SELECT LOWER(email_address) as email, CAST(SUM(total_amount_claimed_£) as decimal(10,2)) AS owed
       FROM expenses
       WHERE paid IS null
       GROUP BY email)
    select names.name, expenses_list.email, expenses_list.owed
    from expenses_list
      left join (SELECT DISTINCT(LOWER(email_address)) as email, Min(name) as name
                 from expenses
                 group by email) names
        on LOWER(expenses_list.email) = LOWER(names.email))
SELECT expenses_list.name, LOWER(expenses_list.email) as email,
       COALESCE(expenses_list.owed, 0.0) as owed,
       string_agg(CAST(expenses.index as varchar), ', ') as expense_nums
from expenses_list, expenses
where LOWER(expenses_list.email) = LOWER(expenses.email_address) AND expenses.paid IS NULL
group by expenses_list.name, expenses_list.email, expenses_list.owed ;
