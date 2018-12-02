SELECT name, email, balance, owes_for_trips, owed_for_expenses, credit_requests
FROM balance_sheet
WHERE balance <> 0 ;
