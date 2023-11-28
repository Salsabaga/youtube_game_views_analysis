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
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from youtube_data_table import YoutubeDataTable, Base
from database_manager import DatabaseManager
import youtube_videos


video_list = youtube_videos.youtube_videos
db_url = "sqlite:///youtubeviews.db"
db_manager = DatabaseManager(db_url)

db_manager.create_tables(Base)

session = db_manager.get_session()

# data_collector = DataConverter(video_list)
# views_list = data_collector.add_to_table()
# db_manager.add_new_view_counts(views_list, YoutubeDataTable)

r = db_manager.daily_view_count()
t = db_manager.daily_change_count()
session.close()

# Dash Server
#
external_stylesheet = ['https://fonts.googleapis.com/css2?family=Roboto&display=swap', "styles.css"]

colors = {
    "background": "#111111",
    "text": "#c0cdeb"
}

app = Dash(__name__, external_stylesheets=external_stylesheet)

fig = px.bar(data_frame=r, y="name", x="Daily_view_count",
             labels={"name": "Character/Video Name", "Daily_view_count": "Total View Count"})

fig.update_layout(plot_bgcolor=colors["background"], paper_bgcolor=colors["background"], font_color=colors["text"])

trend_fig = px.line(data_frame=t, y="view_count_difference", x="distinct_date", color="name",
                    labels={"view_count_difference": "View Count Increase", "distinct_date": "Date"})

trend_fig.update_layout(plot_bgcolor=colors["background"], paper_bgcolor=colors["background"], font_color=colors["text"])

app.layout = dbc.Container(className="intro-container", children=[
    html.H1("Tekken 8 Youtube Trailers Analysis"),
    dbc.Card([
        html.P("Tekken Series is my all time favourite gaming franchise, a masterpiece of a fighting game that always "
               "has the capactity, tendency and quality to create something amazing. Tekken 8 will be the latest "
               "upcoming release, 26 January 2024, and while I am excited to purchase the game, the build up has been "
               "disjointed, a 'disjointed hype' as I would describe it. By utilising the stats of its Youtube view "
               "counts, from its Bandai Namco America Channel, I want to analyse the uncharacterisical trend as "
               "compared to other fighting game and what are the factors in regards to a confusing, but exciting hype "
               "and delivery for Tekken 8.")
    ]),
    dcc.Tabs(id="youtube_views_tabs", className="custom-tabs", value="tab-1", children=[
        dcc.Tab(label="View Count Daily Increase Graph", value="tab-1", className="custom-tab"),
        dcc.Tab(label="Total View Count Graph", value="tab-2", className="custom-tab")
    ]),
    dbc.Container(id="youtube_views_content")
])


@app.callback(
    Output('youtube_views_content', 'children'),
    [Input('youtube_views_tabs', 'value')]
)
def render_content(tab):
    if tab == "tab-1":
        return dbc.Container([
            html.H3("Daily View Count Increase"),
            dcc.Graph(
                className="graph-design",
                id="graph-1",
                figure=trend_fig
            )
        ])
    elif tab == "tab-2":
        return dbc.Container([
            html.H3("Total View Count"),
            dcc.Graph(
                className="graph-design",
                id="graph-2",
                figure=fig
            )
        ])


app.run_server(debug=True)

