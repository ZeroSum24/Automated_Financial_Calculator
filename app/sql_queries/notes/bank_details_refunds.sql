-- Filtering by provided bank details and the lengths of the account number and sort code
-- updating both extra zeros where their should be more
-- (uk account numbers should be length 8, sort codes should be length 6 )

WITH bank_details as
  (SELECT email_address AS email,
         refunds."do_you_have_a_uk_based_bank_account?" as uk_based_bank,
         name_of_bank, sort_code, account_number
  FROM refunds
  WHERE refunds."do_we_at_euhwc_need_your_bank_details_to_process_your_cash_refund?" <> 'No'
    AND (name_of_bank IS NOT NULL AND account_number IS NOT NULL AND sort_code IS NOT NULL)
  GROUP BY email, refunds."do_you_have_a_uk_based_bank_account?",
         name_of_bank, sort_code, account_number )
SELECT names.name, bank_details.email, bank_details.uk_based_bank, name_of_bank,
      CONCAT(REPEAT('0',8-LENGTH(CAST(account_number as varchar))),CAST(account_number as varchar)) as account_number,
      CONCAT(REPEAT('0',6-LENGTH(CAST(sort_code as varchar))),CAST(sort_code as varchar)) as sort_code
FROM bank_details
   LEFT JOIN (SELECT DISTINCT(email_address) as email, Min(name) as name
                  from refunds
                  group by email) names
       on bank_details.email = names.email
WHERE LENGTH(CONCAT(REPEAT('0',8-LENGTH(CAST(account_number as varchar))),CAST(account_number as varchar)))=8
  AND LENGTH(CONCAT(REPEAT('0',6-LENGTH(CAST(sort_code as varchar))),CAST(sort_code as varchar)))=6
ORDER BY name ;
