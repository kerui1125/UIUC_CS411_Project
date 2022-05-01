from uiuc_411_project.db.mysql import MYSQL

import plotly.graph_objects as go
import pandas as pd


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
