--Average truck fill rate per carrier, worst first. Count each trip only once.
with cte AS (
SELECT DISTINCT carrier_id, fill_rate_pct, tour_id

FROM tracking)

SELECT carrier_id, AVG(fill_rate_pct) AS top
FROM cte
GROUP BY carrier_id
ORDER BY top asc


