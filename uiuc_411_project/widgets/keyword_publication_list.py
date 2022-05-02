from uiuc_411_project.db.mysql import MYSQL

from dash import dcc, html, Dash, Input, Output, State
import plotly.graph_objects as go
import pandas as pd


def get_publications_by_keyword_widget(app: Dash) -> list:
    @app.callback(Output('publication-form', 'figure'),
                  Input('submit-button-keyword', 'n_clicks'),
                  State('my-keyword', 'value'))
    def update_output(n_clicks, keyword):
        return get_keyword_publication_list(keyword)

    return [
        html.H2(children='Search paper by keyword'),
        dcc.Input(id='my-keyword', value='input keyword', type='text'),
        html.Button(id='submit-button-keyword', n_clicks=0, children='Submit'),
        dcc.Graph(id='publication-form')
    ]


def get_keyword_publication_list(keyword) -> go.Figure:
    mysql = MYSQL()
    df = mysql.get_publication_by_keyword(keyword, 0)

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    align='left'),
        cells=dict(values=[df.publication_id, df.publication_name, df.year, df.professor],
                   align='left'))
    ])

    return fig
