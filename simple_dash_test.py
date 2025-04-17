import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# Initialize the Dash app with the custom theme
app = dash.Dash(__name__)
server = app.server

# Create some sample data
sample_data = {'x': [1, 2, 3, 4, 5], 
               'y': [10, 11, 12, 13, 14], 
               'category': ['A', 'B', 'A', 'B', 'A']}
df = pd.DataFrame(sample_data)

# Create a simple figure with a bright, high-contrast color
fig = px.bar(df, x='x', y='y', color='category', 
             color_discrete_sequence=['#FF5E5E', '#00FFB0'])

# Make sure the colors are extremely high contrast
fig.update_traces(
    marker=dict(
        line=dict(width=2, color='black'),
        opacity=1.0
    )
)

# Set layout properties for maximum visibility
fig.update_layout(
    title='Simple Test Chart',
    plot_bgcolor='#FFFFFF',
    paper_bgcolor='#03120e',
    font_color='#FFFFFF',
    font=dict(size=16),
    legend=dict(font=dict(color='#FFFFFF', size=14))
)

# Create a very simple layout with just one chart
app.layout = html.Div([
    html.H1("Dash Test Chart", style={'color': 'white', 'textAlign': 'center'}),
    
    html.Div([
        # Test Figure 1: Using the figure we created above
        html.Div([
            html.H3("Test Chart 1", style={'color': 'white'}),
            dcc.Graph(
                id='test-figure-1',
                figure=fig
            )
        ], style={'marginBottom': '20px', 'padding': '15px', 'backgroundColor': '#1a1d1a'}),
        
        # Test Figure 2: Direct dictionary definition
        html.Div([
            html.H3("Test Chart 2", style={'color': 'white'}),
            dcc.Graph(
                id='test-figure-2',
                figure={
                    'data': [
                        {
                            'x': [1, 2, 3], 
                            'y': [4, 1, 2], 
                            'type': 'bar', 
                            'name': 'Sample A',
                            'marker': {'color': '#FF0000'}
                        },
                        {
                            'x': [1, 2, 3], 
                            'y': [2, 4, 5], 
                            'type': 'bar', 
                            'name': 'Sample B',
                            'marker': {'color': '#00FF00'}
                        }
                    ],
                    'layout': {
                        'title': 'Basic Bar Chart',
                        'plot_bgcolor': '#FFFFFF',
                        'paper_bgcolor': '#03120e',
                        'font': {'color': '#FFFFFF', 'size': 14}
                    }
                }
            )
        ], style={'marginBottom': '20px', 'padding': '15px', 'backgroundColor': '#1a1d1a'})
    ], style={'maxWidth': '800px', 'margin': '0 auto'}),
], style={'backgroundColor': '#03120e', 'minHeight': '100vh', 'padding': '20px'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)