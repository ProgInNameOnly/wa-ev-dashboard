import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Custom theme colors
colors = {
    'background': '#03120e',  # night
    'text': '#8ab0ab',        # cambridge-blue
    'accent': '#3e505b',      # charcoal
    'card': '#1a1d1a',        # eerie-black
    'dark_accent': '#26413c', # dark-slate-gray
    'highlight': '#65a6a0',   # brighter version of cambridge-blue
    'bright_accent': '#5a6f7d', # brighter version of charcoal
    'bar_color': '#00FFB0',   # bright neon turquoise - highly visible
    'accent_bar': '#FF5E5E',  # bright coral red
    'third_color': '#FFD166'  # bright amber
}

# Fixed bright colorscale that will definitely be visible
custom_colorscale = [
    [0, '#FF5E5E'],       # bright coral red
    [0.25, '#FFD166'],    # bright amber
    [0.5, '#06D6A0'],     # bright mint
    [0.75, '#118AB2'],    # bright cerulean
    [1, '#073B4C']        # dark blue
]

def apply_theme(fig):
    """Apply the custom theme to a plotly figure"""
    fig.update_layout(
        paper_bgcolor=colors['background'],
        plot_bgcolor=colors['card'],
        font_color=colors['text'],
        font_family='Courier New, monospace',
        margin=dict(l=10, r=10, t=30, b=10),
        # Increase contrast for better visibility
        title_font=dict(color=colors['highlight'], size=18),
    )
    
    # Update axes with brighter colors for better visibility
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=colors['bright_accent'],
        zeroline=False,
        showline=True,
        linewidth=2,
        linecolor=colors['highlight'],
        title_font=dict(color=colors['highlight'], size=14),
        tickfont=dict(color=colors['highlight'])
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=colors['bright_accent'],
        zeroline=False,
        showline=True,
        linewidth=2,
        linecolor=colors['highlight'],
        title_font=dict(color=colors['highlight'], size=14),
        tickfont=dict(color=colors['highlight'])
    )
    
    # Update legend with better contrast
    fig.update_layout(
        legend=dict(
            font=dict(color=colors['highlight']),
            bgcolor=colors['card'],
            bordercolor=colors['highlight'],
            borderwidth=1
        )
    )
    
    return fig

def create_make_distribution_chart(make_counts):
    """
    Create a bar chart of EV distribution by make
    """
    fig = px.bar(
        make_counts,
        x='Count',
        y='Make',
        orientation='h',
        color='Count',
        color_continuous_scale=custom_colorscale,
        labels={'Count': 'Number of Vehicles', 'Make': 'Manufacturer'},
        title='Top 10 EV Manufacturers'
    )
    
    # Override the colors to ensure they're visible - CRITICAL CHANGE
    fig.update_traces(
        marker=dict(
            color=colors['bar_color'],  # Use bright neon turquoise
            opacity=1.0,                # Full opacity
            line=dict(width=1, color=colors['background'])
        ),
        hovertemplate='<b>%{y}</b><br>Number of Vehicles: %{x:,}',
        texttemplate='%{x:,}',          # Add text labels
        textposition='outside',
        textfont=dict(
            size=14,
            color=colors['highlight']
        )
    )
    
    # Add more explicit axis labels
    fig.update_layout(
        xaxis_title='Number of Vehicles',
        yaxis_title='Manufacturer',
        hoverlabel=dict(
            bgcolor=colors['background'],
            font_size=14,
            font_color=colors['highlight']
        )
    )
    
    return apply_theme(fig)

