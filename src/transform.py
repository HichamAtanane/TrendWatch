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
    day: int
    day_of_week: str
    week_of_month: int
    week_of_year: int


@dataclass
class DimensionVideo:
    video_id: str
    video_title: str
    video_duration: int
    video_caption: int
    video_rank: int
    video_published_at: str
    video_description: str
    video_tags: list[str]


@dataclass
class DimensionChannel:
    channel_id: str
    channel_name: str


@dataclass
class FactTrendingVideoStats:
    trending_date_pk: int
    video_pk: int
    channel_pk: int
    category_id: int
    region_code: str
    video_view_count: int
    video_like_count: int
    video_comment_count: int


def parse_trending_date(trending_date: str) -> dict:
    trending_date = datetime.strptime(trending_date, "%Y-%m-%d")
    year = trending_date.year
    month = trending_date.month
    day = trending_date.day
    day_of_week = day_name[trending_date.weekday()]
    week_of_month = (day - 1) // 7 + 1
    week_of_year = trending_date.isocalendar().week
    dim_trending_date = DimensionTrendingDate(
        trending_date,
        year,
        month,
        day,
        day_of_week,
        week_of_month,
        week_of_year,
    )
    return asdict(dim_trending_date)


def duration_in_seconds(duration: str) -> int:
    pattern = r"^PT(\d+H)?(\d+M)?(\d+S)?$"
    match = re.match(pattern, duration)
    if match:
        hours = int(match.group(1)[:-1]) if match.group(1) else 0
        minutes = int(match.group(2)[:-1]) if match.group(2) else 0
        seconds = int(match.group(3)[:-1]) if match.group(3) else 0
        duration = hours * 3600 + minutes * 60 + seconds
    else:
        duration = 0
    return duration


def parse_dim_video(data: dict) -> dict:
    video_id = data["id"]
    duration = duration_in_seconds(data["contentDetails"]["duration"])
    caption = data["contentDetails"]["caption"]
    caption = 1 if caption == "true" else 0
    title = data["snippet"]["title"]
    rank = data["rank"]
    published_at = data["snippet"]["publishedAt"]
    # published_at = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%SZ')
    description = data["snippet"]["description"]
    tags = data["snippet"]["tags"] if "tags" in data["snippet"] else []
    dim_video = DimensionVideo(
        video_id, title, duration, caption, rank, published_at, description, tags
    )
    return asdict(dim_video)


def parse_dim_channel(snippet: dict) -> dict:
    channel_id = snippet["channelId"]
    channel_title = snippet["channelTitle"]
    dim_channel = DimensionChannel(channel_id, channel_title)
    return asdict(dim_channel)


def parse_trending_video_stats(statistics: dict) -> dict:
    trending_date_pk = statistics["trending_date_pk"]
    video_pk = statistics["video_pk"]
    channel_pk = statistics["channel_pk"]
    category_id = statistics["categoryId"]
    region_code = statistics["regionCode"]
    comment_count = statistics.get("commentCount", 0)
    like_count = statistics.get("likeCount", 0)
    view_count = statistics["viewCount"]
    trending_video_stats = FactTrendingVideoStats(
        trending_date_pk,
        video_pk,
        channel_pk,
        category_id,
        region_code,
        comment_count,
        like_count,
        view_count,
    )
    return asdict(trending_video_stats)


def parse_video_data(data: dict, file_name: Path) -> tuple[dict, dict, dict, dict]:
    file_name = file_name.stem
    data["trendingDate"] = file_name[3:-2].replace("_", "-")
    # (trending_date, year, month, day, day_of_week, week_of_month, week_of_year)
    trending_date = parse_trending_date(data["trendingDate"])
    # (video_id, title, duration, caption, rank, published_at, description, tags)
    dim_video = parse_dim_video(data)
    # (channel_id, channel_title)
    dim_channel = parse_dim_channel(data["snippet"])
    video_statistics = data["statistics"]
    video_statistics["regionCode"] = file_name[:2]
    video_statistics["categoryId"] = data["snippet"]["categoryId"]

    return trending_date, dim_video, dim_channel, video_statistics


def read_json_file(file: Path) -> list[dict]:
    with open(file, "r", encoding="utf-8") as f:
        data = dict(json.load(f))
    data = data["items"]
    for index in range(len(data)):
        rank = index + 1
        data[index]["rank"] = rank
    return data
