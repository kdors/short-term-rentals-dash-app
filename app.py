import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

from st_rentals import get_df

app = dash.Dash(__name__)

colors = {
    "mainBackground": "#dfdfde",
    "background": "#ffffff",
    "text": "#444444"
}


''' Get data and clean up'''
df = get_df()

# only keep the most recent application date for each unique address
df_last_add = df.sort_values("application_date").drop_duplicates("address", keep="last")
df_last_add = df_last_add.drop(df_last_add[df_last_add["address"].isnull()].index)

# separate out latitude and longitude from Location column
lat = [d.get("latitude") for d in df_last_add["location"]]
lon = [d.get("longitude") for d in df_last_add["location"]]

df_last_add["latitude"] = list(map(float,lat))
df_last_add["longitude"] = list(map(float,lon))


''' Application Count by Year Figure'''
df_year_count = df_last_add.groupby("Year")["application_date"].count().reset_index()
df_year_count.rename(columns={"Year":"Year", "application_date":"Application Count"}, inplace=True)

fig_year = px.bar(df_year_count, x="Year", y="Application Count", color_discrete_sequence=px.colors.qualitative.Set3)

fig_year.update_layout(
    plot_bgcolor=colors["background"],
    font_color=colors["text"],
    margin={"r":10,"t":10,"l":10,"b":10}
)


''' Current Status Count Figure'''
df_status_count = df_last_add.groupby("current_status")["application_date"].count().reset_index()
df_status_count.rename(columns={"current_status":"Current Status", "application_date":"Count"}, inplace=True)

fig_status = px.bar(df_status_count, x="Current Status", y="Count", color_discrete_sequence=px.colors.qualitative.Set3)

fig_status.update_layout(
    plot_bgcolor=colors["background"],
    font_color=colors["text"],
    margin={"r":10,"t":10,"l":10,"b":10}
)


''' App Layout'''
app.layout = html.Div(children=[

    html.H1(children='Short-Term Rentals in New Orleans'),

    html.Div(
        className="first-row",
        children=[
        html.Div(
            className="map",
            children=[
            dcc.Graph(
                id='location-map'
            )]),

        html.Div(
            className="info-and-filters",
            children=[
            html.Div(
                className="info",
                children=[
                html.H2("What is the state of current short-term rental applications in New Orleans?"),
                    '''
                    The year 2020 and the beginning of lockdowns saw a sharp decline in the number 
                    of submitted short-term rental applications.
                    ''',
                    html.Br(),
                    '''
                    In 2021, that number increased significantly, but still was not as high as pre-2020.
                    ''',
                    html.Br(),
                    '''
                    Will we see even more applications in 2022?
                    '''
                ]),
            html.Div(
                className="filter",
                children=[
                html.H2("Map Filters"),
                html.Label("Application Current Status"),
                dcc.Dropdown(
                    id="map-dropdown",
                    options=[
                        {"label":"Denied", "value":"Denied"},
                        {"label":"Expired", "value":"Expired"},
                        {"label":"Issued", "value":"Issued"},
                        {"label":"Pending", "value":"Pending"}
                    ],
                    value=["Issued"],
                    multi=True
                ),
                html.Label("Year"),
                dcc.Dropdown(
                    id="year-dropdown",
                    options=[
                        {"label":"2017", "value":2017},
                        {"label":"2018", "value":2018},
                        {"label":"2019", "value":2019},
                        {"label":"2020", "value":2020},
                        {"label":"2021", "value":2021},
                        {"label":"2022", "value":2022},
                    ],
                    value=[2017,2018,2019,2020,2021,2022],
                    multi=True
                )]
            )])
        ]),

    html.Div(
        className="second-row",
        children=[
        html.Div(
            className="figure",
            children=[
            html.H3("Number of New Applications Each Year"),
            dcc.Graph(
                id='applications-by-year',
                figure=fig_year
            )]), 
        html.Div(
            className="figure",
            children=[
            html.H3("Current Status for All Addresses"),
            html.Div(
            dcc.Graph(
                id='status-count',
                figure=fig_status
            )),
            html.H3("")])
            ])
], style={
    "backgroundColor":colors["mainBackground"],
    "color":colors["text"],
    "margin":0
})

@app.callback(
    Output("location-map","figure"),
    Input("map-dropdown","value"),
    Input("year-dropdown","value"))
def update_map(status_values, year_values):
    df_updated = df_last_add[(df_last_add["current_status"].isin(status_values)) & (df["Year"].isin(year_values))]
    fig_map = px.scatter_mapbox(df_updated, lat="latitude", lon="longitude", hover_name="address", 
                        hover_data=["application_date", "current_status"], 
                        color_discrete_sequence=px.colors.qualitative.Safe, zoom=11, height=600)
    fig_map.update_layout(mapbox_style="open-street-map")
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig_map

if __name__ == '__main__':
    app.run_server(debug=True)