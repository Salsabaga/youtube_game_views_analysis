# Convert the dictionary into a dataframe for pandas and matplot lib
from youtube_view_count import YoutubeViewCount
import datetime


class DataConverter:
    def __init__(self, video_data_list):
        self.video_data_list = video_data_list
        self.data = []

    def add_to_table(self):
        for video in self.video_data_list:
            video_url = video["url"]
            overall_name = video["name"]
            video_views = YoutubeViewCount(video_url)
            video_info = video_views.get_views()
            video_name = video_info[0].text
            raw_view_count = video_info[1]
            cleaned_view_text = raw_view_count.replace(" views", "")
            view_count = int(cleaned_view_text.replace(",", ""))
            fetch_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").split(" ")
            date = fetch_datetime[0]
            time = fetch_datetime[1]
            data_entry = {'Video Name': video_name, 'View Count': view_count, 'Date': date,
                          'Time': time, 'Name': overall_name}
            self.data.append(data_entry)
            video_views.close()

        return self.data
