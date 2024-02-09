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
# decade_years = list(range(df["year"].min(), df["year"].max() + 1, 10))
decade_years = list(range(df["year"].min() // 10 * 10, df["year"].max() + 1, 10))
year_slider = dcc.RangeSlider(
    id="year-slider",
    min=df["year"].min(),
    max=df["year"].max(),
    value=[df["year"].min(), df["year"].max()],
    marks={
        str(year): str(year) if year in decade_years else ""
        for year in df["year"].unique()
    },
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
        # center={"lat": 10, "lon": 0},
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
        # margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )
    return fig


# Tab layouts for regional maps
tabs = dcc.Tabs(
    id="map-tabs",
    value="all",
    children=[
        dcc.Tab(label="World Wide", value="all"),
        dcc.Tab(
            label="I, II, III - European Atlantic, Med, W. Africa", value="I, II, III"
        ),
        dcc.Tab(label="VIII & IX - HOA, Gulf, Indian Ocean", value="VIII, IX"),
        dcc.Tab(label="XI - SE Asia", value="XI"),
        dcc.Tab(label="IV - Carribean, W Atlantic", value="IV"),
    ],
)

# Use grid-based layout
app.layout = html.Div(
    # New outer Div with styling
    style={
        "display": "flex",
        "align-items": "flex-start",
        "flex-direction": "column",
        "border": "1px solid #33313C",  # Border
        "background-color": "#E0E0E0",  # Background color
        "padding": "10px",  # Optional padding
    },
    children=[
        html.Div(
            [
                tabs,
                html.Div(
                    [
                        dcc.Graph(
                            id="map-graph",
                            style={"height": "60vh"},
                        ),
                    ],
                    style={"margin-top": "10px"},  # Example spacing above the map
                ),
                html.Div(
                    [
                        year_slider,
                    ],
                    style={"margin-top": "10px"},  # Example spacing below the tabs
                ),
            ],
            style={"flex": "66%", "width": "calc(100% - 30px)"},  # Updated style
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
        nav_areas = [area.strip() for area in selected_tab.split(",")]

    # Filter data based on selected tab and year range
    filtered_df = df[df["navArea"].isin(nav_areas)]
    if selected_years:
        filtered_df = filtered_df[
            (filtered_df["year"] >= selected_years[0])
            & (filtered_df["year"] <= selected_years[1])
        ]

    # Create map figure
    center_lat = filtered_df["latitude"].mean()
    center_lon = filtered_df["longitude"].mean()
    center = {"lat": center_lat, "lon": center_lon}

    fig = px.scatter_mapbox(
        data_frame=filtered_df,
        lat="latitude",
        lon="longitude",
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
    )

    # Update event list based on clicked point
    if click_data is not None:
        point_index = click_data["points"][0]["pointIndex"]
        if point_index < len(filtered_df):
            selected_point = filtered_df.iloc[point_index]
            description = f"Description for point {point_index + 1}:\n"

            # Use available columns to describe the point
            if "victim" in selected_point:
                description += f"- Victim: {selected_point['victim']}\n"
            if "date" in selected_point:
                description += f"- Date: {selected_point['date']}\n"
            if "description" in selected_point:
                description += f"- Brief Description: {selected_point['description']}\n"
            # Add more details using other relevant columns as needed

            event_list = html.Div(
                description,
                style={
                    "width": "calc(100% - 30px)",
                    "overflow-y": "scroll",
                    "height": "60vh",
                },
            )
        else:
            event_list = html.Div(
                ["The selected point is out of bounds for the current data"]
            )
    else:
        event_list = html.Div(["Click on a point in the map to see its description"])

    return fig, event_list


if __name__ == "__main__":
    app.run_server(debug=True)
