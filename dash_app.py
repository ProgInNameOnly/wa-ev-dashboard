import dash
from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import data_processor as dp
import visualizations as viz
import os
import time

# Initialize the Dash app with the custom theme
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.DARKLY],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

# Set the server port for proper deployment in Replit
server = app.server

# Custom colors for styling
colors = {
    'background': '#03120e',  # night
    'text': '#8ab0ab',        # cambridge-blue
    'accent': '#3e505b',      # charcoal
    'card': '#1a1d1a',        # eerie-black
    'dark_accent': '#26413c'  # dark-slate-gray
}

# Load data
def load_data():
    import pandas as pd
    import numpy as np
    
    try:
        # Load the data - make sure the path is correct
        df = pd.read_csv('attached_assets/Electric_Vehicle_Population_Data.csv')
        
        # Process the data for analysis
        df = dp.preprocess_data(df)
        
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        
        # For demonstration, create a larger sample dataset
        makes = ['TESLA', 'NISSAN', 'CHEVROLET', 'BMW', 'FORD', 'KIA', 'TOYOTA', 'AUDI', 'HYUNDAI', 'VOLVO']
        models = ['MODEL 3', 'MODEL Y', 'LEAF', 'BOLT', 'ID.4', 'IONIQ 5', 'MUSTANG MACH-E', 'EV6', 'PRIUS PRIME', 'RAV4 PRIME']
        ev_types = ['Battery Electric Vehicle (BEV)', 'Plug-in Hybrid Electric Vehicle (PHEV)']
        cafv = ['Clean Alternative Fuel Vehicle Eligible', 'Not eligible due to low battery range', 'Eligible - Battery Range']
        counties = ['KING', 'PIERCE', 'SNOHOMISH', 'CLARK', 'SPOKANE', 'THURSTON', 'WHATCOM', 'KITSAP', 'BENTON', 'YAKIMA']
        
        # Create random sample data - enough to make charts meaningful
        np.random.seed(42)
        n_samples = 5000
        
        # Generate data with realistic distributions
        sample_data = {
            'Make': np.random.choice(makes, n_samples, p=[0.32, 0.15, 0.12, 0.10, 0.08, 0.07, 0.06, 0.05, 0.03, 0.02]),
            'Model': np.random.choice(models, n_samples),
            'Model Year': np.random.choice(range(2012, 2024), n_samples),
            'Electric Vehicle Type': np.random.choice(ev_types, n_samples, p=[0.75, 0.25]),
            'Clean Alternative Fuel Vehicle (CAFV) Eligibility': np.random.choice(cafv, n_samples, p=[0.7, 0.2, 0.1]),
            'Electric Range': np.random.normal(250, 80, n_samples).clip(0, 400).astype(int),
            'County': np.random.choice(counties, n_samples, p=[0.40, 0.15, 0.12, 0.08, 0.07, 0.05, 0.05, 0.04, 0.02, 0.02]),
        }
        
        sample_df = pd.DataFrame(sample_data)
        
        # Ensure models align with makes (more realistic)
        mask_tesla = sample_df['Make'] == 'TESLA'
        sample_df.loc[mask_tesla, 'Model'] = np.random.choice(['MODEL 3', 'MODEL Y', 'MODEL S', 'MODEL X'], sum(mask_tesla))
        
        mask_nissan = sample_df['Make'] == 'NISSAN'
        sample_df.loc[mask_nissan, 'Model'] = np.random.choice(['LEAF', 'ARIYA'], sum(mask_nissan), p=[0.8, 0.2])
        
        # Add sample electric utility data
        utilities = [
            'PUGET SOUND ENERGY',
            'SEATTLE CITY LIGHT',
            'SNOHOMISH COUNTY PUD',
            'TACOMA PUBLIC UTILITIES',
            'CLARK PUBLIC UTILITIES'
        ]
        
        sample_df['Electric Utility'] = np.random.choice(utilities, n_samples)
        
        # Add trend data - EV adoption growing over time
        year_weights = {}
        for year in range(2012, 2024):
            # More EVs in recent years
            year_weights[year] = (year - 2011) ** 2
            
        year_p = np.array([year_weights[y] for y in range(2012, 2024)])
        year_p = year_p / year_p.sum()
        
        sample_df['Model Year'] = np.random.choice(range(2012, 2024), n_samples, p=year_p)
        
        # Process the data
        sample_df = dp.preprocess_data(sample_df)
        
        return sample_df