def create_model_distribution_chart(model_counts):
    """
    Create a bar chart of the most popular EV models
    """
    # Create a column combining make and model
    model_counts['Full Model'] = model_counts['Make'] + ' ' + model_counts['Model']
    
    # Use a much brighter color sequence for better visibility
    manufacturer_colors = ['#FF5E5E', '#FFD166', '#06D6A0', '#118AB2', '#E71D36', '#FF9F1C', '#2EC4B6', '#FDFFFC']
    
    fig = px.bar(
        model_counts,
        x='Count',
        y='Full Model',
        orientation='h',
        color='Make',
        labels={'Count': 'Number of Vehicles', 'Full Model': 'Vehicle Model'},
        title='Top 10 EV Models by Popularity',
        color_discrete_sequence=manufacturer_colors
    )
    
    # Ensure bars are fully visible with high opacity
    fig.update_traces(
        hovertemplate='<b>%{y}</b><br>Number of Vehicles: %{x:,}',
        marker_line_color=colors['background'],
        marker_line_width=1,
        marker=dict(opacity=1.0),  # Full opacity
        texttemplate='%{x:,}',     # Add text labels
        textposition='outside',
        textfont=dict(
            size=14,
            color=colors['highlight']
        )
    )
    
    # Add more explicit axis labels
    fig.update_layout(
        xaxis_title='Number of Vehicles',
        yaxis_title='Vehicle Model',
        hoverlabel=dict(
            bgcolor=colors['background'],
            font_size=14,
            font_color=colors['highlight']
        ),
        # Enhanced legend for better visibility
        legend=dict(
            font=dict(color=colors['highlight'], size=14),
            bgcolor=colors['card'],
            bordercolor=colors['highlight'],
            borderwidth=2
        )
    )
    
    return apply_theme(fig)

def create_range_distribution_chart(range_df):
    """
    Create a histogram of electric range distribution
    """
    # Use extremely bright colors for better visibility
    ev_type_colors = ['#FF5E5E', '#06D6A0']  # Bright red and bright mint
    
    fig = px.histogram(
        range_df,
        x='Electric Range',
        color='Electric Vehicle Type',
        nbins=30,
        opacity=1.0,  # Full opacity
        barmode='overlay',
        labels={'Electric Range': 'Electric Range (miles)'},
        title='Distribution of Electric Range',
        color_discrete_sequence=ev_type_colors
    )
    
    # Ensure histogram bars are fully visible
    fig.update_traces(
        hovertemplate='<b>Range: %{x} miles</b><br>Count: %{y}',
        marker_line_color=colors['background'],
        marker_line_width=1,
        marker=dict(opacity=0.9)  # High opacity but allow slight overlay
    )
    
    # Add vertical line for average range with improved visibility
    avg_range = range_df['Electric Range'].mean()
    fig.add_vline(
        x=avg_range,
        line_dash="dash",
        line_color=colors['highlight'],
        line_width=2,
        annotation_text=f"Avg: {avg_range:.1f} miles",
        annotation_position="top right",
        annotation_font_color=colors['highlight'],
        annotation_font_size=14
    )
    
    # Add more explicit axis labels
    fig.update_layout(
        xaxis_title='Electric Range (miles)',
        yaxis_title='Number of Vehicles',
        hoverlabel=dict(
            bgcolor=colors['background'],
            font_size=14,
            font_color=colors['highlight']
        ),
        # Enhanced legend for better visibility
        legend=dict(
            font=dict(color=colors['highlight'], size=14),
            bgcolor=colors['card'],
            bordercolor=colors['highlight'],
            borderwidth=2
        )
    )
    
    return apply_theme(fig)

def create_county_distribution_chart(county_counts):
    """
    Create a bar chart of EV distribution by county
    """
    # Sort by count
    county_counts = county_counts.sort_values('Count', ascending=False).head(15)
    
    fig = px.bar(
        county_counts,
        x='County',
        y='Count',
        color='Count',
        color_continuous_scale=custom_colorscale,
        labels={'Count': 'Number of Vehicles', 'County': 'County'},
        title='Top 15 Counties by EV Population'
    )
    
    # Override colors to ensure visibility
    fig.update_traces(
        marker=dict(
            color=colors['third_color'],  # Use bright amber color
            opacity=1.0,                  # Full opacity
            line=dict(width=1, color=colors['background'])
        ),
        hovertemplate='<b>%{x}</b><br>Number of Vehicles: %{y:,}',
        texttemplate='%{y:,}',  # Add text labels
        textposition='outside',
        textfont=dict(
            size=14,
            color=colors['highlight']
        )
    )
    
    # Add more explicit axis labels
    fig.update_layout(
        xaxis_title='County',
        yaxis_title='Number of Vehicles',
        xaxis_tickangle=-45,
        hoverlabel=dict(
            bgcolor=colors['background'],
            font_size=14,
            font_color=colors['highlight']
        )
    )
    
    return apply_theme(fig)

