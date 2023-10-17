from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import ProgrammingError
from db_models import Base, DimCategory, DimRegion
from dotenv import dotenv_values
import json
from pathlib import Path


config = dotenv_values("../.env")
DB = config["DATABASE"]
DB_USER = config["DATABASE_USER"]
DB_PASSWORD = config["DATABASE_PASSWORD"]
DB_NAME = config["DATABASE_NAME"]
DB_HOST = config["DATABASE_HOST"]
DB_PORT = config["DATABASE_PORT"]
REGION_CODES = Path("../data/input/dim_region_codes.json")
VIDEO_CATEGORIES = Path("../data/input/dim_video_categories.json")


def read_json_file(file: Path) -> list[dict]:
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"{file} not found.")


def load_data_row(row, data_model) -> None:
    row_data = data_model(**row)
    session.add(row_data)
    session.commit()


def load_data() -> None:
    # category data
    video_categories = read_json_file(VIDEO_CATEGORIES)
    for data in video_categories:
        load_data_row(data, DimCategory)
    print("Category Data Loaded Successfully")
    # region data
    region_codes = read_json_file(REGION_CODES)
    for data in region_codes:
        load_data_row(data, DimRegion)
    print("Region Codes Data Loaded Successfully")


def main() -> None:
    # Create an SQLAlchemy engine and session
    engine = create_engine(
        f"{DB}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # Create tables in the database
    try:
        Base.metadata.create_all(engine)
        print("Tables Created Successfully")
        load_data()
    except ProgrammingError as pe:
        print(f"DATABASE ERROR:\n{pe}")


if __name__ == "__main__":
    engine = create_engine(
        f"{DB}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    Session = sessionmaker(bind=engine)
    with Session() as session:
        main()
