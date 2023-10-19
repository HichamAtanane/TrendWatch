DROP TABLE IF EXISTS FactTrendingVideoStats;
DROP TABLE IF EXISTS DimTrendingDate;
DROP TABLE IF EXISTS DimVideo;
DROP TABLE IF EXISTS DimChannel;
DROP TABLE IF EXISTS DimRegion;
DROP TABLE IF EXISTS DimCategory;


-- Dimension Tables
CREATE TABLE DimTrendingDate (
    trending_date_pk SERIAL PRIMARY KEY,
    trending_date DATE NOT NULL,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    day INTEGER NOT NULL,
    day_of_week VARCHAR NOT NULL,
    week_of_month INTEGER NOT NULL,
    week_of_year INTEGER NOT NULL
);

CREATE TABLE DimVideo (
    video_pk SERIAL PRIMARY KEY,
    video_id VARCHAR(50) NOT NULL,
    video_title TEXT NOT NULL,
    video_duration INTEGER NOT NULL,
    video_caption INTEGER NOT NULL,
    video_published_at TIMESTAMP NOT NULL,
    video_rank INTEGER NOT NULL,
    video_description TEXT,
    video_tags TEXT
);

CREATE TABLE DimChannel (
    channel_pk SERIAL PRIMARY KEY,
    channel_id VARCHAR(50) NOT NULL,
    channel_name VARCHAR(100) NOT NULL
);

CREATE TABLE DimRegion (
    region_code CHAR(2) PRIMARY KEY,
    region_name VARCHAR(100) NOT NULL
);

CREATE TABLE DimCategory (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

-- Fact Table
CREATE TABLE FactTrendingVideoStats (
    trending_date_pk INTEGER REFERENCES DimTrendingDate(trending_date_pk),
    video_pk INTEGER REFERENCES DimVideo(video_pk),
    channel_pk INTEGER REFERENCES DimChannel(channel_pk),
    category_id INTEGER REFERENCES DimCategory(category_id),
    region_code CHAR(2) REFERENCES DimRegion(region_code),
    video_view_count INTEGER NOT NULL,
    video_like_count INTEGER,
    video_comment_count INTEGER,
    PRIMARY KEY (trending_date_pk, video_pk, channel_pk, category_id, region_code)
);
