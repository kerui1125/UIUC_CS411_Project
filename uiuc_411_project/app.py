# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State

import pandas as pd

from uiuc_411_project.flask_api import flask_app, register_routes
from uiuc_411_project.widgets.us_college_map import generate_us_college_map
from uiuc_411_project.widgets.keyword_publication_list import get_keyword_publication_list

register_routes(flask_app)
app = Dash(__name__, server=flask_app)

us_college_map_fig = generate_us_college_map()

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    dcc.Graph(figure=us_college_map_fig),
    html.Div([
        html.H2(children='Search paper by keyword'),
        dcc.Input(id='my-keyword', value='input keyword', type='text'),
        html.Button(id='submit-button-keyword', n_clicks=0, children='Submit'),
    ]),
    dcc.Graph(id='publication-form')
])

@app.callback(Output('publication-form', 'figure'),
              Input('submit-button-keyword', 'n_clicks'),
              State('my-keyword', 'value'))
def update_output(n_clicks, keyword):
    return get_keyword_publication_list(keyword)

if __name__ == '__main__':
    app.run_server(debug=True)
