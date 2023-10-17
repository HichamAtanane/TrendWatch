import extract
import transform
import load
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values


config = dotenv_values("../.env")
DB = config["DATABASE"]
DB_USER = config["DATABASE_USER"]
DB_PASSWORD = config["DATABASE_PASSWORD"]
DB_NAME = config["DATABASE_NAME"]
DB_HOST = config["DATABASE_HOST"]
DB_PORT = config["DATABASE_PORT"]
STAGING_DIR = Path("../data/staging/")
OUTPUT_DIR = Path("../data/output/")


def main(session) -> None:
    # EXTRACT
    extract.main()
    # TRANSFORM & LOAD
    json_files = STAGING_DIR.glob("*.json")
    for json_file in json_files:
        print(json_file)
        data = transform.read_json_file(json_file)
        for video_data in data:
            data = transform.parse_video_data(video_data, json_file)
            trending_date, dim_video, dim_channel, video_statistics = data
            trending_date_pk = load.load_dim_trending_date(session, trending_date)
            video_pk = load.load_dim_video(session, dim_video)
            channel_pk = load.load_dim_channel(session, dim_channel)
            video_statistics["trending_date_pk"] = trending_date_pk
            video_statistics["video_pk"] = video_pk
            video_statistics["channel_pk"] = channel_pk
            trending_stats = transform.parse_trending_video_stats(video_statistics)
            load_trending_video_stats(session, trending_stats)
        # move file from staging to output
        json_file.rename(OUTPUT_DIR / json_file.name)


if __name__ == "__main__":
    engine = create_engine(
        f"{DB}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    Session = sessionmaker(bind=engine)
    with Session() as session:
        main(session)
