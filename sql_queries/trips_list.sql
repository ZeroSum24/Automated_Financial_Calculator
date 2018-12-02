SELECT *, tableoid::regclass::text AS trip_name
FROM trips_table
ORDER BY trip_name ;
