--How many trips drove more than 10% further than planned?
WITH cte AS (
SELECT DISTINCT tour_id, planned_km, driven_km
FROM tracking
)

SELECT COUNT(tour_id)
FROM cte
WHERE ((driven_km- planned_km)*100.0/planned_km) >10