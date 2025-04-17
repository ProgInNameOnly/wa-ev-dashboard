import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import io
import base64
import matplotlib.pyplot as plt
import numpy as np

# Initialize the app with a bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Set the server port for proper deployment in Replit
server = app.server

# Function to create a matplotlib figure and convert to base64 for display
def create_figure():
    # Create a figure with a white background
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    # Simple bar chart data
    categories = ['Category A', 'Category B', 'Category C']
    values = [25, 40, 30]
    
    # Create bars with explicit colors
    bars = ax.bar(categories, values, color=['red', 'blue', 'green'])
    
    # Add labels and title
    ax.set_xlabel('Categories', fontsize=14)
    ax.set_ylabel('Values', fontsize=14)
    ax.set_title('Basic Bar Chart - Matplotlib', fontsize=16)
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2., height + 1,
            f'{height}',
            ha='center', va='bottom', fontsize=12
        )
    
    # Add grid for better readability
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Save figure to a PNG image in memory
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    
    # Encode the image to base64 string
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    return f'data:image/png;base64,{img_str}'

# Function to create a simple top makes chart
def create_top_makes_chart():
    try:
        # Load data
        df = pd.read_csv('attached_assets/Electric_Vehicle_Population_Data.csv')
        
        # Get top makes
        top_makes = df['Make'].value_counts().head(10)
        
        # Create figure with white background
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')
        
        # Create horizontal bar chart with bright colors
        bars = ax.barh(top_makes.index, top_makes.values, color='crimson')
        
        # Add labels and title
        ax.set_xlabel('Number of Vehicles', fontsize=14)
        ax.set_ylabel('Manufacturer', fontsize=14)
        ax.set_title('Top 10 EV Manufacturers', fontsize=16)
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            ax.text(
                width + 0.5, bar.get_y() + bar.get_height()/2.,
                f'{width:,}',
                ha='left', va='center', fontsize=12
            )
        
        # Invert y-axis to show most common at the top
        ax.invert_yaxis()
        
        # Add grid for better readability
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        
        # Save figure to a PNG image in memory
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        
        # Encode the image to base64 string
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        return f'data:image/png;base64,{img_str}'
    except Exception as e:
        print(f"Error creating top makes chart: {e}")
        # Create a simple error image
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')
        ax.text(0.5, 0.5, f"Error loading data: {e}", ha='center', va='center', fontsize=14)
        ax.axis('off')
        
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        return f'data:image/png;base64,{img_str}'

# App layout
app.layout = dbc.Container([
    html.H1("Matplotlib Charts in Dash", 
            style={'color': 'black', 'textAlign': 'center', 'marginTop': '20px'}),
    
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H3("Basic Bar Chart"),
                html.Img(src=create_figure(), style={'width': '100%'})
            ], style={'padding': '15px', 'backgroundColor': 'white', 'borderRadius': '5px'})
        ], width=12, lg=6),
        
        dbc.Col([
            html.Div([
                html.H3("Top EV Manufacturers"),
                html.Img(src=create_top_makes_chart(), style={'width': '100%'})
            ], style={'padding': '15px', 'backgroundColor': 'white', 'borderRadius': '5px'})
        ], width=12, lg=6)
    ], className="mb-4"),
    
], fluid=True, style={'backgroundColor': '#f5f5f5', 'minHeight': '100vh', 'padding': '20px'})

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)