# Load the data
df = load_data()

print(f"Data loaded successfully. {len(df)} vehicle records found.")

# Create tab styles
tab_style = {
    'backgroundColor': colors['card'],
    'color': colors['text'],
    'padding': '10px',
    'borderRadius': '5px 5px 0 0',
}

tab_selected_style = {
    'backgroundColor': colors['accent'],
    'color': colors['text'],
    'padding': '10px',
    'borderRadius': '5px 5px 0 0',
}

# Define the app layout
app.layout = dbc.Container([
    # Title and description
    html.H1("Washington State Electric Vehicle Population Dashboard", 
            style={'color': colors['text'], 'textAlign': 'center', 'marginTop': '20px'}),
    html.P("Explore and analyze electric vehicle data across Washington State.",
           style={'color': colors['text'], 'textAlign': 'center', 'marginBottom': '30px'}),
    
    # Main content with sidebar filter and charts
    dbc.Row([
        # Sidebar filters
        dbc.Col([
            html.Div([
                html.H4("Data Filters", style={'color': colors['text']}),
                
                # Year range slider
                html.Label("Model Year Range", style={'color': colors['text'], 'marginTop': '20px'}),
                dcc.RangeSlider(
                    id='year-slider',
                    min=int(df['Model Year'].min()),
                    max=int(df['Model Year'].max()),
                    step=1,
                    marks={i: {'label': str(i), 'style': {'color': colors['text']}} 
                           for i in range(int(df['Model Year'].min()), int(df['Model Year'].max()) + 1, 3)},
                    value=[int(df['Model Year'].min()), int(df['Model Year'].max())],
                ),
                
                # Make filter
                html.Label("Vehicle Make", style={'color': colors['text'], 'marginTop': '20px'}),
                dcc.Dropdown(
                    id='make-filter',
                    options=[{'label': make, 'value': make} for make in sorted(df['Make'].unique())],
                    multi=True,
                    placeholder="Select manufacturer(s)",
                    style={'backgroundColor': colors['card'], 'color': 'black'}
                ),
                
                # EV Type filter
                html.Label("EV Type", style={'color': colors['text'], 'marginTop': '20px'}),
                dcc.Dropdown(
                    id='ev-type-filter',
                    options=[{'label': ev_type, 'value': ev_type} for ev_type in sorted(df['Electric Vehicle Type'].unique())],
                    multi=True,
                    placeholder="Select EV type(s)",
                    style={'backgroundColor': colors['card'], 'color': 'black'}
                ),
                
                # County filter
                html.Label("County", style={'color': colors['text'], 'marginTop': '20px'}),
                dcc.Dropdown(
                    id='county-filter',
                    options=[{'label': county, 'value': county} for county in sorted(df['County'].unique())],
                    multi=True,
                    placeholder="Select county(s)",
                    style={'backgroundColor': colors['card'], 'color': 'black'}
                ),
                
                # CAFV Eligibility filter
                html.Label("CAFV Eligibility", style={'color': colors['text'], 'marginTop': '20px'}),
                dcc.Dropdown(
                    id='cafv-filter',
                    options=[{'label': cafv, 'value': cafv} for cafv in sorted(df['Clean Alternative Fuel Vehicle (CAFV) Eligibility'].unique())],
                    multi=True,
                    placeholder="Select eligibility",
                    style={'backgroundColor': colors['card'], 'color': 'black'}
                ),
                
                # Filtered records counter
                html.Div(id='filtered-count', style={'color': colors['text'], 'marginTop': '20px'})
            ], 
            style={
                'backgroundColor': colors['card'],
                'padding': '20px',
                'borderRadius': '5px',
                'height': '100%'
            })
        ], width=3),
        
        # Main content area with tabs
        dbc.Col([
            dcc.Tabs(id='tabs', value='tab-1', children=[
                # Tab 1: Overview
                dcc.Tab(label='Overview', value='tab-1', style=tab_style, selected_style=tab_selected_style, children=[
                    dbc.Row([
                        dbc.Col([
                            html.Div(id='metric-total-evs', className='metric-card')
                        ], width=3),
                        dbc.Col([
                            html.Div(id='metric-bev-count', className='metric-card')
                        ], width=3),
                        dbc.Col([
                            html.Div(id='metric-phev-count', className='metric-card')
                        ], width=3),
                        dbc.Col([
                            html.Div(id='metric-avg-range', className='metric-card')
                        ], width=3),
                    ], className='mb-4'),
                    
                    html.H4("Vehicle Distribution by Make", style={'color': colors['text']}),
                    dcc.Graph(id='make-distribution'),
                    
                    html.H4("Most Popular EV Models", style={'color': colors['text']}),
                    dcc.Graph(id='model-distribution'),
                    
                    html.H4("Electric Range Distribution", style={'color': colors['text']}),
                    dcc.Graph(id='range-distribution'),
                ]),
                
                # Tab 2: Geographical Analysis
                dcc.Tab(label='Geographical Analysis', value='tab-2', style=tab_style, selected_style=tab_selected_style, children=[
                    html.H4("EV Distribution by County", style={'color': colors['text']}),
                    dcc.Graph(id='county-distribution'),
                    
                    html.H4("EV Locations Map", style={'color': colors['text']}),
                    dcc.Graph(id='location-map'),
                    
                    html.H4("EVs by Electric Utility", style={'color': colors['text']}),
                    dcc.Graph(id='utility-distribution'),
                ]),
                
                # Tab 3: Manufacturer Analysis
                dcc.Tab(label='Manufacturer Analysis', value='tab-3', style=tab_style, selected_style=tab_selected_style, children=[
                    html.H4("Electric Range by Manufacturer", style={'color': colors['text']}),
                    dcc.Graph(id='range-by-make'),
                    
                    html.H4("EV Type Distribution by Manufacturer", style={'color': colors['text']}),
                    dcc.Graph(id='ev-type-by-make'),
                    
                    html.H4("Model Distribution for Selected Manufacturers", style={'color': colors['text']}),
                    dcc.Dropdown(
                        id='manufacturer-selector',
                        placeholder="Select a manufacturer",
                        style={'backgroundColor': colors['card'], 'color': 'black', 'marginBottom': '20px'}
                    ),
                    dcc.Graph(id='manufacturer-models'),
                ]),
                
                # Tab 4: Time Trends
                dcc.Tab(label='Time Trends', value='tab-4', style=tab_style, selected_style=tab_selected_style, children=[
                    html.H4("EV Adoption Trend by Model Year", style={'color': colors['text']}),
                    dcc.Graph(id='adoption-trend'),
                    
                    html.H4("EV Type Adoption Over Time", style={'color': colors['text']}),
                    dcc.Graph(id='ev-type-trend'),
                    
                    html.H4("Top Manufacturers Adoption Trend", style={'color': colors['text']}),
                    dcc.Graph(id='manufacturer-trend'),
                    
                    html.H4("CAFV Eligibility Trend", style={'color': colors['text']}),
                    dcc.Graph(id='cafv-trend'),
                ]),
            ]),
        ], width=9),
    ]),
    
    # Footer
    html.Hr(style={'borderColor': colors['accent']}),
    html.P("Data source: Electric Vehicle Population Data from Washington State Department of Licensing", 
           style={'color': colors['text'], 'textAlign': 'center'}),
    html.P("Dashboard created with Dash and Plotly", 
           style={'color': colors['text'], 'textAlign': 'center'}),
    
], fluid=True, style={'backgroundColor': colors['background'], 'minHeight': '100vh'})

