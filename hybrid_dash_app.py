import dash
from dash import html, dcc, callback, Input, Output, State
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
            .tab-container {
                margin-top: 20px;
                margin-bottom: 20px;
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
            .filter-container {
                background-color: ''' + COLORS['eerie-black'] + ''';
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 20px;
            }
            .filter-label {
                color: ''' + COLORS['cambridge-blue'] + ''';
                font-weight: bold;
                margin-bottom: 5px;
            }
            .filter-card {
                background-color: ''' + COLORS['dark-slate-gray'] + ''';
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 10px;
            }
            .btn-filter {
                background-color: ''' + COLORS['accent'] + ''';
                color: ''' + COLORS['night'] + ''';
                border: none;
                font-weight: bold;
            }
            .btn-filter:hover {
                background-color: ''' + COLORS['cambridge-blue'] + ''';
                color: ''' + COLORS['night'] + ''';
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

# Create the dashboard layout
def create_dashboard_layout():
    df = load_data()
    
    # Get unique values for filter options
    years = sorted(df['Model Year'].dropna().unique())
    min_year, max_year = int(min(years)), int(max(years))
    makes = sorted([x for x in df['Make'].dropna().unique() if isinstance(x, str)])
    counties = sorted([x for x in df['County'].dropna().unique() if isinstance(x, str)])
    ev_types = sorted([x for x in df['Electric Vehicle Type'].dropna().unique() if isinstance(x, str)])
    cafv_eligibility = df['Clean Alternative Fuel Vehicle (CAFV) Eligibility'].fillna('Unknown').unique()
    cafv_eligibility = sorted([x for x in cafv_eligibility if isinstance(x, str)])
    
    # Create the main layout with tabs
    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Washington State EV Population Dashboard", className="text-center my-4"), width=12)
        ]),
        
        dbc.Row([
            dbc.Col(html.H4("Comprehensive Analysis of Electric Vehicle Population Data", className="text-center mb-4"), width=12)
        ]),
        
        # Filter section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Filters"),
                    dbc.CardBody([
                        dbc.Row([
                            # Year Range Filter
                            dbc.Col([
                                html.Div("Year Range", className="filter-label"),
                                dcc.RangeSlider(
                                    id='year-range-slider',
                                    min=min_year,
                                    max=max_year,
                                    step=1,
                                    marks={i: str(i) for i in range(min_year, max_year+1, 2)},
                                    value=[min_year, max_year],
                                ),
                            ], width=12, className="mb-3"),
                        ]),
                        
                        dbc.Row([
                            # Make Filter
                            dbc.Col([
                                html.Div("Manufacturer", className="filter-label"),
                                dcc.Dropdown(
                                    id='make-dropdown',
                                    options=[{'label': make, 'value': make} for make in makes],
                                    multi=True,
                                    placeholder="Select manufacturers",
                                    style={"color": "black"}
                                ),
                            ], width=6, className="mb-3"),
                            
                            # EV Type Filter
                            dbc.Col([
                                html.Div("EV Type", className="filter-label"),
                                dcc.Dropdown(
                                    id='ev-type-dropdown',
                                    options=[{'label': ev_type, 'value': ev_type} for ev_type in ev_types],
                                    multi=True,
                                    placeholder="Select EV types",
                                    style={"color": "black"}
                                ),
                            ], width=6, className="mb-3"),
                        ]),
                        
                        dbc.Row([
                            # County Filter
                            dbc.Col([
                                html.Div("County", className="filter-label"),
                                dcc.Dropdown(
                                    id='county-dropdown',
                                    options=[{'label': county, 'value': county} for county in counties],
                                    multi=True,
                                    placeholder="Select counties",
                                    style={"color": "black"}
                                ),
                            ], width=6, className="mb-3"),
                            
                            # CAFV Eligibility Filter
                            dbc.Col([
                                html.Div("CAFV Eligibility", className="filter-label"),
                                dcc.Dropdown(
                                    id='cafv-dropdown',
                                    options=[{'label': cafv if cafv else "Unknown", 'value': cafv} for cafv in cafv_eligibility],
                                    multi=True,
                                    placeholder="Select CAFV eligibility",
                                    style={"color": "black"}
                                ),
                            ], width=6, className="mb-3"),
                        ]),
                        
                        dbc.Row([
                            dbc.Col([
                                dbc.Button("Apply Filters", id="apply-filters-button", color="primary", className="w-100 btn-filter")
                            ], width=12),
                        ]),
                    ])
                ]),
            ], width=12)
        ], className="mb-4"),
        
        # Tabs for different dashboard sections
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Tabs(id="dashboard-tabs", value="tab-overview", className="custom-tabs", children=[
                        dcc.Tab(label="Overview", value="tab-overview", className="custom-tab", selected_className="custom-tab--selected"),
                        dcc.Tab(label="Geographical Analysis", value="tab-geo", className="custom-tab", selected_className="custom-tab--selected"),
                        dcc.Tab(label="Manufacturer Analysis", value="tab-manufacturer", className="custom-tab", selected_className="custom-tab--selected"),
                        dcc.Tab(label="Time Trends", value="tab-trends", className="custom-tab", selected_className="custom-tab--selected"),
                    ]),
                    html.Div(id="tab-content", className="pt-4")
                ], className="tab-container"),
            ], width=12),
        ]),
        
        dbc.Row([
            dbc.Col(html.P("Data source: Electric Vehicle Population Data from Washington State Department of Licensing", 
                           className="text-center text-muted mt-4"), 
                    width=12)
        ])
    ], 
    fluid=True,
    style={"backgroundColor": COLORS['night']})

