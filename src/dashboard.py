import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

df = pd.read_pickle("../data/in_progress/pickled_data.pkl")

# Extract year from date
df["year"] = df["date"].dt.year

app = dash.Dash(__name__)

# Create a RangeSlider for years
year_slider = dcc.RangeSlider(
    id="year-slider",
    min=df["year"].min(),
    max=df["year"].max(),
    value=[df["year"].min(), df["year"].max()],
    marks={str(year): str(year) for year in df["year"].unique()},
    step=None,
)

# app.layout = html.Div([
#     dcc.Graph(id='map-graph', style={'height': '90vh'}),  # Map takes the entire height of the viewport
#     html.Div(year_slider, style={'margin': '10px'})
# ])
# app.layout = html.Div(
#     [
#         dcc.Graph(
#             id="map-graph", style={"height": "90vh"}
#         ),  # Map takes the entire height of the viewport
#         html.Div(
#             year_slider, style={"width": "100%", "margin": "10px"}
#     ]
app.layout = html.Div(
    [
        dcc.Graph(
            id="map-graph", style={"height": "90vh"}
        ),  # Map takes the entire height of the viewport
        html.Div(year_slider, style={"margin": "10px"}),
    ]
)
# )


@app.callback(Output("map-graph", "figure"), [Input("year-slider", "value")])
def update_figure(selected_years):
    filtered_df = df[
        (df["year"] >= selected_years[0]) & (df["year"] <= selected_years[1])
    ]

    fig = px.scatter_mapbox(
        data_frame=filtered_df,
        lat="latitude",
        lon="longitude",
        center={"lat": 10, "lon": 0},
        color_discrete_sequence=["gold"],
        zoom=1.3,  # Show the entire world
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
    ),

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
