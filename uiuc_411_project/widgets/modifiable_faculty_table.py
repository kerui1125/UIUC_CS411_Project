from dash import dcc, html

from uiuc_411_project.db.neo4jdb import get_institutes


def generate_modifiable_faculty_widget() -> list:
    institutes_from_db = get_institutes()
    return [
        # faculty add, delete, modify keywords widget
        html.H2(children='Universities Selection'),
        dcc.Dropdown(
            id='Universities',
            options=institutes_from_db,
            value=['University of illinois at Urbana Champaign']
        ),
        html.H2(children='Faculty Selection'),
        dcc.Dropdown(id='Faculty')
        # tab 1 - show/modify faculty info, editable datatable to show data
        # tab 2 - add faculty info, editable datatable show to modify data, dropdowns inside datatable
        # when add new faculty search for univ, keywords.
    ]
