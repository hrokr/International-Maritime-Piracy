import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

df = pd.read_pickle("../data/in_progress/pickled_data.pkl")
df["year"] = df["date"].dt.year

app = dash.Dash(__name__)

# RangeSlider for main map
year_slider = dcc.RangeSlider(
    id="year-slider",
    min=df["year"].min(),
    max=df["year"].max(),
    value=[df["year"].min(), df["year"].max()],
    marks={str(year): str(year) for year in df["year"].unique()},
    step=None,
)

# Create map figures based on input data and options
def create_map_figure(df, nav_areas, year_range=None):
    filtered_df = df[df["navArea"].isin(nav_areas)]

    if year_range:
        filtered_df = filtered_df[
            (filtered_df["year"] >= year_range[0])
            & (filtered_df["year"] <= year_range[1])
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


# Tab layouts for regional maps
tabs = dcc.Tabs(
    id="map-tabs",
    value="all",
    children=[
        dcc.Tab(label="All Areas", value="all"),
        dcc.Tab(label="I, II, & III", value="123"),
        dcc.Tab(label="VII & IX", value="79"),
        dcc.Tab(label="XI", value="11"),
        dcc.Tab(label="IV", value="4"),
    ],
)

# Use grid-based layout
app.layout = html.Div(
    style={
        "display": "flex",
        "align-items": "flex-start",
    },  # Apply flexbox to the main layout
    children=[
        html.Div(
            [
                tabs,
                dcc.Graph(id="map-graph", style={"height": "60vh"}),
                year_slider,
            ],
            style={"flex": "66%"},
        ),
        html.Div(
            id="event-list",
            style={"flex": "33%", "overflow-y": "scroll", "height": "60vh"},
        ),
    ],
)


## Callbacks

# Update the map based on selected tab and year slider
@app.callback(
    Output("map-graph", "figure"),
    [Input("map-tabs", "value"), Input("year-slider", "value")],
)
def update_map(selected_tab, selected_years):
    if selected_tab == "all":
        nav_areas = df["navArea"].unique()
    else:
        nav_areas = [int(area) for area in selected_tab]
    return create_map_figure(df, nav_areas, year_range=selected_years)


@app.callback(
    Output("event-list", "children"),
    [Input("map-graph", "clickData")],
)
def display_events(click_data):
    if click_data:
        point_index = click_data["points"][0]["pointIndex"]
        description = df.iloc[point_index]["description"]
        return html.Div(
            description,
            style={"overflow-y": "scroll", "height": "60vh"},  # Add scrollbar and height
        )
    else:
        return html.Div(["Click on a point in the map to see its description"])


if __name__ == "__main__":
    app.run_server(debug=True)
