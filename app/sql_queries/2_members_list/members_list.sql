-- showing a member list of all the people that have been listed in  a financial
-- doc for the club listed by their unique emails
CREATE TABLE members_list as

with member_list as
  (with unionised_emails as
    -- Get email of everyone on trips
    (SELECT DISTINCT(LOWER(email)) as email, Min(name) as name
      FROM trips_table
    GROUP BY email
    UNION
    -- get email of everyone in expenses
    SELECT DISTINCT(LOWER(email_address)) as email, Min(name) as name
      FROM expenses
    GROUP BY email
    UNION
    -- get email of everyone from refunds
    SELECT DISTINCT(LOWER(email_address)) as email, Min(name) as name
      FROM refunds
    GROUP BY email)
  -- select only the unique emails
  SELECT email, MIN(name) as name
  FROM unionised_emails
  group by email)
SELECT name, email
FROM member_list
ORDER BY name ;
