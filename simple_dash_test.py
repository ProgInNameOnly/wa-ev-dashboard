import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import os

app = dash.Dash(__name__)
server = app.server

df = pd.DataFrame({
    'Fruit': ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges', 'Bananas'],
    'Amount': [4, 1, 2, 2, 4, 5],
    'City': ['SF', 'SF', 'SF', 'NYC', 'NYC', 'NYC']
})

app.layout = html.Div([
    html.H1('Super Simple Test Dashboard', style={'textAlign': 'center'}),

    html.Div([
        html.H3('Static Test Chart'),
        dcc.Graph(
            figure=go.Figure(
                data=[
                    go.Bar(
                        x=['A', 'B', 'C'],
                        y=[10, 20, 30],
                        marker_color='rgb(255, 0, 0)'
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

    html.Div(style={'height': '40px'}),

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
                    'SF': 'rgb(0, 0, 255)',
                    'NYC': 'rgb(255, 165, 0)'
                }
            ).update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white'
            )
        )
    ])
])

# Force Replit-compatible port
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port, debug=True)