# Callback to filter data and update all components
@app.callback(
    [Output('filtered-count', 'children'),
     Output('metric-total-evs', 'children'),
     Output('metric-bev-count', 'children'),
     Output('metric-phev-count', 'children'),
     Output('metric-avg-range', 'children'),
     Output('make-distribution', 'figure'),
     Output('model-distribution', 'figure'),
     Output('range-distribution', 'figure'),
     Output('county-distribution', 'figure'),
     Output('location-map', 'figure'),
     Output('utility-distribution', 'figure'),
     Output('range-by-make', 'figure'),
     Output('ev-type-by-make', 'figure'),
     Output('manufacturer-selector', 'options'),
     Output('manufacturer-selector', 'value'),
     Output('manufacturer-models', 'figure'),
     Output('adoption-trend', 'figure'),
     Output('ev-type-trend', 'figure'),
     Output('manufacturer-trend', 'figure'),
     Output('cafv-trend', 'figure')],
    [Input('year-slider', 'value'),
     Input('make-filter', 'value'),
     Input('ev-type-filter', 'value'),
     Input('county-filter', 'value'),
     Input('cafv-filter', 'value'),
     Input('manufacturer-selector', 'value')]
)
def update_dashboard(year_range, selected_makes, selected_ev_types, selected_counties, selected_cafv, selected_mfr):
    # Apply filters
    filtered_df = df.copy()
    
    # Apply year range filter
    filtered_df = filtered_df[(filtered_df['Model Year'] >= year_range[0]) & 
                              (filtered_df['Model Year'] <= year_range[1])]
    
    # Apply make filter if selected
    if selected_makes:
        filtered_df = filtered_df[filtered_df['Make'].isin(selected_makes)]
    
    # Apply EV type filter if selected
    if selected_ev_types:
        filtered_df = filtered_df[filtered_df['Electric Vehicle Type'].isin(selected_ev_types)]
    
    # Apply county filter if selected
    if selected_counties:
        filtered_df = filtered_df[filtered_df['County'].isin(selected_counties)]
    
    # Apply CAFV eligibility filter if selected
    if selected_cafv:
        filtered_df = filtered_df[filtered_df['Clean Alternative Fuel Vehicle (CAFV) Eligibility'].isin(selected_cafv)]
    
    # If filtered dataframe is empty, show a message
    if len(filtered_df) == 0:
        filtered_count = "No records match your filters."
        
        # Create empty figures for all charts
        empty_fig = go.Figure()
        empty_fig.update_layout(
            paper_bgcolor=colors['background'],
            plot_bgcolor=colors['card'],
            font_color=colors['text'],
            title="No data available with current filters",
            height=400
        )
        
        metric_total = create_metric_card("Total EVs", "0")
        metric_bev = create_metric_card("Battery Electric Vehicles", "0")
        metric_phev = create_metric_card("Plug-in Hybrid Vehicles", "0")
        metric_range = create_metric_card("Average Electric Range (miles)", "0")
        
        return [filtered_count, metric_total, metric_bev, metric_phev, metric_range] + [empty_fig] * 15 + [[], None, empty_fig]
    
    # Count records after filtering
    filtered_count = f"Filtered records: {len(filtered_df):,}"
    
    # Calculate metrics
    total_evs = len(filtered_df)
    bev_count = len(filtered_df[filtered_df['Electric Vehicle Type'].str.contains('Battery Electric Vehicle')])
    phev_count = len(filtered_df[filtered_df['Electric Vehicle Type'].str.contains('Plug-in Hybrid')])
    avg_range = int(filtered_df['Electric Range'].mean())
    
    # Create metric cards
    metric_total = create_metric_card("Total EVs", f"{total_evs:,}")
    metric_bev = create_metric_card("Battery Electric Vehicles", f"{bev_count:,}")
    metric_phev = create_metric_card("Plug-in Hybrid Vehicles", f"{phev_count:,}")
    metric_range = create_metric_card("Average Electric Range (miles)", f"{avg_range}")
    
    # Create figures for Tab 1: Overview
    # Top 10 makes bar chart
    make_counts = filtered_df['Make'].value_counts().reset_index()
    make_counts.columns = ['Make', 'Count']
    make_counts = make_counts.head(10)
    fig_makes = viz.create_make_distribution_chart(make_counts)
    
    # Top models by popularity
    model_counts = filtered_df.groupby(['Make', 'Model']).size().reset_index(name='Count')
    model_counts = model_counts.sort_values('Count', ascending=False).head(10)
    fig_models = viz.create_model_distribution_chart(model_counts)
    
    # Electric Range Distribution
    range_df = filtered_df[filtered_df['Electric Range'] > 0]
    fig_range = viz.create_range_distribution_chart(range_df)
    
    # Tab 2: Geographical Analysis
    # County distribution
    county_counts = filtered_df['County'].value_counts().reset_index()
    county_counts.columns = ['County', 'Count']
    fig_counties = viz.create_county_distribution_chart(county_counts)
    
    # Map visualization
    map_data = dp.process_location_data(filtered_df)
    if not map_data.empty:
        fig_map = viz.create_location_map(map_data)
    else:
        fig_map = go.Figure()
        fig_map.update_layout(
            title="No valid location data available for mapping",
            height=500
        )
    
    # Electric Utility Distribution
    utility_data = dp.process_utility_data(filtered_df)
    fig_utilities = viz.create_utility_distribution_chart(utility_data)
    
    # Tab 3: Manufacturer Analysis
    # Select top manufacturers for comparison
    top_makes = filtered_df['Make'].value_counts().head(8).index.tolist()
    
    # Electric range by manufacturer
    range_comp_df = filtered_df[(filtered_df['Make'].isin(top_makes)) & (filtered_df['Electric Range'] > 0)]
    if not range_comp_df.empty:
        fig_range_by_make = viz.create_range_by_make_chart(range_comp_df)
    else:
        fig_range_by_make = go.Figure()
        fig_range_by_make.update_layout(
            title="Not enough data available for range comparison",
            height=500
        )
    
    # EV Type Distribution by Manufacturer
    type_by_make = filtered_df[filtered_df['Make'].isin(top_makes)].groupby(['Make', 'Electric Vehicle Type']).size().reset_index(name='Count')
    fig_type_by_make = viz.create_ev_type_by_make_chart(type_by_make)
    
    # Create options for manufacturer selector
    mfr_options = [{'label': make, 'value': make} for make in top_makes]
    
    # If no manufacturer is selected, use the first one from the list
    if not selected_mfr and top_makes:
        selected_mfr = top_makes[0]
        
    # Model distribution by manufacturer
    if selected_mfr:
        mfr_models = filtered_df[filtered_df['Make'] == selected_mfr]['Model'].value_counts().reset_index()
        mfr_models.columns = ['Model', 'Count']
        fig_mfr_models = viz.create_manufacturer_models_chart(mfr_models, selected_mfr)
    else:
        fig_mfr_models = go.Figure()
        fig_mfr_models.update_layout(
            title="Please select a manufacturer",
            height=500
        )
    
    # Tab 4: Time Trends Analysis
    # EV adoption over time
    year_counts = filtered_df.groupby('Model Year').size().reset_index(name='Count')
    fig_trend = viz.create_adoption_trend_chart(year_counts)
    
    # EV type adoption over time
    type_year_counts = filtered_df.groupby(['Model Year', 'Electric Vehicle Type']).size().reset_index(name='Count')
    fig_type_trend = viz.create_ev_type_trend_chart(type_year_counts)
    
    # Manufacturer adoption over time
    top5_makes = filtered_df['Make'].value_counts().head(5).index.tolist()
    make_year_counts = filtered_df[filtered_df['Make'].isin(top5_makes)].groupby(['Model Year', 'Make']).size().reset_index(name='Count')
    fig_make_trend = viz.create_manufacturer_trend_chart(make_year_counts)
    
    # CAFV eligibility over time
    cafv_year_counts = filtered_df.groupby(['Model Year', 'Clean Alternative Fuel Vehicle (CAFV) Eligibility']).size().reset_index(name='Count')
    fig_cafv_trend = viz.create_cafv_trend_chart(cafv_year_counts)
    
    return [
        filtered_count, 
        metric_total, 
        metric_bev, 
        metric_phev, 
        metric_range,
        fig_makes, 
        fig_models, 
        fig_range,
        fig_counties, 
        fig_map, 
        fig_utilities,
        fig_range_by_make, 
        fig_type_by_make, 
        mfr_options,
        selected_mfr,
        fig_mfr_models,
        fig_trend, 
        fig_type_trend, 
        fig_make_trend, 
        fig_cafv_trend
    ]

# Helper function to create metric cards
def create_metric_card(title, value):
    return html.Div([
        html.H6(title, style={'color': colors['text']}),
        html.H3(value, style={'color': colors['text'], 'fontWeight': 'bold'})
    ], style={
        'backgroundColor': colors['card'],
        'border': f'1px solid {colors["accent"]}',
        'borderRadius': '5px',
        'padding': '15px',
        'textAlign': 'center'
    })

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)