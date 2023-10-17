from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_models import DimTrendingDate, DimVideo, DimChannel, FactTrendingVideoStats
from dotenv import dotenv_values


config = dotenv_values("../.env")
DB = config["DATABASE"]
DB_USER = config["DATABASE_USER"]
DB_PASSWORD = config["DATABASE_PASSWORD"]
DB_NAME = config["DATABASE_NAME"]
DB_HOST = config["DATABASE_HOST"]
DB_PORT = config["DATABASE_PORT"]
STAGING_DIR = Path("../data/staging")


def load_dim_trending_date(session, data: dict) -> str:
    dim_trending_date = DimTrendingDate(**data)
    session.add(dim_trending_date)
    session.commit()
    return dim_trending_date.trending_date_pk


def load_dim_video(session, data: dict) -> str:
    dim_video = DimVideo(**data)
    session.add(dim_video)
    session.commit()
    return dim_video.video_pk


def load_dim_channel(session, data: dict) -> str:
    dim_channel = DimChannel(**data)
    session.add(dim_channel)
    session.commit()
    return dim_channel.channel_pk


def load_trending_video_stats(session, data: dict) -> None:
    trending_video_stats = FactTrendingVideoStats(**data)
    session.add(trending_video_stats)
    session.commit()
    return None
