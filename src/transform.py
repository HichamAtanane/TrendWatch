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
