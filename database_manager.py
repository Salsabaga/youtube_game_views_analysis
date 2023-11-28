from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd


class DatabaseManager:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self, Base):
        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.Session()

    def add_new_view_counts(self, converted_data, db_table):
        with self.Session() as session:
            for data in converted_data:
                new_entry = db_table(video_name=data["Video Name"], view_count=data["View Count"], date=data["Date"],
                                             time=data["Time"], name=data["Name"])
                session.add(new_entry)
                session.commit()

    def daily_view_trend(self):
        query_sql = """SELECT t.name, DATE(t.date) AS distinct_date, MIN(t.time) AS latest_time, t.video_name, t.view_count
        FROM youtube_data_table t
        WHERE (t.date, t.time) IN (
            SELECT MIN(date), time
            FROM youtube_data_table
            WHERE name = t.name
            GROUP BY time
        )
        GROUP BY t.name, DATE(t.date);"""
        result = pd.read_sql(query_sql, self.engine)
        return result

    def daily_view_count(self):
        query_sql = "SELECT name, MAX(view_count) AS Daily_view_count FROM youtube_data_table GROUP BY name"
        result = pd.read_sql(query_sql, self.engine)
        return result

    def daily_change_count(self):
        query = """WITH RankedRows AS (
            SELECT
                t.name,
                DATE(t.date) AS distinct_date,
                t.date,
                t.time,
                t.video_name,
                t.view_count,
                ROW_NUMBER() OVER (PARTITION BY t.name, DATE(t.date) ORDER BY t.date, t.time) AS row_num
            FROM youtube_data_table t
        )
        SELECT
            name,
            distinct_date,
            date,
            time,
            video_name,
            view_count
        FROM RankedRows
        WHERE row_num = 1;"""
        change_count_df = pd.read_sql_query(query, self.engine)

        # Calculate view count differences
        change_count_df['view_count_difference'] = change_count_df.groupby('name')['view_count'].diff()

        return change_count_df.dropna()

    # Fix issue with null values, to be ammended in case of edgecases (a new column to be made)
    # for data in video_list:
    #     result = session.query(YoutubeDataTable).filter(and_(YoutubeDataTable.video_name.contains(data["name"]),
    #                                                     YoutubeDataTable.name.is_(None))).all()
    #     for row in result:
    #         row.name = data['name']
    #         print(f"{row.video_name}, {row.name}, matches with: {data['name']}")
    #
    # session.commit()
