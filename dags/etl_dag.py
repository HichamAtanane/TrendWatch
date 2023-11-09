# Airflow
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
# ETL Modules
import extract
import transform
import load
# SQLAlchmey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# other imports
from datetime import datetime, timedelta
from dotenv import dotenv_values
from pathlib import Path
import logging
import re


parent_dir = Path(__file__).resolve().parents[1]
config = dotenv_values(parent_dir / ".env")
DB = config["DATABASE"]
DB_USER = config["DATABASE_USER"]
DB_PASSWORD = config["DATABASE_PASSWORD"]
DB_NAME = config["DATABASE_NAME"]
DB_HOST = config["DATABASE_HOST"]
DB_PORT = config["DATABASE_PORT"]
STAGING_DIR = parent_dir / "data/staging/"
OUTPUT_DIR = parent_dir / "data/output/"
LOGS_DIR = parent_dir / "data/logs/"
CATEGORY_IDS = [0,1,2,10,15,17,18,19,20,21,22,23,24,25,26,27,28,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,]


def setup_logging():
    exec_time = str(datetime.now()).split(".")[0]
    exec_time = re.sub(r"-|:|\s", "_", exec_time)
    LOG_FILE = LOGS_DIR / f"{exec_time}.log"
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO)


@dag(
    schedule_interval="0 16 * * *", start_date=days_ago(1), catchup=False, tags=["etl", "Trendwatch"]
)
def trendwatch_etl_dag():
    setup_logging()

    @task(retries=3, retry_delay=timedelta(minutes=30))
    def extract_data():
        logging.info("Start Fetching Data...")
        # extract.main()
        logging.info("Data Fetched Successfully.")


    @task()
    def transform_data() -> list[tuple[dict, dict, dict, dict]]:
        json_files = STAGING_DIR.glob("*.json")
        logging.info("Start Transforming data...")
        transformed_data = []
        for json_file in json_files:
            data = transform.read_json_file(json_file)
            for video_data in data:
                data = transform.parse_video_data(video_data, json_file)
                transformed_data.append(data)
            logging.info(f"{json_file.name} transformed successfully")
        return transformed_data


    @task
    def load_transformed_data(transformed_data) -> None:
        # Create Database Session
        engine = create_engine(
            f"{DB}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
        Session = sessionmaker(bind=engine)
        # Load Data
        with Session() as session:
            logging.info("Start Loading data...")
            for data in transformed_data:
                trending_date, dim_video, dim_channel, video_statistics = data
                trending_date_pk = load.load_dim_trending_date(session, trending_date)
                video_pk = load.load_dim_video(session, dim_video)
                channel_pk = load.load_dim_channel(session, dim_channel)
                video_statistics["trending_date_pk"] = trending_date_pk
                video_statistics["video_pk"] = video_pk
                video_statistics["channel_pk"] = channel_pk
                trending_stats = transform.parse_trending_video_stats(video_statistics)
                if trending_stats["category_id"] not in CATEGORY_IDS:
                    trending_stats["category_id"] = 0
                load.load_trending_video_stats(session, trending_stats)
        logging.info(f"Data Loaded successfully!!")


    @task
    def move_transformed_files() -> None:
        json_files = STAGING_DIR.glob("*.json")
        for json_file in json_files:
            json_file.rename(OUTPUT_DIR / json_file.name)
            logging.info(f"{json_file.name} moved from STAGING AREA to OUTPUT folder")
        logging.info("All transformed files moved from STAGING AREA to OUTPUT folder")

    extract_data = extract_data()
    transformed_data = transform_data()
    load_transformed_data = load_transformed_data(transformed_data)
    move_transformed_files = move_transformed_files()

    (
        extract_data
        >> transformed_data
        >> load_transformed_data
        >> move_transformed_files
    )


trendwatch_etl_dag()
