--How many invoices are duplicates (the same shipment billed again)? Count only the later invoice, not the first.
WITH cte AS(
SELECT invoice_id, shipment_id, invoice_date, ROW_NUMBER() OVER(PARTITION BY shipment_id ORDER BY invoice_date) as rn
FROM invoices
)

SELECT invoice_id, shipment_id, invoice_date
FROM cte
WHERE rn>1


