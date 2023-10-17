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


def main(session) -> None:
    json_files = STAGING_DIR.glob("*_1.json")
    for json_file in json_files:
        data = read_json_file(json_file)
        for video_data in data:
            trending_date, dim_video, dim_channel, video_statistics = parse_video_data(
                video_data, json_file
            )
            trending_date_pk = load_dim_trending_date(session, trending_date)
            video_pk = load_dim_video(session, dim_video)
            channel_pk = load_dim_channel(session, dim_channel)
            video_statistics["trending_date_pk"] = trending_date_pk
            video_statistics["video_pk"] = video_pk
            video_statistics["channel_pk"] = channel_pk
            trending_video_stats = parse_trending_video_stats(video_statistics)
            load_trending_video_stats(session, trending_video_stats)


if __name__ == "__main__":
    engine = create_engine(
        f"{DB}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    Session = sessionmaker(bind=engine)
    session = Session()

    main(session)
