from dash import dcc, html, Dash, Input, Output, State

from uiuc_411_project.db.neo4jdb import add_a_faculty_member


def generate_modifiable_faculty_widget(app: Dash) -> list:
    @app.callback(
        Output('add_faculty_result', 'children'),
        Input('submit-val', 'n_clicks'),
        State('input_name', 'value'),
        State('input_phone', 'value'),
        State('input_position', 'value'),
        State('input_email', 'value'),
        State('input_institute_name', 'value')
    )
    def add_a_new_faculty(n_clicks, name, phone, position, email, institute_name):
        try:
            if name is not None and institute_name is not None:
                add_a_faculty_member(name, phone, position, email, institute_name)
                return "Successfully added a new faculty member"
        except Exception as e:
            print(f"Error occurred due to: {e}")
            return "Failed to add a new faculty member"

    return [
        html.H1('Add Faculty Widget'),
        html.Br(),
        html.H2('Add a New Member'),
        html.Table([
            html.Tr([
                html.Th('Input Fields'),
                html.Th('Input Values')
            ]),
            html.Tr([
                html.Td('Name'),
                html.Td(dcc.Input(
                    id='input_name',
                    type='text',
                    placeholder='Please enter a member name'
                ))
            ]),
            html.Tr([
                html.Td('Phone'),
                html.Td(dcc.Input(
                    id='input_phone',
                    type='text',
                    placeholder='Please enter a phone number'
                ))
            ]),
            html.Tr([
                html.Td('Position'),
                html.Td(dcc.Input(
                    id='input_position',
                    type='text',
                    placeholder='Please enter a position'
                ))
            ]),
            html.Tr([
                html.Td('Email'),
                html.Td(dcc.Input(
                    id='input_email',
                    type='text',
                    placeholder='Please enter an email address'
                ))
            ]),
            html.Tr([
                html.Td('Institute Name'),
                html.Td(dcc.Input(
                    id='input_institute_name',
                    type='text',
                    placeholder='Please enter an institute name'
                ))
            ])
        ]),
        html.Button('Submit', id='submit-val', n_clicks=0),
        html.Div(id='add_faculty_result', children='')
    ]
