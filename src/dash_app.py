import pandas as pd

from dash import Dash
import plotly_express as px

df = pd.read_pickle("../data/in_progress/pickled_data.pkl")
app = Dash(__name__)


fig = px.scatter_mapbox(
    data_frame=df,
    lat="latitude",
    lon="longitude",
    mapbox_style="carto-darkmatter",
    color_discrete_sequence=["gold"],
)
fig.show()
