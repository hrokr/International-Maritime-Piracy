import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly_express as px

df = pd.read_pickle("../data/in_progress/pickled_data.pkl")

# Extract year from date
df['year'] = df['date'].dt.year

app = dash.Dash(__name__)

# Create a RangeSlider for years
year_slider = dcc.RangeSlider(
    id='year-slider',
    min=df['year'].min(),
    max=df['year'].max(),
    value=[df['year'].min(), df['year'].max()],
    marks={str(year): str(year) for year in df['year'].unique()},
    step=None
)

app.layout = html.Div([
    dcc.Graph(id='map-graph', style={'height': '90vh'}),  # Map takes the entire height of the viewport
    html.Div(year_slider, style={'margin': '10px'})
])

@app.callback(
    Output('map-graph', 'figure'),
    [Input('year-slider', 'value')]
)
def update_figure(selected_years):
    filtered_df = df[(df['year'] >= selected_years[0]) & (df['year'] <= selected_years[1])]

    fig = px.scatter_geo(
        data_frame=filtered_df,
        lat="latitude",
        lon="longitude",
        color_discrete_sequence=["gold"],
        projection="natural earth"  # Use the Natural Earth projection
    )

    fig.update_layout(
        autosize=True,
        hovermode='closest',
        geo=dict(
            showland=True,  # default land mass
            landcolor="rgb(243, 243, 243)",
            countrycolor="rgb(204, 204, 204)",
        ),
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

