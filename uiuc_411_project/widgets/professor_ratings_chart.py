from dash import html, dcc
import plotly.graph_objects as go

from uiuc_411_project.db.mysql import MYSQL


def generate_professor_ratings_chart() -> go.Figure:
    mysql = MYSQL()
    df = mysql.get_professor_ratings()

    df['text'] = "Professor: " + df['professor'] + " University: " + df['school'] + "<br>Average of ratings: " + df['ratings'].astype(str)

    fig = go.Figure(data=go.Scatter(
        x=df['ratings'],
        y=df['papers'],
        text=df['text'],
        mode='markers',
        marker=dict(
            size=df['papers'] / 100,
            sizemode="area"
                    )
    ))

    fig = go.Figure()

    return fig


def professor_ratings_widget() -> list:
    return [
        html.H2(children='Professor Ratings based on publications'),
        dcc.Graph(figure=generate_professor_ratings_chart())
    ]
