# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
from dash import Dash, html

from uiuc_411_project.app_registrations import flask_app, register_routes, register_callback_functions
from uiuc_411_project.widgets.us_college_map import generate_college_map_widget
from uiuc_411_project.widgets.faculty_pie_chart import generate_faculty_pie_chart_widget
from uiuc_411_project.widgets.modifiable_faculty_table import generate_modifiable_faculty_widget
from uiuc_411_project.widgets.keyword_publication_list import get_publications_by_keyword_widget

register_routes(flask_app)
flask_app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app = Dash(__name__, server=flask_app)

content = []
# US University map widget
content.extend(generate_college_map_widget())
# Keywords, institutes, faculty count pie chart widget
content.extend(generate_faculty_pie_chart_widget())
# Faculty add, delete, modify keywords widget
content.extend(generate_modifiable_faculty_widget())
# Publication query by keyword
content.extend(get_publications_by_keyword_widget())

app.layout = html.Div(children=content)
register_callback_functions(app)


if __name__ == '__main__':
    app.run_server(debug=True)
