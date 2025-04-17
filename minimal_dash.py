import dash
from dash import html, dcc
import plotly.graph_objects as go

# Create a simple bar chart figure
fig = go.Figure(
    data=[
        go.Bar(
            x=[1, 2, 3],
            y=[10, 20, 30],
            marker_color='red'
        )
    ]
)

# Update layout for maximum visibility
fig.update_layout(
    title='Red Bar Chart',
    paper_bgcolor='white',
    plot_bgcolor='white',
    font_color='black'
)

# Initialize app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1('Minimal Dash App with One Chart'),
    dcc.Graph(
        id='example-graph',
        figure=fig
    )
], style={'backgroundColor': 'white', 'padding': '20px'})

# Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)