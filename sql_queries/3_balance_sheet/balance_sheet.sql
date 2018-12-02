-- debt_list balance debug
CREATE TABLE balance_sheet as
SELECT members_list.name, members_list.email,

      CAST((CASE WHEN owes is not null and owed is not null and credit is not null
              THEN owes-owed-credit
             WHEN owes is not null and owed is not null and credit is null
              THEN owes-owed
             WHEN owes is not null and owed is null and credit is not null
              THEN owes-credit
             WHEN owes is not null and owed is null and credit is null
              THEN owes
             WHEN owes is null and owed is not null and credit is null
              THEN 0.0-owed
             ELSE 0.0
             END) as DECIMAL(10,2)) as balance,
       COALESCE(owes, 0.00) as owes, COALESCE(owed, 0.00) as owed,
       COALESCE(credit,0.00) as credit,
       COALESCE(trips, 'n/a') as owes_for_trips,
       COALESCE(expense_nums, 'n/a') as owed_for_expenses,
       COALESCE(refund_nums, 'n/a') as credit_requests
FROM members_list
  LEFT JOIN trip_debts
    ON LOWER(members_list.email) = LOWER(trip_debts.email)
  LEFT JOIN expenses_owed
    ON LOWER(members_list.email) = LOWER(expenses_owed.email)
  LEFT JOIN refunds_info
    ON LOWER(members_list.email) = LOWER(refunds_info.email)
ORDER BY members_list.name;
