from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import ProgrammingError
from db_models import Base
from dotenv import dotenv_values


config = dotenv_values("../.env")
DB = config["DATABASE"]
DB_USER = config["DATABASE_USER"]
DB_PASSWORD = config["DATABASE_PASSWORD"]
DB_NAME = config["DATABASE_NAME"]
DB_HOST = config["DATABASE_HOST"]
DB_PORT = config["DATABASE_PORT"]


def main() -> None:
    # Create an SQLAlchemy engine and session
    engine = create_engine(
        f"{DB}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # Create tables in the database
    try:
        Base.metadata.create_all(engine)
        print("Tables Created Successfully")
    except ProgrammingError as pe:
        print(f"DATABASE ERROR:\n{pe}")


if __name__ == "__main__":
    main()
