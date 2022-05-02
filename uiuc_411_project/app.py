# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html
import dash_bootstrap_components as dbc

from uiuc_411_project.app_registrations import flask_app, register_routes
from uiuc_411_project.widgets.us_college_map import generate_college_map_widget
from uiuc_411_project.widgets.faculty_pie_chart import generate_faculty_pie_chart_widget
from uiuc_411_project.widgets.view_faculty_table import generate_view_faculty_widget
from uiuc_411_project.widgets.modifiable_faculty_table import generate_modifiable_faculty_widget

register_routes(flask_app)
flask_app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app = Dash(__name__, server=flask_app)

content = []
# US University map widget
content.extend(generate_college_map_widget())
# Keywords, institutes, faculty count pie chart widget
content.extend(generate_faculty_pie_chart_widget(app))
# Faculty view widget
content.extend(generate_view_faculty_widget(app))
# Faculty add, delete, modify keywords widget
content.extend(generate_modifiable_faculty_widget(app))

app.layout = html.Div(children=content)

if __name__ == '__main__':
    app.run_server(debug=True)
