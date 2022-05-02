from dash import dcc, html, Dash, Input, Output

from uiuc_411_project.db.neo4jdb import get_institutes, get_faculties, get_faculty_data


def generate_view_faculty_widget(app: Dash) -> list:
    @app.callback(
        Output("faculty", "options"),
        Input("universities", "value")
    )
    def faculty_selection(university_input):
        faculties_from_db = get_faculties(university_input)
        return faculties_from_db

    @app.callback(
        Output('view_member', 'children'),
        Input('faculty', 'value')
    )
    def display_faculty_data(faculty_name):
        faculty_data = get_faculty_data(faculty_name)
        return html.Div([
            html.Div([
                html.Table([
                    html.Tr([
                        html.Th('Fields'),
                        html.Th('Values')
                    ]),
                    html.Tr([
                        html.Td('Phone'),
                        html.Td(faculty_data['phone'])
                    ]),
                    html.Tr([
                        html.Td('Position'),
                        html.Td(faculty_data['position'])
                    ]),
                    html.Tr([
                        html.Td('Email'),
                        html.Td(faculty_data['email'])
                    ]),
                    html.Tr([
                        html.Td('Institute Name'),
                        html.Td(faculty_data['institute_name'])
                    ])
                ]),
                html.Img(src=faculty_data['photoUrl'])
            ])
        ])

    institutes_from_db = get_institutes()
    return [
        html.H1('View Faculty Widget'),
        html.Br(),
        # faculty add, delete, modify keywords widget
        html.H2(children='Universities Selection'),
        dcc.Dropdown(
            id='universities',
            options=institutes_from_db,
            value='College of William Mary'
        ),
        html.H2(children='Faculty Selection'),
        dcc.Dropdown(
            id='faculty',
            value='Jog,Adwait'
        ),
        # tab 1 - show/modify faculty info, editable datatable to show data
        # tab 2 - add faculty info, editable datatable show to modify data, dropdowns inside datatable
        # when add new faculty search for univ, keywords.
        html.H2(children='Faculty Data'),
        html.H2('View Faculty Members'),
        html.Div(id='view_member', children='')
    ]
