# Run this app with `python app.py` and
# visit http://127.0.0.1:2020/ in your web browser.

# Notes 

# Changing the max_rows from an int to max_rows=len(df.latitude) makes the load time longer
# as expected however the screen forces a reload every so often so an int seem preferable.

import os
from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd


df = pd.read_csv('../data/in_progress/v1_lat_long.csv')

def generate_table(dataframe, max_rows=20):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


app = Dash(__name__)

app.layout = html.Div([
    html.H4(children='Threats to Shipping', 
        style={'textAlign': 'center'}
            ), 
    generate_table(df)
    ])


if __name__ == '__main__':
    app.run_server(debug=True, port=2020)