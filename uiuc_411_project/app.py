# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc

from uiuc_411_project.flask_api import flask_app, register_routes
from uiuc_411_project.widgets.us_college_map import generate_us_college_map

register_routes(flask_app)
app = Dash(__name__, server=flask_app)

us_college_map_fig = generate_us_college_map()

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    dcc.Graph(figure=us_college_map_fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)