# Create callback to update the tab content
@callback(
    Output("tab-content", "children"),
    [Input("dashboard-tabs", "value"),
     Input("apply-filters-button", "n_clicks")],
    [State("year-range-slider", "value"),
     State("make-dropdown", "value"),
     State("ev-type-dropdown", "value"),
     State("county-dropdown", "value"),
     State("cafv-dropdown", "value")]
)
def update_tab_content(tab, n_clicks, year_range, selected_makes, selected_ev_types, selected_counties, selected_cafv):
    df = load_data()
    
    # Apply filters if specified
    filtered_df = df.copy()
    
    if year_range:
        filtered_df = filtered_df[(filtered_df['Model Year'] >= year_range[0]) & 
                                 (filtered_df['Model Year'] <= year_range[1])]
    
    if selected_makes:
        filtered_df = filtered_df[filtered_df['Make'].isin(selected_makes)]
    
    if selected_ev_types:
        filtered_df = filtered_df[filtered_df['Electric Vehicle Type'].isin(selected_ev_types)]
    
    if selected_counties:
        filtered_df = filtered_df[filtered_df['County'].isin(selected_counties)]
    
    if selected_cafv:
        filtered_df = filtered_df[filtered_df['Clean Alternative Fuel Vehicle (CAFV) Eligibility'].isin(selected_cafv)]
    
    # Overview Tab
    if tab == "tab-overview":
        # 1. Create top makes chart
        make_counts = filtered_df['Make'].value_counts().head(10).reset_index()
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
        model_counts = filtered_df.groupby(['Make', 'Model']).size().reset_index(name='Count')
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
        
        # 3. Create EV type distribution chart
        ev_type_counts = filtered_df['Electric Vehicle Type'].value_counts().reset_index()
        ev_type_counts.columns = ['Type', 'Count']
        
        fig3 = go.Figure(data=[go.Pie(
            labels=ev_type_counts['Type'],
            values=ev_type_counts['Count'],
            marker=dict(colors=[COLORS['accent'], COLORS['cambridge-blue']])
        )])
        fig3.update_layout(title='EV Type Distribution')
        
        # 4. Create CAFV eligibility chart
        cafv_counts = filtered_df['Clean Alternative Fuel Vehicle (CAFV) Eligibility'].fillna('Unknown').value_counts().reset_index()
        cafv_counts.columns = ['Eligibility', 'Count']
        
        fig4 = px.pie(
            cafv_counts,
            names='Eligibility',
            values='Count',
            title='CAFV Eligibility Distribution',
            color_discrete_sequence=[COLORS['accent'], COLORS['cambridge-blue'], '#FF5E5E']
        )
        
        # Create layout for Overview tab with Key Statistics at the top
        return [
            # Stats summary row at the top
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Key Statistics"),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Div("Total EVs", className="text-center", style={"color": COLORS['cambridge-blue']}),
                                    html.H3(f"{len(filtered_df):,}", className="text-center")
                                ], width=3),
                                dbc.Col([
                                    html.Div("Total Makes", className="text-center", style={"color": COLORS['cambridge-blue']}),
                                    html.H3(f"{filtered_df['Make'].nunique():,}", className="text-center")
                                ], width=3),
                                dbc.Col([
                                    html.Div("Total Models", className="text-center", style={"color": COLORS['cambridge-blue']}),
                                    html.H3(f"{filtered_df['Model'].nunique():,}", className="text-center")
                                ], width=3),
                                dbc.Col([
                                    html.Div("Counties", className="text-center", style={"color": COLORS['cambridge-blue']}),
                                    html.H3(f"{filtered_df['County'].nunique():,}", className="text-center")
                                ], width=3),
                            ])
                        ])
                    ])
                ], width=12)
            ], className="mb-4"),
            
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
                        dbc.CardHeader("EV Type Distribution"),
                        dbc.CardBody(html.Div([
                            html.Iframe(srcDoc=generate_chart_html(fig3), style={'width': '100%', 'height': '400px', 'border': 'none'})
                        ]))
                    ])
                ], width=6),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("CAFV Eligibility"),
                        dbc.CardBody(html.Div([
                            html.Iframe(srcDoc=generate_chart_html(fig4), style={'width': '100%', 'height': '400px', 'border': 'none'})
                        ]))
                    ])
                ], width=6)
            ]),
        ]
    
    # Geographical Analysis Tab
    elif tab == "tab-geo":
        # 1. Create county distribution chart
        county_counts = filtered_df['County'].value_counts().head(15).reset_index()
        county_counts.columns = ['County', 'Count']
        
        fig1 = px.bar(
            county_counts,
            x='County',
            y='Count',
            title='EV Distribution by County',
            color_discrete_sequence=[COLORS['accent']]
        )
        fig1.update_layout(xaxis_tickangle=-45)
        
        # 2. Create county by EV type chart
        county_ev_type = filtered_df.groupby(['County', 'Electric Vehicle Type']).size().reset_index(name='Count')
        county_ev_type = county_ev_type.sort_values('Count', ascending=False)
        top_counties = county_counts['County'].head(10).tolist()
        county_ev_type = county_ev_type[county_ev_type['County'].isin(top_counties)]
        
        fig2 = px.bar(
            county_ev_type,
            x='County',
            y='Count',
            color='Electric Vehicle Type',
            title='EV Types by County (Top 10 Counties)',
            barmode='stack',
            color_discrete_sequence=[COLORS['accent'], COLORS['cambridge-blue']]
        )
        fig2.update_layout(xaxis_tickangle=-45)
        
        # Add more geographical charts and analysis here
        
        return [
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("EV Distribution by County"),
                        dbc.CardBody(html.Div([
                            html.Iframe(srcDoc=generate_chart_html(fig1), style={'width': '100%', 'height': '400px', 'border': 'none'})
                        ]))
                    ])
                ], width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("EV Types by County"),
                        dbc.CardBody(html.Div([
                            html.Iframe(srcDoc=generate_chart_html(fig2), style={'width': '100%', 'height': '500px', 'border': 'none'})
                        ]))
                    ])
                ], width=12)
            ], className="mt-4"),
        ]
    
    # Manufacturer Analysis Tab
    elif tab == "tab-manufacturer":
        # 1. Create manufacturer by EV type chart
        make_ev_type = filtered_df.groupby(['Make', 'Electric Vehicle Type']).size().reset_index(name='Count')
        top_makes = filtered_df['Make'].value_counts().head(10).index.tolist()
        make_ev_type = make_ev_type[make_ev_type['Make'].isin(top_makes)]
        
        fig1 = px.bar(
            make_ev_type,
            x='Make',
            y='Count',
            color='Electric Vehicle Type',
            title='EV Types by Manufacturer (Top 10)',
            barmode='stack',
            color_discrete_sequence=[COLORS['accent'], COLORS['cambridge-blue']]
        )
        
        # 2. Create manufacturer model distribution chart (top 5 models for top 5 manufacturers)
        top_5_makes = filtered_df['Make'].value_counts().head(5).index.tolist()
        top_models = filtered_df[filtered_df['Make'].isin(top_5_makes)].groupby(['Make', 'Model']).size().reset_index(name='Count')
        top_models = top_models.sort_values(['Make', 'Count'], ascending=[True, False])
        
        make_models = []
        for make in top_5_makes:
            make_top_models = top_models[top_models['Make'] == make].head(5)
            make_models.append(make_top_models)
        
        model_df = pd.concat(make_models)
        model_df['Full Model'] = model_df['Make'] + ' ' + model_df['Model']
        
        fig2 = px.bar(
            model_df,
            x='Count',
            y='Full Model',
            color='Make',
            orientation='h',
            title='Top 5 Models by Top 5 Manufacturers',
            color_discrete_sequence=[COLORS['accent'], COLORS['cambridge-blue'], '#FF5E5E', '#FFD166', '#06D6A0']
        )
        
        return [
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("EV Types by Manufacturer"),
                        dbc.CardBody(html.Div([
                            html.Iframe(srcDoc=generate_chart_html(fig1), style={'width': '100%', 'height': '400px', 'border': 'none'})
                        ]))
                    ])
                ], width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Top Models by Manufacturer"),
                        dbc.CardBody(html.Div([
                            html.Iframe(srcDoc=generate_chart_html(fig2), style={'width': '100%', 'height': '600px', 'border': 'none'})
                        ]))
                    ])
                ], width=12)
            ], className="mt-4"),
        ]
    
    # Time Trends Tab
    elif tab == "tab-trends":
        # 1. Create year trend chart
        year_counts = filtered_df.groupby('Model Year').size().reset_index(name='Count')
        year_counts = year_counts.sort_values('Model Year')
        
        fig1 = px.line(
            year_counts,
            x='Model Year',
            y='Count',
            title='EV Adoption by Year',
            markers=True
        )
        fig1.update_traces(line=dict(color=COLORS['accent']), marker=dict(color=COLORS['accent']))
        
        # 2. Create EV type trend by year
        ev_type_year = filtered_df.groupby(['Model Year', 'Electric Vehicle Type']).size().reset_index(name='Count')
        ev_type_year = ev_type_year.sort_values('Model Year')
        
        fig2 = px.line(
            ev_type_year,
            x='Model Year',
            y='Count',
            color='Electric Vehicle Type',
            title='EV Type Adoption Trend',
            markers=True,
            color_discrete_sequence=[COLORS['accent'], COLORS['cambridge-blue']]
        )
        
        # 3. Create top 5 manufacturers trend
        top_5_makes = filtered_df['Make'].value_counts().head(5).index.tolist()
        make_year = filtered_df[filtered_df['Make'].isin(top_5_makes)].groupby(['Model Year', 'Make']).size().reset_index(name='Count')
        make_year = make_year.sort_values('Model Year')
        
        fig3 = px.line(
            make_year,
            x='Model Year',
            y='Count',
            color='Make',
            title='Top 5 Manufacturers Adoption Trend',
            markers=True,
            color_discrete_sequence=[COLORS['accent'], COLORS['cambridge-blue'], '#FF5E5E', '#FFD166', '#06D6A0']
        )
        
        return [
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("EV Adoption Trend"),
                        dbc.CardBody(html.Div([
                            html.Iframe(srcDoc=generate_chart_html(fig1), style={'width': '100%', 'height': '400px', 'border': 'none'})
                        ]))
                    ])
                ], width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("EV Type Adoption Trend"),
                        dbc.CardBody(html.Div([
                            html.Iframe(srcDoc=generate_chart_html(fig2), style={'width': '100%', 'height': '400px', 'border': 'none'})
                        ]))
                    ])
                ], width=12)
            ], className="mt-4"),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Manufacturer Adoption Trend"),
                        dbc.CardBody(html.Div([
                            html.Iframe(srcDoc=generate_chart_html(fig3), style={'width': '100%', 'height': '400px', 'border': 'none'})
                        ]))
                    ])
                ], width=12)
            ], className="mt-4"),
        ]
    
    return []  # Default empty content

# Set up the app layout
app.layout = create_dashboard_layout()

# Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)