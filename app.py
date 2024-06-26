import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import base64
import io

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server  # Expose the server variable for deployments

# Define the layout of the Dash app
app.layout = html.Div([
    html.H1("Data Visualization Tool", style={'textAlign': 'center', 'color': '#4CAF50'}),
    html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px',
                'backgroundColor': '#f9f9f9'
            },
            multiple=False
        ),
        html.Div(id='output-data-upload', style={'marginTop': '20px'}),
        dcc.Dropdown(id='x-column', placeholder='Select X Column', style={'marginTop': '10px'}),
        dcc.Dropdown(id='y-column', placeholder='Select Y Column', style={'marginTop': '10px'}),
        dcc.Dropdown(
            id='plot-type',
            options=[
                {'label': 'Scatter', 'value': 'scatter'},
                {'label': 'Histogram', 'value': 'histogram'},
                {'label': 'Box', 'value': 'box'}
            ],
            placeholder='Select Plot Type',
            style={'marginTop': '10px'}
        ),
        html.Button('Visualize', id='visualize-button', style={'marginTop': '10px', 'backgroundColor': '#4CAF50', 'color': 'white'}),
        dcc.Graph(id='output-graph', style={'marginTop': '20px'})
    ], style={'width': '50%', 'margin': 'auto'})
])

# Callback to handle file upload and data processing
@app.callback(
    Output('output-data-upload', 'children'),
    Output('x-column', 'options'),
    Output('y-column', 'options'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_output(contents, filename):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        options = [{'label': col, 'value': col} for col in df.columns]
        return html.Div([
            html.H5(filename),
            html.H6('Data uploaded successfully.'),
            html.Pre(df.head().to_string())
        ]), options, options
    return html.Div(), [], []

# Callback to generate visualizations
@app.callback(
    Output('output-graph', 'figure'),
    Input('visualize-button', 'n_clicks'),
    State('upload-data', 'contents'),
    State('x-column', 'value'),
    State('y-column', 'value'),
    State('plot-type', 'value')
)
def update_graph(n_clicks, contents, x_column, y_column, plot_type):
    if n_clicks is not None and contents is not None and x_column and y_column and plot_type:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        if plot_type == 'scatter':
            fig = px.scatter(df, x=x_column, y=y_column)
        elif plot_type == 'histogram':
            fig = px.histogram(df, x=x_column)
        elif plot_type == 'box':
            fig = px.box(df, x=x_column, y=y_column)
        return fig
    return {}

if __name__ == '__main__':
    app.run_server(debug=True)


    
   


          




