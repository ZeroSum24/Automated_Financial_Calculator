-- Creating parent table to organise hold the trips together, have them inherit with a consistent schema

-- creating the parent table
CREATE TABLE trips_table (index bigint, name text, email text, position text, owes double precision, paid text, payment_method text ) ;


-- altering the tables to have the same schema as the parent

-- ALTER TABLE cairngorm SET SCHEMA (index bigint, name text, email text, position text, owes double precision, paid text, payment_method text ) ;
-- ALTER TABLE crianlarich SET SCHEMA (index bigint, name text, email text, position text, owes double precision, paid text, payment_method text ) ;
-- ALTER TABLE lakes_trip SET SCHEMA (index bigint, name text, email text, position text, owes double precision, paid text, payment_method text ) ;
-- ALTER TABLE loch_lochy SET SCHEMA (index bigint, name text, email text, position text, owes double precision, paid text, payment_method text ) ;
-- ALTER TABLE nov_sat_day_trip SET SCHEMA (index bigint, name text, email text, position text, owes double precision, paid text, payment_method text ) ;
-- ALTER TABLE nov_sun_day_trip SET SCHEMA (index bigint, name text, email text, position text, owes double precision, paid text, payment_method text ) ;
-- ALTER TABLE ratagan SET SCHEMA (index bigint, name text, email text, position text, owes double precision, paid text, payment_method text ) ;

-- altering the tables to inherit the parent
ALTER TABLE cairngorm INHERIT trips_table ;
ALTER TABLE crianlarich INHERIT trips_table ;
ALTER TABLE lakes_trip INHERIT trips_table ;
ALTER TABLE loch_lochy INHERIT trips_table ;
ALTER TABLE nov_sat_day_trip INHERIT trips_table ;
ALTER TABLE nov_sun_day_trip INHERIT trips_table ;
ALTER TABLE ratagan INHERIT trips_table ;
