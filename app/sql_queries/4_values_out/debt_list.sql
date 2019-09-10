SELECT email, name, balance, owes_for_trips, owed_for_expenses as owed_for_expense_requests, credit_requests
FROM balance_sheet
WHERE balance <> 0 ;
