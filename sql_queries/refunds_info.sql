
COPY (
with refunds_list as
  (with refunds_list as
    (SELECT email_address as email, CAST(SUM(total_amount_claimed_£) as DECIMAL(10,2)) AS credit
     FROM refunds
     WHERE paid IS NULL
     GROUP BY email)
    select names.name, refunds_list.email, refunds_list.credit
    from refunds_list
      left join (SELECT DISTINCT(email_address) as email, Min(name) as name
                 from refunds
                 group by email) names
        on refunds_list.email = names.email)
SELECT refunds_list.name, email, credit,
        string_agg(CAST((refunds.index+1) as varchar), ', ') as refund_num,
        string_agg(refunds.type_of_refunds, ', ') as refund_types
FROM refunds_list, refunds
where refunds_list.email = refunds.email_address
group by refunds_list.name, email, credit ;
) TO STDOUT (format csv, delimiter ',') ;
