# Run this app with `python app.py` and
# visit http://127.0.0.1:2030/ in your web browser.

# Notes 

# Changing the max_rows from an int to max_rows=len(df.latitude) makes the load time longer
# as expected however the screen forces a reload every so often so an int seem preferable.

import os
from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd

app = Dash(__name__)

df = pd.read_csv('../data/in_progress/v1_lat_long.csv')


fig = px.scatter(df, x="navArea", y="subreg",
                 size="year", color="navArea", hover_name="description",
                 log_x=False, size_max=100)

app.layout = html.Div([
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, port=2030)