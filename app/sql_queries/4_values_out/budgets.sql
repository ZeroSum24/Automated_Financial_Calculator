
-- Total spend overall
SELECT CAST(SUM(total_amount_claimed_£) as decimal(10,2)) as total_overall
FROM Expenses e
WHERE e.paid = 'Paid' ;

-- Per budget spending
SELECT e.budget, CAST(SUM(total_amount_claimed_£) as decimal(10,2)) as total_expenses
FROM Expenses e
WHERE e.paid = 'Paid'
GROUP BY e.budget
ORDER BY e.budget ;

-- Per budget per category
SELECT e.budget, e.category, CAST(SUM(total_amount_claimed_£) as decimal(10,2)) as total
FROM Expenses e
WHERE e.paid = 'Paid'
GROUP BY e.budget, e.category
ORDER BY e.budget, e.category ;

-- Per category/category
SELECT e.category, CAST(SUM(total_amount_claimed_£) as decimal(10,2)) as total
FROM Expenses e
WHERE e.paid = 'Paid'
GROUP BY e.category
ORDER BY e.category ;

-- Trip Income/Outstanding
SELECT tableoid::regclass::text AS trip_name,
       CAST(SUM(owes) as DECIMAL(10,2)) as presign_income,
       CAST(SUM(owes) - SUM(CASE WHEN paid is not null THEN owes else 0 END) as DECIMAL(10,2)) as outstanding_amounts
FROM trips_table
GROUP BY trip_name
ORDER BY trip_name ;
