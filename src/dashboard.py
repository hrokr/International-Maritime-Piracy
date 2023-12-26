import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px


def load_data():
    """Load and preprocess data."""
    df = pd.read_pickle("../data/in_progress/pickled_data.pkl")
    df["year"] = df["date"].dt.year
    return df


def create_app():
    """Create and configure the Dash app."""
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    df = load_data()

    year_slider = dcc.RangeSlider(
        id="year-slider",
        min=df["year"].min(),
        max=df["year"].max(),
        value=[df["year"].min(), df["year"].max()],
        marks={
            str(year): str(year) if year % 10 == 0 else "" for year in df["year"].unique()
        },
        step=None,
    )

    navarea_dropdown = dcc.Dropdown(
        id="navarea-dropdown",
        options=[{"label": i, "value": i} for i in df["navArea"].unique()],
        value=df["navArea"].unique().tolist(),
        multi=True,
    )

    subregion_dropdown = dcc.Dropdown(
        id="subregion-dropdown",
        options=[{"label": i, "value": i} for i in df["subreg"].unique()],
        value=df["subreg"].unique().tolist(),
        multi=True,
    )

    app.layout = dbc.Container(
        [
            dbc.Row(dcc.Graph(id="map-graph", style={"height": "70vh"})),
            dbc.Row(year_slider, style={"width": "100%", "margin": "10px"}),
            dbc.Row(
                [
                    dbc.Col(navarea_dropdown),
                    dbc.Col(subregion_dropdown),
                ]
            ),
        ]
    )

    @app.callback(
        Output("map-graph", "figure"),
        [
            Input("year-slider", "value"),
            Input("navarea-dropdown", "value"),
            Input("subregion-dropdown", "value"),
        ],
    )
    def update_figure(selected_years, selected_navarea, selected_subregion):
        filtered_df = df[
            (df["year"] >= selected_years[0]) & (df["year"] <= selected_years[1])
        ]
        filtered_df = filtered_df[
            (filtered_df["navArea"].isin(selected_navarea))
            | (filtered_df["subreg"].isin(selected_subregion))
        ]

        fig = px.scatter_mapbox(
            data_frame=filtered_df,
            lat="latitude",
            lon="longitude",
            center={"lat": 10, "lon": 0},
            color_discrete_sequence=["gold"],
            zoom=1.3,
            height=600,
        )

        fig.update_layout(
            mapbox_style="white-bg",
            mapbox_layers=[
                {
                    "below": "traces",
                    "sourcetype": "raster",
                    "sourceattribution": "United States Geological Survey",
                    "source": [
                        "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                    ],
                }
            ],
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
        )

        return fig

    return app


if __name__ == "__main__":
    app = create_app()
    app.run_server(debug=True)