def create_location_map(map_data):
    """
    Create a scatter map of EV locations
    """
    # Use brighter colors for better visibility
    ev_type_colors = ['#65a6a0', '#a7ccc7', '#d5e8e5']
    
    fig = px.scatter_mapbox(
        map_data,
        lat='Latitude',
        lon='Longitude',
        color='Electric Vehicle Type',
        hover_name='Make',
        hover_data={
            'Model': True,
            'Model Year': True,
            'Electric Range': True,
            'Latitude': False,
            'Longitude': False
        },
        zoom=6,
        title='EV Locations in Washington State',
        color_discrete_sequence=ev_type_colors,
        opacity=0.8  # Slightly transparent points for better overlap visibility
    )
    
    fig.update_layout(
        mapbox_style="carto-darkmatter",
        mapbox_accesstoken=None,
        legend=dict(
            font=dict(color=colors['highlight'], size=14),
            bgcolor=colors['card'],
            bordercolor=colors['highlight'],
            borderwidth=2,
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hoverlabel=dict(
            bgcolor=colors['background'],
            font_size=14,
            font_color=colors['highlight']
        )
    )
    
    return apply_theme(fig)

def create_utility_distribution_chart(utility_data):
    """
    Create a pie chart of EV distribution by electric utility
    """
    # Use brighter, more distinct colors for pie slices
    utility_colors = ['#65a6a0', '#3d8a7d', '#a7ccc7', '#d5e8e5', '#2a6056', 
                      '#5a6f7d', '#7a8f9d', '#9aafbd', '#bacfdd', '#cedff9']
    
    fig = px.pie(
        utility_data,
        values='Count',
        names='Utility',
        title='EV Distribution by Electric Utility',
        color_discrete_sequence=utility_colors
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont=dict(size=14, color=colors['background']),
        marker=dict(line=dict(color=colors['background'], width=2)),
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}'
    )
    
    # Enhanced legend for better visibility
    fig.update_layout(
        hoverlabel=dict(
            bgcolor=colors['background'],
            font_size=14,
            font_color=colors['highlight']
        ),
        legend=dict(
            font=dict(color=colors['highlight'], size=14),
            bgcolor=colors['card'],
            bordercolor=colors['highlight'],
            borderwidth=2
        )
    )
    
    return apply_theme(fig)

def create_range_by_make_chart(range_df):
    """
    Create a box plot of electric range by manufacturer
    """
    # Use brighter colors for better visibility
    manufacturer_colors = ['#65a6a0', '#a7ccc7', '#d5e8e5', '#3d8a7d', '#2a6056', 
                           '#5a6f7d', '#7a8f9d', '#9aafbd']
    
    fig = px.box(
        range_df,
        x='Make',
        y='Electric Range',
        color='Make',
        points='outliers',
        labels={'Electric Range': 'Electric Range (miles)'},
        title='Electric Range Distribution by Manufacturer',
        color_discrete_sequence=manufacturer_colors
    )
    
    fig.update_traces(
        marker_line_color=colors['background'],
        marker_line_width=1,
        boxmean=True,  # Show mean as a dashed line
        marker=dict(
            opacity=0.8,
            size=6,
            line=dict(width=1, color=colors['background'])
        )
    )
    
    # Add more explicit axis labels
    fig.update_layout(
        xaxis_title='Manufacturer',
        yaxis_title='Electric Range (miles)',
        xaxis_tickangle=-45,
        hoverlabel=dict(
            bgcolor=colors['background'],
            font_size=14,
            font_color=colors['highlight']
        ),
        # Enhanced legend for better visibility
        legend=dict(
            font=dict(color=colors['highlight'], size=14),
            bgcolor=colors['card'],
            bordercolor=colors['highlight'],
            borderwidth=2
        )
    )
    
    return apply_theme(fig)

