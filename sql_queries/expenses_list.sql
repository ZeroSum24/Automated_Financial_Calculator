COPY (
with expenses_list as
    (with expenses_list as
      (SELECT email_address as email, CAST(SUM(total_amount_claimed_£) as decimal(10,2)) AS owed
       FROM expenses
       -- WHERE paid IS null
       GROUP BY email)
    select names.name, expenses_list.email, expenses_list.owed
    from expenses_list
      left join (SELECT DISTINCT(email_address) as email, Min(name) as name
                 from expenses
                 group by email) names
        on expenses_list.email = names.email)
SELECT expenses_list.name, expenses_list.email, expenses_list.owed, string_agg(CAST(expenses.index as varchar), ', ') as expense_num
from expenses_list, expenses
-- where expenses_list.email = expenses.email AND expenses.paid IS NULL
where expenses_list.email = expenses.email_address
group by expenses_list.name, expenses_list.email, expenses_list.owed
) TO STDOUT (format csv, delimiter ',') ;
