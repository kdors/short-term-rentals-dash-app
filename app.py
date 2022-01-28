import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

from st_rentals import get_df

app = dash.Dash(__name__)

colors = {
    "mainBackground": "#a9a9a9",
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

fig_year = px.bar(df_year_count, x="Year", y="Application Count", color_discrete_sequence=px.colors.qualitative.Set3,
                    title="Number of New Applications Each Year")

fig_year.update_layout(
    plot_bgcolor=colors["background"],
    font_color=colors["text"]
)


''' Current Status Count Figure'''
df_status_count = df_last_add.groupby("current_status")["application_date"].count().reset_index()
df_status_count.rename(columns={"current_status":"Current Status", "application_date":"Count"}, inplace=True)

fig_status = px.bar(df_status_count, x="Current Status", y="Count", color_discrete_sequence=px.colors.qualitative.Set3,
                    title="Current Status for All Addresses")

fig_status.update_layout(
    plot_bgcolor=colors["background"],
    font_color=colors["text"]
)


''' Current Status By Year Figure'''
df_year_status = df.groupby(["Year","current_status"])["application_date"].count().reset_index()
df_year_status.rename(columns={"Year":"Year", "current_status":"Current Status", "application_date":"Count"}, inplace=True)

fig_year_status = px.line(df_year_status, x="Year", y="Count", color="Current Status", 
                            color_discrete_sequence=px.colors.qualitative.Safe)

fig_year_status.update_layout(
    plot_bgcolor=colors["background"],
    font_color=colors["text"]
)


''' Location Map '''
fig_map = px.scatter_mapbox(df_last_add, lat="latitude", lon="longitude", hover_name="address", 
                        hover_data=["application_date", "current_status"], 
                        color_discrete_sequence=px.colors.qualitative.Safe, zoom=11, height=600)

fig_map.update_layout(mapbox_style="open-street-map")
fig_map.update_layout(margin={"r":75,"t":25,"l":75,"b":25})


''' App Layout'''
app.layout = html.Div(children=[
    html.H1(children='Short-Term Rentals in New Orleans',
            style={
                "textAlign":"center",
                "color":colors["text"]
            }),

    html.Div(children=[
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
            '''], 
            style={
                "padding":"10px",
                "textAlign":"center",
                "color":colors["text"]
            }),

    html.Div(children=[
            html.Label("Application Current Status"),
            dcc.Dropdown(
                id="map-dropdown",
                options=[
                    {"label":"Denied", "value":"Denied"},
                    {"label":"Expired", "value":"Expired"},
                    {"label":"Issued", "value":"Issued"},
                    {"label":"Pending", "value":"Pending"}
                ],
                value="Issued"
            )],
            style={
                "color":colors["text"],
                "margin":"25px 100px 0 75px",
                "padding":"0 200px 0 0"
            }),

    html.Div(children=[
            dcc.Graph(
                id='location-map'
            )], 
            style={
                "color":colors["text"],
                "textAlign":"center",    
                "margin":"auto"
            }),

    html.Div(children=[
            html.H2("Deeper Dive into Short-Term Rental Applications"),
            '''
            Just how many new applications are being submitted each year,
            and what is the current status for all addresses in the short-term rental database?
            '''],
            style={
                "color":colors["text"],
                "textAlign":"center"
            }),

    html.Div(children=[
            dcc.Graph(
                id='applications-by-year',
                figure=fig_year
            ), 

            dcc.Graph(
                id='status-count',
                figure=fig_status
            )], 
            style={
                "display":"flex",
                "flex-wrap":"wrap"})
])

@app.callback(
    Output("location-map","figure"),
    Input("map-dropdown","value"))
def update_map(status):
    df_updated = df_last_add[df_last_add["current_status"] == status]
    fig_map = px.scatter_mapbox(df_updated, lat="latitude", lon="longitude", hover_name="address", 
                        hover_data=["application_date", "current_status"], 
                        color_discrete_sequence=px.colors.qualitative.Safe, zoom=11, height=600)
    fig_map.update_layout(mapbox_style="open-street-map")
    fig_map.update_layout(margin={"r":75,"t":25,"l":75,"b":25})

    return fig_map

if __name__ == '__main__':
    app.run_server(debug=True)