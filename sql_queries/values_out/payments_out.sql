COPY
(SELECT balance_sheet.email, balance_sheet.name, balance, uk_based_bank,
       name_of_bank, account_number, sort_code
FROM balance_sheet
  LEFT JOIN bank_details
    ON LOWER(balance_sheet.email) = LOWER(bank_details.email)
WHERE balance < 0) TO STDOUT (format csv, delimiter ',') ;
