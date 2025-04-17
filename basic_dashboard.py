import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Initialize the app with a bold theme
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

# Set the server port for proper deployment in Replit
server = app.server

# Load data
def load_data():
    try:
        # Load the data
        df = pd.read_csv('attached_assets/Electric_Vehicle_Population_Data.csv')
        
        # Simple preprocessing
        # Convert model year to numeric, handling errors
        df['Model Year'] = pd.to_numeric(df['Model Year'], errors='coerce')
        
        # Drop rows with missing Model Year
        df = df.dropna(subset=['Model Year'])
        
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        # Return a small sample for testing
        return pd.DataFrame({
            'Make': ['TESLA', 'NISSAN', 'CHEVROLET'],
            'Model': ['MODEL 3', 'LEAF', 'BOLT'],
            'Model Year': [2020, 2019, 2021]
        })

# Load the data
df = load_data()

# Super simple layout with just two charts
app.layout = dbc.Container([
    html.H1("EV Dashboard with Basic Charts", 
            style={'color': 'black', 'textAlign': 'center', 'marginTop': '20px'}),
    
    html.Div([
        html.H3("Test Chart 1 - Basic Bar Chart"),
        dcc.Graph(
            id='test-chart-1',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [40, 10, 20], 'type': 'bar', 'name': 'Car A',
                     'marker': {'color': 'red'}},
                    {'x': [1, 2, 3], 'y': [20, 40, 30], 'type': 'bar', 'name': 'Car B',
                     'marker': {'color': 'blue'}}
                ],
                'layout': {
                    'title': 'Basic Test Chart',
                    'paper_bgcolor': 'white',
                    'plot_bgcolor': 'white',
                    'font': {'color': 'black', 'size': 14},
                    'height': 400,
                }
            }
        )
    ], style={'marginBottom': '30px', 'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '5px', 'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)'}),
    
    html.Div([
        html.H3("Top Makes"),
        dcc.Graph(id='top-makes')
    ], style={'marginBottom': '30px', 'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '5px', 'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)'})
    
], fluid=True, style={'backgroundColor': '#f5f5f5', 'minHeight': '100vh', 'padding': '20px'})

# Callback to populate the Top Makes chart
@app.callback(
    Output('top-makes', 'figure'),
    Input('test-chart-1', 'clickData')  # This input won't actually be used
)
def update_top_makes(_):
    # Get top makes
    make_counts = df['Make'].value_counts().head(10).reset_index()
    make_counts.columns = ['Make', 'Count']
    
    # Create a simple bar chart with clear colors and no color gradients
    fig = px.bar(
        make_counts,
        x='Count',
        y='Make',
        orientation='h',
        labels={'Count': 'Number of Vehicles', 'Make': 'Manufacturer'},
        title='Top 10 EV Manufacturers',
        color_discrete_sequence=['red'] * len(make_counts)  # Force all bars to be red
    )
    
    # Further ensure visibility with explicit styling
    fig.update_traces(
        marker=dict(
            color='red',
            opacity=1.0,
            line=dict(width=1, color='black')
        ),
        texttemplate='%{x:,}',
        textposition='outside',
        textfont=dict(
            size=14,
            color='black'
        )
    )
    
    # Light theme styling
    fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        font_color='black',
        title_font_size=20,
        xaxis=dict(
            title_font=dict(size=16),
            tickfont=dict(size=14),
            gridcolor='lightgray'
        ),
        yaxis=dict(
            title_font=dict(size=16),
            tickfont=dict(size=14)
        ),
        margin=dict(l=10, r=10, t=50, b=10),
    )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)