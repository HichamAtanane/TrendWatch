import extract
import transform
import load
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values
import logging
import re
from datetime import datetime


config = dotenv_values("../.env")
DB = config["DATABASE"]
DB_USER = config["DATABASE_USER"]
DB_PASSWORD = config["DATABASE_PASSWORD"]
DB_NAME = config["DATABASE_NAME"]
DB_HOST = config["DATABASE_HOST"]
DB_PORT = config["DATABASE_PORT"]
STAGING_DIR = Path("../data/staging/")
OUTPUT_DIR = Path("../data/output/")
LOGS_DIR = Path("../data/logs/")

exec_time = str(datetime.exec_time()).split(".")[0]
exec_time = re.sub(r"-|:|\s", "_", exec_time)
LOG_FILE = LOGS_DIR / f"{exec_time}.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)


def main(session) -> None:
    # EXTRACT
    logging.info("Start Fetching Data...")
    # extract.main()
    logging.info("Data Fetched Successfully.")
    # TRANSFORM & LOAD
    json_files = STAGING_DIR.glob("*.json")
    logging.info("Start Transforming data...")
    for json_file in json_files:
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
            load.load_trending_video_stats(session, trending_stats)
        logging.info(f"{json_file.name} transformed and loaded successfully")
        json_file.rename(OUTPUT_DIR / json_file.name)
        logging.info(f"{json_file.name} moved from STAGING AREA to OUTPUT folder")


if __name__ == "__main__":
    engine = create_engine(
        f"{DB}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    Session = sessionmaker(bind=engine)
    with Session() as session:
        main(session)
