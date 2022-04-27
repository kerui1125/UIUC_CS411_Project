from dash import Dash, Input, Output
from flask import Flask
import pandas as pd
import plotly.express as px

from uiuc_411_project.db.mongodb import get_us_college_map_info
from uiuc_411_project.db.neo4jdb import get_faculties, get_selection_items

flask_app = Flask(__name__)


def register_routes(app: Flask) -> None:
    @app.get("/ping")
    def ping():
        return "pong"

    @app.get("/college_and_faculty_map")
    def get_college_faculty_map():
        df = get_us_college_map_info()
        return df.to_dict(orient="split")


def register_callback_functions(app: Dash) -> None:
    # Keywords, institutes, faculty count pie chart widget
    @app.callback(
        Output("keywords_institute_pie", "figure"),
        Input("keywords", "value"),
        Input("institutes", "value")
    )
    def generate_keywords_selection_pie_map(k, i):
        results = get_selection_items(k, i)
        df = pd.DataFrame(results, columns=['keywords', 'institutes', 'faculty_count'], dtype=str)
        fig = px.pie(df, values="faculty_count", names="institutes", hole=.3)
        return fig

    # Faculty add, delete, modify keywords widget
    # Faculty dropdown selection
    @app.callback(
        Output("Faculty", "options"),
        Input("Universities", "value"))
    def faculty_selection(u):
        faculties_from_db = get_faculties(u)
        return faculties_from_db
