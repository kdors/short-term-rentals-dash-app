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


''' Get data and clean up'''
df = get_df()

df_last_add = df.sort_values("application_date").drop_duplicates("address", keep="last")
df_last_add = df_last_add.drop(df_last_add[df_last_add["address"].isnull()].index)


''' Application Count by Year Figure'''
df_year_count = df_last_add.groupby("Year")["application_date"].count().reset_index()
df_year_count.rename(columns={"Year":"Year", "application_date":"Application Count"}, inplace=True)

fig_year = px.bar(df_year_count, x="Year", y="Application Count", color_discrete_sequence=px.colors.qualitative.Safe,
                    title="Number of New Applications Each Year")

fig_year.update_layout(
    plot_bgcolor=colors["background"],
    font_color=colors["text"]
)


''' Current Status Count Figure'''
df_status_count = df_last_add.groupby("current_status")["application_date"].count().reset_index()
df_status_count.rename(columns={"current_status":"Current Status", "application_date":"Count"}, inplace=True)

fig_status = px.bar(df_status_count, x="Current Status", y="Count", color_discrete_sequence=px.colors.qualitative.Safe)

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
            dcc.Graph(
                id='applications-by-year',
                figure=fig_year
            )], 
            style={
                "color":colors["text"],
                "textAlign":"center"         
            }),

    html.Div(children=[
            html.H2("Applications By Current Status"),
            '''
            What is the current status for rental applications submitted more recently?
            '''],
            style={
                "color":colors["text"],
                "textAlign":"center"
            }),

    html.Div(children=[
            dcc.Graph(
                id='status-count',
                figure=fig_status
            ), 

            dcc.Graph(
                id='year-status',
                figure=fig_year_status
            )], 
            style={
                "display":"flex",
                "flex-wrap":"wrap"})
])


if __name__ == '__main__':
    app.run_server(debug=True)