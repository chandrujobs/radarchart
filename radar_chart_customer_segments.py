import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the dataset
data = pd.read_excel("C:/Users/Chandru/OneDrive/Desktop/Python Visuals/Sample - Superstore.xls", sheet_name="Orders")

# Data preparation for radar chart
segment_performance = data.groupby('Segment').agg({'Sales': 'sum', 'Discount': 'mean', 'Profit': 'mean'}).reset_index()

# Normalize the numeric data for radar chart
numeric_data = segment_performance.select_dtypes(include=[float, int])
normalized_data = (numeric_data - numeric_data.min()) / (numeric_data.max() - numeric_data.min())

# Add 'Segment' back to the normalized DataFrame
normalized_data['Segment'] = segment_performance['Segment']

# Create a Dash application
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    dcc.Dropdown(
        id='segment-dropdown',
        options=[{'label': segment, 'value': segment} for segment in normalized_data['Segment'].unique()],
        value=normalized_data['Segment'].unique(),
        multi=True
    ),
    dcc.Graph(id='radar-chart')
])

# Define callback to update graph
@app.callback(
    Output('radar-chart', 'figure'),
    [Input('segment-dropdown', 'value')]
)
def update_graph(selected_segments):
    filtered_data = normalized_data[normalized_data['Segment'].isin(selected_segments)]
    fig = px.line_polar(filtered_data, r='Sales', theta='Segment', line_close=True)
    fig.update_traces(fill='toself')
    fig.update_layout(title='Customer Segment Performance Metrics')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8056)
