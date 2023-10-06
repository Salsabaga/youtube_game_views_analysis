from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class YoutubeDataTable(Base):
    __tablename__ = 'youtube_data_table'
    id = Column(Integer, primary_key=True)
    video_name = Column(String, nullable=False)
    view_count = Column(Integer, nullable=False)
    date = Column(String, nullable=False)
    time = Column(String)
