import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Define color scheme
COLORS = {
    'cambridge-blue': '#96BDC6',
    'charcoal': '#36454F',
    'dark-slate-gray': '#2F4F4F',
    'eerie-black': '#1A1A1A',
    'night': '#141414',
    'text': '#E0E0E0',
    'accent': '#00FFB0',  # Bright accent for visibility
}

# App initialization with dark theme
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.DARKLY],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

# Custom dark theme CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background-color: ''' + COLORS['night'] + ''';
                color: ''' + COLORS['text'] + ''';
                font-family: Arial, sans-serif;
            }
            .card {
                background-color: ''' + COLORS['eerie-black'] + ''';
                border: none;
                margin-bottom: 15px;
            }
            .card-header {
                background-color: ''' + COLORS['charcoal'] + ''';
                color: ''' + COLORS['text'] + ''';
                font-weight: bold;
            }
            h1, h2, h3, h4, h5, h6 {
                color: ''' + COLORS['cambridge-blue'] + ''';
            }
            .custom-tabs {
                background-color: ''' + COLORS['dark-slate-gray'] + ''';
                padding: 10px;
                border-radius: 5px;
            }
            .custom-tab {
                color: ''' + COLORS['text'] + ''';
                background-color: ''' + COLORS['eerie-black'] + ''';
                border-color: ''' + COLORS['charcoal'] + ''';
                border-radius: 5px;
                padding: 10px 15px;
                margin-right: 5px;
            }
            .custom-tab--selected {
                background-color: ''' + COLORS['charcoal'] + ''';
                color: ''' + COLORS['accent'] + ''';
                font-weight: bold;
            }
            /* Alternative approach for tabs */
            .dash-tab {
                background-color: ''' + COLORS['eerie-black'] + ''' !important;
                color: ''' + COLORS['text'] + ''' !important;
            }
            .dash-tab--selected {
                background-color: ''' + COLORS['charcoal'] + ''' !important;
                color: ''' + COLORS['accent'] + ''' !important;
                border-top: 2px solid ''' + COLORS['accent'] + ''' !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Load the data
def load_data():
    try:
        df = pd.read_csv('attached_assets/Electric_Vehicle_Population_Data.csv')
        # Basic preprocessing
        df['Model Year'] = pd.to_numeric(df['Model Year'], errors='coerce')
        df = df.dropna(subset=['Model Year'])
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        # Return a minimal dataframe to prevent app crash
        return pd.DataFrame({
            'Make': ['Data Load Error'], 
            'Model': ['Check Console'], 
            'Model Year': [2023],
            'Electric Vehicle Type': ['Error'],
            'County': ['Error']
        })

# Function to generate Plotly HTML that works in this environment
def generate_chart_html(fig):
    fig.update_layout(
        paper_bgcolor=COLORS['eerie-black'],
        plot_bgcolor=COLORS['dark-slate-gray'],
        font_color=COLORS['text'],
        margin=dict(l=30, r=30, t=50, b=30),
    )
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

# Create a dashboard layout with HTML-injection approach for charts
def create_dashboard_layout():
    df = load_data()
    
    # 1. Create top makes chart
    make_counts = df['Make'].value_counts().head(10).reset_index()
    make_counts.columns = ['Make', 'Count']
    
    fig1 = px.bar(
        make_counts,
        x='Count',
        y='Make',
        orientation='h',
        title='Top 10 EV Manufacturers'
    )
    fig1.update_traces(marker=dict(color=COLORS['accent']))
    
    # 2. Create top models chart
    model_counts = df.groupby(['Make', 'Model']).size().reset_index(name='Count')
    model_counts = model_counts.sort_values('Count', ascending=False).head(10)
    model_counts['Full Model'] = model_counts['Make'] + ' ' + model_counts['Model']
    
    fig2 = px.bar(
        model_counts,
        x='Count',
        y='Full Model',
        orientation='h',
        title='Top 10 EV Models'
    )
    fig2.update_traces(marker=dict(color=COLORS['cambridge-blue']))
    
    # 3. Create county distribution chart
    county_counts = df['County'].value_counts().head(15).reset_index()
    county_counts.columns = ['County', 'Count']
    
    fig3 = px.bar(
        county_counts,
        x='County',
        y='Count',
        title='EV Distribution by County'
    )
    fig3.update_traces(marker=dict(color=COLORS['accent']))
    fig3.update_layout(xaxis_tickangle=-45)
    
    # 4. Create EV type distribution chart
    ev_type_counts = df['Electric Vehicle Type'].value_counts().reset_index()
    ev_type_counts.columns = ['Type', 'Count']
    
    fig4 = go.Figure(data=[go.Pie(
        labels=ev_type_counts['Type'],
        values=ev_type_counts['Count'],
        marker=dict(colors=[COLORS['accent'], COLORS['cambridge-blue']])
    )])
    fig4.update_layout(title='EV Type Distribution')
    
    # 5. Create year trend chart
    year_counts = df.groupby('Model Year').size().reset_index(name='Count')
    year_counts = year_counts.sort_values('Model Year')
    
    fig5 = px.line(
        year_counts,
        x='Model Year',
        y='Count',
        title='EV Adoption by Year'
    )
    fig5.update_traces(line=dict(color=COLORS['accent']), mode='lines+markers')
    
    # Create layout with HTML-injected charts
    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Washington State EV Population Dashboard", className="text-center my-4"), width=12)
        ]),
        
        dbc.Row([
            dbc.Col(html.H4("Comprehensive Analysis of Electric Vehicle Population Data", className="text-center mb-4"), width=12)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Top EV Manufacturers"),
                    dbc.CardBody(html.Div([
                        html.Iframe(srcDoc=generate_chart_html(fig1), style={'width': '100%', 'height': '400px', 'border': 'none'})
                    ]))
                ])
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Top EV Models"),
                    dbc.CardBody(html.Div([
                        html.Iframe(srcDoc=generate_chart_html(fig2), style={'width': '100%', 'height': '400px', 'border': 'none'})
                    ]))
                ])
            ], width=6)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("County Distribution"),
                    dbc.CardBody(html.Div([
                        html.Iframe(srcDoc=generate_chart_html(fig3), style={'width': '100%', 'height': '400px', 'border': 'none'})
                    ]))
                ])
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("EV Type Distribution"),
                    dbc.CardBody(html.Div([
                        html.Iframe(srcDoc=generate_chart_html(fig4), style={'width': '100%', 'height': '400px', 'border': 'none'})
                    ]))
                ])
            ], width=6)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("EV Adoption Trend"),
                    dbc.CardBody(html.Div([
                        html.Iframe(srcDoc=generate_chart_html(fig5), style={'width': '100%', 'height': '400px', 'border': 'none'})
                    ]))
                ])
            ], width=12)
        ]),
        
        dbc.Row([
            dbc.Col(html.P("Data source: Electric Vehicle Population Data from Washington State Department of Licensing", 
                           className="text-center text-muted mt-4"), 
                    width=12)
        ])
    ], 
    fluid=True,
    style={"backgroundColor": COLORS['night']})

# Set up the app layout
app.layout = create_dashboard_layout()

# Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)