from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import ProgrammingError
from ..db_models import Base, DimCategory, DimRegion
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
REGION_CODES = Path("./dim_region_codes.json")
VIDEO_CATEGORIES = Path("./dim_video_categories.json")


def read_json_file(file: Path) -> list[dict]:
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = dict(json.load(f))
        return data
    except FileNotFoundError:
        print(f"{file} not found.")


def load_data() -> None:
    # category data
    category_data = DimCategory(**read_json_file(VIDEO_CATEGORIES))
    session.add(category_data)
    session.commit()
    print("Category Data Loaded Successfully")
    # region data
    region_data = DimRegion(**read_json_file(REGION_CODES))
    session.add(region_data)
    session.commit()
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
    main()
