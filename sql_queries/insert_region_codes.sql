-- psql -U your_username -d your_database_name -f insert_region_codes.sql

CREATE TEMP TABLE DimRegion_Staging (
    region_code CHAR(2),
    region_name VARCHAR(100)
);

COPY DimRegion_Staging (region_code, region_name)
FROM 'C:\_projects\TrendWatch\data\input\dim_region_codes.csv' WITH (FORMAT CSV, HEADER true, DELIMITER ',');

INSERT INTO DimRegion (region_code, region_name)
SELECT region_code, region_name
FROM DimRegion_Staging;

DROP TABLE DimRegion_Staging;
