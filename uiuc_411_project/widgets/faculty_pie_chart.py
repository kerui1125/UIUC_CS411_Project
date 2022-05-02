from dash import dcc, html, Dash, Input, Output
import pandas as pd
import plotly.express as px

from uiuc_411_project.db.neo4jdb import get_institutes, get_keywords, get_selection_items


def generate_faculty_pie_chart_widget(app: Dash) -> list:
    @app.callback(
        Output("keywords_institute_pie", "figure"),
        Input("keywords", "value"),
        Input("institutes", "value")
    )
    def generate_keywords_selection_pie_map(keywords_input, institutes_input):
        results = get_selection_items(keywords_input, institutes_input)
        df = pd.DataFrame(results, columns=['keywords', 'institutes', 'faculty_count'], dtype=str)
        fig = px.pie(df, values="faculty_count", names="institutes", hole=.3)
        return fig

    keywords_from_db = get_keywords()
    institutes_from_db = get_institutes()
    return [
        html.H1('Keywords Institutes Faculty Number Pie-chart'),
        html.Br(),
        html.H2(children='Keywords Filter Selection'),
        dcc.Dropdown(
            id='keywords',
            options=keywords_from_db,
            value=['internet', 'computer science'],
            multi=True
        ),
        html.H2(children='Institutes Filter Selection'),
        dcc.Dropdown(
            id='institutes',
            options=institutes_from_db,
            value=['Purdue University--West Lafayette', 'University of Rochester'],
            multi=True
        ),
        html.H2(children='Pie Chart'),
        dcc.Graph(id='keywords_institute_pie')
    ]
