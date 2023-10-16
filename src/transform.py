from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
from calendar import day_name
import json
import re


@dataclass
class DimensionTrendingDate:
    trending_date: datetime
    year: int
    month: int
    day_of_month: int
    day_of_week: str
    week_of_month: int
    week_of_year: int


@dataclass
class DimensionVideo:
    video_id: str
    title: str
    duration: int
    caption: int
    rank: int
    published_at: str
    description: str
    tags: list[str]


@dataclass
class DimensionChannel:
    channel_id: str
    channel_title: str


@dataclass
class FactTrendingVideoStats:
    trending_date_pk: int
    video_pk: int
    channel_pk: int
    category_id: int
    region_code: str
    view_count: int
    like_count: int
    comment_count: int


def parse_trending_date(trending_date: str) -> dict:
    trending_date = datetime.strptime(trending_date, "%Y-%m-%d")
    year = trending_date.year
    month = trending_date.month
    day_of_month = trending_date.day
    day_of_week = day_name[trending_date.weekday()]
    week_of_month = (day_of_month - 1) // 7 + 1
    week_of_year = trending_date.isocalendar().week
    dim_trending_date = DimensionTrendingDate(
        trending_date,
        year,
        month,
        day_of_month,
        day_of_week,
        week_of_month,
        week_of_year,
    )
    return asdict(dim_trending_date)