def create_ev_type_by_make_chart(type_by_make):
    """
    Create a stacked bar chart of EV types by manufacturer
    """
    # Use brighter colors for better visibility
    ev_type_colors = ['#65a6a0', '#a7ccc7', '#d5e8e5']
    
    fig = px.bar(
        type_by_make,
        x='Make',
        y='Count',
        color='Electric Vehicle Type',
        barmode='stack',
        labels={'Count': 'Number of Vehicles', 'Make': 'Manufacturer'},
        title='EV Type Distribution by Manufacturer',
        color_discrete_sequence=ev_type_colors
    )
    
    fig.update_traces(
        marker_line_color=colors['background'],
        marker_line_width=1,
        # Add text labels showing values
        texttemplate='%{y:,}',  
        textposition='inside',
        textfont=dict(
            size=14,
            color=colors['background']
        )
    )
    
    # Add more explicit axis labels
    fig.update_layout(
        xaxis_title='Manufacturer',
        yaxis_title='Number of Vehicles',
        xaxis_tickangle=-45,
        hoverlabel=dict(
            bgcolor=colors['background'],
            font_size=14,
            font_color=colors['highlight']
        ),
        # Enhanced legend for better visibility
        legend=dict(
            font=dict(color=colors['highlight'], size=14),
            bgcolor=colors['card'],
            bordercolor=colors['highlight'],
            borderwidth=2
        )
    )
    
    return apply_theme(fig)

def create_manufacturer_models_chart(model_data, manufacturer):
    """
    Create a bar chart of models for a specific manufacturer
    """
    # Limit to top 10 models
    model_data = model_data.head(10)
    
    fig = px.bar(
        model_data,
        x='Model',
        y='Count',
        color='Count',
        color_continuous_scale=custom_colorscale,
        labels={'Count': 'Number of Vehicles', 'Model': 'Model'},
        title=f'{manufacturer} Models by Popularity'
    )
    
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Number of Vehicles: %{y:,}',
        marker_line_color=colors['background'],
        marker_line_width=1,
        texttemplate='%{y:,}',  # Add text labels
        textposition='outside',
        textfont=dict(
            size=14,
            color=colors['highlight']
        )
    )
    
    # Add more explicit axis labels
    fig.update_layout(
        xaxis_title='Model',
        yaxis_title='Number of Vehicles',
        xaxis_tickangle=-45,
        hoverlabel=dict(
            bgcolor=colors['background'],
            font_size=14,
            font_color=colors['highlight']
        )
    )
    
    return apply_theme(fig)

def create_adoption_trend_chart(year_counts):
    """
    Create a line chart of EV adoption trend by year
    """
    fig = px.line(
        year_counts,
        x='Model Year',
        y='Count',
        markers=True,
        labels={'Count': 'Number of Vehicles', 'Model Year': 'Year'},
        title='EV Adoption Trend by Model Year'
    )
    
    # Use much brighter colors for line visibility
    fig.update_traces(
        line_color=colors['highlight'],
        line_width=4,
        marker_color='#a7ccc7',  # Light teal
        marker_line_color=colors['background'],
        marker_line_width=1,
        marker_size=12
    )
    
    # Add more explicit axis labels
    fig.update_layout(
        xaxis_title='Model Year',
        yaxis_title='Number of Vehicles',
        hoverlabel=dict(
            bgcolor=colors['background'],
            font_size=14,
            font_color=colors['highlight']
        )
    )
    
    return apply_theme(fig)

