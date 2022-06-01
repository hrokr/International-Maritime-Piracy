
import numpy as np
import pandas as pd

from dash import Dash, dcc, html, Input, Output

import plotly.graph_objects as go
import plotly.express as px


app = Dash(__name__)


df = pd.read_csv('../data/in_progress/v1_lat_long.csv')

fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_name= "date", hover_data=["navArea", "year"],
                        color_discrete_sequence=["orange"], zoom=1, height=800)
fig.update_layout(
    mapbox_style="white-bg",
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        }
      ])
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

