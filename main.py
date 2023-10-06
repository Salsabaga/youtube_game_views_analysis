# YouTube Video Tracker
# Step 1. Download Selenium
# Step 2. Obtain the viscount using selenium and the text count of the view count.
# Step 3. Add to Excel/Database
# 3.1: Format the data to show the columns and rows
# 3.2: Columns will include, view count, time, date and increase percentage.
# 3.3: Add them into a list of dictionaries
# 3.4: Add list of dictionaries to database
# Step 4. Automate call to run every 6 hrs

from data_converter import DataConverter
from youtube_data_table import YoutubeDataTable, Base
from database_manager import DatabaseManager
import youtube_videos

video_list = youtube_videos.youtube_videos
db_url = "sqlite:///youtubeviews.db"
db_manager = DatabaseManager(db_url)

db_manager.create_tables(Base)

session = db_manager.get_session()

data_collector = DataConverter(video_list)
views_list = data_collector.add_to_table()

for data in views_list:
    new_entry = YoutubeDataTable(video_name=data["Video Name"], view_count=data["View Count"], date=data["Date"],
                                 time=data["Time"])
    session.add(new_entry)
    session.commit()


session.close()
