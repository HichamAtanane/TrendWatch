-- psql -U your_username -d your_database_name -f insert_video_categories.sql

CREATE TEMP TABLE DimCategory_Staging (
    category_id INT,
    category_name VARCHAR(100)
);


COPY DimCategory_Staging (category_id, category_name)
FROM 'C:\_projects\TrendWatch\data\input\dim_video_categories.csv'WITH (FORMAT CSV, HEADER true, DELIMITER ',');

INSERT INTO DimCategory (category_id, category_name)
SELECT category_id, category_name
FROM DimCategory_Staging;

DROP TABLE DimCategory_Staging;

