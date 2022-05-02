from uiuc_411_project.db.mysql import MYSQL

from dash import dcc, html, Dash, Input, Output, State
import plotly.graph_objects as go


def publication_review_widget(app: Dash) -> list:
    @app.callback(Output('review-form', 'figure'),
                  Input('submit-review', 'n_clicks'),
                  State('paper-id', 'value'),
                  State('reviewer-id', 'value'),
                  State('score', 'value'),)
    def update_output(n_clicks, pub_id, reviewer_id, score):
        return get_paper_review_info(pub_id, reviewer_id, score)

    return [
        html.H2(children='Review publications by paper id and reviewer id'),
        dcc.Input(id='paper-id', value='input paper id', type='text'),
        dcc.Input(id='reviewer-id', value='input reviewer id', type='text'),
        dcc.Input(id='score', value='input review score', type='text'),
        html.Button(id='submit-review', n_clicks=0, children='Submit'),
        dcc.Graph(id='review-form')
    ]


def get_paper_review_info(paper_id, reviewer_id, score) -> go.Figure:
    if paper_id == "input publication id":
        fig = go.Figure(data=[go.Table(
            header=dict(values=['Publication Review'],
                        align='left'),
            cells=dict(values=['Please insert publication id, score and reviewer id'],
                       align='left'))
        ])
        return fig

    mysql = MYSQL()

    try:
        mysql.set_publication_review(paper_id, reviewer_id, score)
    except:
        fig = go.Figure(data=[go.Table(
            header=dict(values=['Input error'],
                        align='left'),
            cells=dict(values=['Review failed to get updated, please check the input combination'],
                       align='left'))
        ])
        return fig

    df = mysql.get_publication_reviews(paper_id)
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    align='left'),
        cells=dict(values=[df.publication_id, df.publication_name, df.review_score, df.reviewer],
                   align='left'))
    ])
    return fig

