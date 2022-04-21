from uiuc_411_project.db.mongodb import get_us_college_map_info

import plotly.graph_objects as go


def generate_us_college_map() -> go.Figure:
    df = get_us_college_map_info()
    df = df.sort_values(by=["professors"], ascending=False)
    df.head()

    df["text"] = "University: " + df['college'] + "<br>Number of professors: " + df['professors'].astype(str)
    limits = [(0, 2), (3, 10), (11, 20), (21, 50), (51, 100)]
    colors = ["royalblue", "crimson", "lightseagreen", "orange", "lightgrey"]
    scale = 0.7

    fig = go.Figure()

    for i in range(len(limits)):
        lim = limits[i]
        df_sub = df[lim[0]:lim[1]]
        fig.add_trace(go.Scattergeo(
            locationmode="USA-states",
            lon=df_sub["lon"],
            lat=df_sub["lat"],
            text=df_sub["text"],
            marker=dict(
                size=df_sub["professors"]/scale,
                color=colors[i],
                line_color="rgb(40,40,40)",
                line_width=0.5,
                sizemode="area"
            ),
            name=f"{lim[0]} - {lim[1]}"
        ))

    fig.update_layout(
            title_text="US University Map",
            showlegend=True,
            geo=dict(
                scope="usa",
                landcolor="rgb(217, 217, 217)",
            )
        )

    return fig
