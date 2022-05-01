from dash import dcc, html

from uiuc_411_project.db.neo4jdb import get_institutes, get_keywords


def generate_faculty_pie_chart_widget() -> list:
    keywords_from_db = get_keywords()
    institutes_from_db = get_institutes()
    return [
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
            value=['Purdue University--West Lafayette', 'Northeastern University'],
            multi=True
        ),
        html.H2(children='Pie Chart'),
        dcc.Graph(id='keywords_institute_pie')
    ]
