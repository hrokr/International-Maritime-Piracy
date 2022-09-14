import pandas as pd

from dash import Dash
import plotly_express as px

df = pd.read_pickle("../data/in_progress/pickled_data.pkl")
app = Dash(__name__)

# world map element
fig = px.scatter_mapbox(
    data_frame=df,
    lat="latitude",
    lon="longitude",
    mapbox_style="white-bg",
    zoom=1,
    color_discrete_sequence=["gold"],
)

fig.update_layout(
    mapbox_style="white-bg",
    mapbox_layers=[
        {
            "below": "traces",
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": [
                """https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/
                MapServer/tile/{z}/{y}/{x}"""
            ],
        }
    ],
)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

fig.show()
