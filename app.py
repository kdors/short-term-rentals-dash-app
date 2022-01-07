import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

from st_rentals import get_df

app = dash.Dash(__name__)

colors = {
    "mainBackground": "#a9a9a9",
    "background": "#ffffff",
    "text": "#444444"
}
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

df = get_df()

df_last_add = df.sort_values("application_date").drop_duplicates("address", keep="last")
df_last_add = df_last_add.drop(df_last_add[df_last_add["address"].isnull()].index)

df_year_count = df_last_add.groupby("Year")["application_date"].count().reset_index()
df_year_count.rename(columns={"Year":"Year","application_date":"Application Count"}, inplace=True)

fig = px.bar(df_year_count, x="Year", y="Application Count")

fig.update_layout(
    plot_bgcolor=colors["background"],
    font_color=colors["text"]
)

app.layout = html.Div(children=[
    html.H1(children='Short-Term Rentals in New Orleans',
            style={
                "textAlign":"center",
                "color":colors["text"]
            }),

    html.Div(children='''
        What is the state of current short-term rental applications in New Orleans?
    ''',
                style={
                    "textAlign":"center",
                    "color":colors["text"]
                }),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)