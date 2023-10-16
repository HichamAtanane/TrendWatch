from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Text,
    TIMESTAMP,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base


Base = declarative_base()


# ------------- Dimension Tables -------------
class DimTrendingDate(Base):
    __tablename__ = "DimTrendingDate"
    __table_args__ = {"quote": False}
    trending_date_pk = Column(Integer, primary_key=True, autoincrement=True)
    trending_date = Column(Date, nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)
    day_of_week = Column(String, nullable=False)
    week_of_month = Column(Integer, nullable=False)
    week_of_year = Column(Integer, nullable=False)


class DimVideo(Base):
    __tablename__ = "DimVideo"
    __table_args__ = {"quote": False}
    video_pk = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(String(50), nullable=False)
    video_title = Column(Text, nullable=False)
    video_duration = Column(Integer, nullable=False)
    video_caption = Column(Integer, nullable=False)
    video_published_at = Column(TIMESTAMP, nullable=False)
    video_rank = Column(Integer, nullable=False)
    video_description = Column(Text)
    video_tags = Column(Text)


class DimChannel(Base):
    __tablename__ = "DimChannel"
    __table_args__ = {"quote": False}
    channel_pk = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(String(50), nullable=False)
    channel_name = Column(String(100), nullable=False)


class DimRegion(Base):
    __tablename__ = "DimRegion"
    __table_args__ = {"quote": False}
    region_code = Column(String(2), primary_key=True)
    region_name = Column(String(100), nullable=False)


class DimCategory(Base):
    __tablename__ = "DimCategory"
    __table_args__ = {"quote": False}
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(100), nullable=False)


# ------------- Fact Tables -------------
class FactTrendingVideoStats(Base):
    __tablename__ = "FactTrendingVideoStats"
    __table_args__ = {"quote": False}
    trending_date_pk = Column(
        Integer, ForeignKey("DimTrendingDate.trending_date_pk"), primary_key=True
    )
    video_pk = Column(Integer, ForeignKey("DimVideo.video_pk"), primary_key=True)
    channel_pk = Column(Integer, ForeignKey("DimChannel.channel_pk"), primary_key=True)
    category_id = Column(
        Integer, ForeignKey("DimCategory.category_id"), primary_key=True
    )
    region_code = Column(
        String(2), ForeignKey("DimRegion.region_code"), primary_key=True
    )
    video_view_count = Column(Integer, nullable=False)
    video_like_count = Column(Integer)
    video_comment_count = Column(Integer)