def create_ev_type_trend_chart(type_year_counts):
    """
    Create a line chart of EV type adoption over time
    """
    # Use a brighter color sequence for better visibility
    bright_colors = ['#65a6a0', '#a7ccc7', '#d5e8e5', '#3d8a7d', '#2a6056']
    
    fig = px.line(
        type_year_counts,
        x='Model Year',
        y='Count',
        color='Electric Vehicle Type',
        markers=True,
        labels={'Count': 'Number of Vehicles', 'Model Year': 'Year'},
        title='EV Type Adoption Trend by Year',
        color_discrete_sequence=bright_colors
    )
    
    fig.update_traces(
        line_width=3,
        marker_line_color=colors['background'],
        marker_line_width=1,
        marker_size=10
    )
    
    # Add more explicit axis labels
    fig.update_layout(
        xaxis_title='Model Year',
        yaxis_title='Number of Vehicles',
        hoverlabel=dict(
            bgcolor=colors['background'],
            font_size=14,
            font_color=colors['highlight']
        ),
        # Enhanced legend for better visibility
        legend=dict(
            font=dict(color=colors['highlight'], size=14),
            bgcolor=colors['card'],
            bordercolor=colors['highlight'],
            borderwidth=2
        )
    )
    
    return apply_theme(fig)

def create_manufacturer_trend_chart(make_year_counts):
    """
    Create a line chart of manufacturer adoption over time
    """
    # Define bright custom colors for manufacturers
    manufacturer_colors = ['#65a6a0', '#a7ccc7', '#3d8a7d', '#2a6056', '#5a6f7d']
    
    fig = px.line(
        make_year_counts,
        x='Model Year',
        y='Count',
        color='Make',
        markers=True,
        labels={'Count': 'Number of Vehicles', 'Model Year': 'Year'},
        title='Top 5 Manufacturers Adoption Trend',
        color_discrete_sequence=manufacturer_colors
    )
    
    fig.update_traces(
        line_width=3,
        marker_line_color=colors['background'],
        marker_line_width=1,
        marker_size=10
    )
    
    # Add more explicit axis labels
    fig.update_layout(
        xaxis_title='Model Year',
        yaxis_title='Number of Vehicles',
        hoverlabel=dict(
            bgcolor=colors['background'],
            font_size=14,
            font_color=colors['highlight']
        ),
        # Enhanced legend for better visibility
        legend=dict(
            font=dict(color=colors['highlight'], size=14),
            bgcolor=colors['card'],
            bordercolor=colors['highlight'],
            borderwidth=2
        )
    )
    
    return apply_theme(fig)

def create_cafv_trend_chart(cafv_year_counts):
    """
    Create a stacked area chart of CAFV eligibility over time
    """
    # Brighter colors for better visibility on dark background
    cafv_colors = ['#65a6a0', '#3d8a7d', '#a7ccc7', '#2a6056']
    
    fig = px.area(
        cafv_year_counts,
        x='Model Year',
        y='Count',
        color='Clean Alternative Fuel Vehicle (CAFV) Eligibility',
        labels={'Count': 'Number of Vehicles', 'Model Year': 'Year'},
        title='CAFV Eligibility Trend by Year',
        color_discrete_sequence=cafv_colors
    )
    
    fig.update_traces(
        marker_line_color=colors['background'],
        marker_line_width=1,
        opacity=0.8  # Increased opacity for better visibility
    )
    
    # Add more explicit axis labels
    fig.update_layout(
        xaxis_title='Model Year',
        yaxis_title='Number of Vehicles',
        hoverlabel=dict(
            bgcolor=colors['background'],
            font_size=14,
            font_color=colors['highlight']
        ),
        # Enhanced legend for better visibility
        legend=dict(
            font=dict(color=colors['highlight'], size=14),
            bgcolor=colors['card'],
            bordercolor=colors['highlight'],
            borderwidth=2
        )
    )
    
    return apply_theme(fig)
