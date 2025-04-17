import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# Initialize app
app = dash.Dash(__name__)

# Create a simple data frame
df = pd.DataFrame({
    'Fruit': ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges', 'Bananas'],
    'Amount': [4, 1, 2, 2, 4, 5],
    'City': ['SF', 'SF', 'SF', 'NYC', 'NYC', 'NYC']
})

# Server
server = app.server

# App layout - extraordinarily simple
app.layout = html.Div([
    # Title
    html.H1('Super Simple Test Dashboard', style={'textAlign': 'center'}),
    
    # Static hardcoded figure - should always render
    html.Div([
        html.H3('Static Test Chart'),
        dcc.Graph(
            figure=go.Figure(
                data=[
                    go.Bar(
                        x=['A', 'B', 'C'],
                        y=[10, 20, 30],
                        marker_color='rgb(255, 0, 0)'  # Pure red
                    )
                ],
                layout=go.Layout(
                    title='Basic Bar Chart',
                    plot_bgcolor='white',
                    paper_bgcolor='white'
                )
            )
        )
    ]),
    
    # Spacer
    html.Div(style={'height': '40px'}),
    
    # Simple Plotly Express chart
    html.Div([
        html.H3('Plotly Express Chart'),
        dcc.Graph(
            figure=px.bar(
                df, 
                x='Fruit', 
                y='Amount', 
                color='City',
                barmode='group',
                color_discrete_map={
                    'SF': 'rgb(0, 0, 255)',  # Pure blue
                    'NYC': 'rgb(255, 165, 0)'  # Pure orange
                }
            ).update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white'
            )
        )
    ])
])

# Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)