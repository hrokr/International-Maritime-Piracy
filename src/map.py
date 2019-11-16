import pandas as pd 
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('../data/data_pipe.csv', sep='|', encoding='utf8', index_col=False, error_bad_lines=False)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Maritime Piracy'



#putting the map on hold
fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", hover_name="date",
                        color_discrete_sequence=["orange"],zoom=1.42, height=900)
fig.update_layout(
    mapbox_style="white-bg",
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        }
      ])
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()


def generate_table(dataframe, max_rows=5):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )




app.layout = html.Div([
    dcc.RangeSlider(
        id='my-range-slider',
        min=0,
        max=20,
        step=0.5,
        value=[5, 15]
    ),
    html.Div(id='output-container-range-slider'),

    html.H4(children='Internation Maritime Priacy'),
    generate_table(df)

])



# to here

# callback for the range slider
@app.callback(
    dash.dependencies.Output('output-container-range-slider', 'children'),
    [dash.dependencies.Input('my-range-slider', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)

# callback for the range slider






# Range slider with marks

# dcc.RangeSlider(
#     marks={i: 'Label {}'.format(i) for i in range(-5, 7)},
#     min=-5,
#     max=6,
#     value=[-3, 4]
# ) 


# Range slider w/o marks





if __name__ == '__main__':
    app.run_server(debug=True)
