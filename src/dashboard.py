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
#decade_years = list(range(df["year"].min(), df["year"].max() + 1, 10))
decade_years = list(range(df["year"].min() // 10 * 10, df["year"].max() + 1, 10))
year_slider = dcc.RangeSlider(
    id="year-slider",
    min=df["year"].min(),
    max=df["year"].max(),
    value=[df["year"].min(), df["year"].max()],
    marks={str(year): str(year) if year in decade_years else '' for year in df["year"].unique()},
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
    
    center_lat = filtered_df["latitude"].mean()
    center_lon = filtered_df["longitude"].mean()
    center = {"lat": center_lat, "lon": center_lon}

    fig = px.scatter_mapbox(
        data_frame=filtered_df,
        lat="latitude",
        lon="longitude",
        #center={"lat": 10, "lon": 0},
        center=center,
        color_discrete_sequence=["gold"],
        zoom=1.3,
        height=600,
    )
    fig.update_layout(
        mapbox_style="white-bg",
        margin={"r": 10, "t": 10, "l": 10, "b": 35},
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
        #margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )
    return fig


# Tab layouts for regional maps
tabs = dcc.Tabs(
    id="map-tabs",
    value="all",
    children=[
        dcc.Tab(label="World Wide", value="all"),
        dcc.Tab(label="I, II, III - European Atlantic, Med, W. Africa", value="I, II, III"),
        dcc.Tab(label="VIII & IX - HOA, Gulf, Indian Ocean", value="VIII, IX"),
        dcc.Tab(label="XI - SE Asia", value="XI"),
        dcc.Tab(label="IV - Carribean, W Atlantic", value="IV"),
    ],
)

# Use grid-based layout
app.layout = html.Div(
    style={
        "display": "flex",
        "align-items": "flex-start",
        "flex-direction": "column",
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
    [Output("map-graph", "figure"), Output("event-list", "children")],
    [
        Input("map-tabs", "value"),
        Input("year-slider", "value"),
        Input("map-graph", "clickData"),
    ],
)

def update_content(selected_tab, selected_years, click_data):
    if selected_tab == "all":
        nav_areas = df["navArea"].unique()
    else:
        #nav_areas = selected_tab.split(",")
        nav_areas = [area.strip() for area in selected_tab.split(",")]   


    fig = create_map_figure(df, nav_areas, year_range=selected_years)

    if click_data is not None:
        filtered_df = df[df["navArea"].isin(nav_areas)]
        if selected_years:
            filtered_df = filtered_df[
                (filtered_df["year"] >= selected_years[0])
                & (filtered_df["year"] <= selected_years[1])
            ]
        point_index = click_data["points"][0]["pointIndex"]
        if point_index < len(filtered_df):
            description = filtered_df.iloc[point_index]["description"]
            event_list = html.Div(
                description,
                style={"overflow-y": "scroll", "height": "60vh"},
            )
        else:
            event_list = html.Div(["The selected point is out of bounds for the current data"])
    else:
        event_list = html.Div(["Click on a point in the map to see its description"])

    return fig, event_list


if __name__ == "__main__":
    app.run_server(debug=True)
