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
    'dark_accent': '#26413c'  # dark-slate-gray
}

# Custom colorscale based on theme
custom_colorscale = [
    [0, colors['background']],
    [0.25, colors['dark_accent']],
    [0.5, colors['accent']],
    [0.75, colors['text']],
    [1, '#ffffff']
]

def apply_theme(fig):
    """Apply the custom theme to a plotly figure"""
    fig.update_layout(
        paper_bgcolor=colors['background'],
        plot_bgcolor=colors['card'],
        font_color=colors['text'],
        font_family='Courier New, monospace',
        margin=dict(l=10, r=10, t=30, b=10),
    )
    
    # Update axes
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=colors['accent'],
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor=colors['text'],
        title_font=dict(color=colors['text'])
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=colors['accent'],
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor=colors['text'],
        title_font=dict(color=colors['text'])
    )
    
    # Update legend
    fig.update_layout(
        legend=dict(
            font=dict(color=colors['text']),
            bgcolor=colors['card'],
            bordercolor=colors['accent'],
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
    
    fig.update_traces(
        hovertemplate='<b>%{y}</b><br>Number of Vehicles: %{x:,}',
        marker_line_color=colors['accent'],
        marker_line_width=1
    )
    
    return apply_theme(fig)

def create_model_distribution_chart(model_counts):
    """
    Create a bar chart of the most popular EV models
    """
    # Create a column combining make and model
    model_counts['Full Model'] = model_counts['Make'] + ' ' + model_counts['Model']
    
    fig = px.bar(
        model_counts,
        x='Count',
        y='Full Model',
        orientation='h',
        color='Make',
        labels={'Count': 'Number of Vehicles', 'Full Model': 'Vehicle Model'},
        title='Top 10 EV Models by Popularity',
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    
    fig.update_traces(
        hovertemplate='<b>%{y}</b><br>Number of Vehicles: %{x:,}',
        marker_line_color=colors['accent'],
        marker_line_width=1
    )
    
    return apply_theme(fig)

def create_range_distribution_chart(range_df):
    """
    Create a histogram of electric range distribution
    """
    fig = px.histogram(
        range_df,
        x='Electric Range',
        color='Electric Vehicle Type',
        nbins=30,
        opacity=0.8,
        barmode='overlay',
        labels={'Electric Range': 'Electric Range (miles)'},
        title='Distribution of Electric Range',
        color_discrete_sequence=[colors['text'], colors['accent']]
    )
    
    fig.update_traces(
        hovertemplate='<b>Range: %{x} miles</b><br>Count: %{y}',
        marker_line_color=colors['background'],
        marker_line_width=1
    )
    
    # Add vertical line for average range
    avg_range = range_df['Electric Range'].mean()
    fig.add_vline(
        x=avg_range,
        line_dash="dash",
        line_color=colors['text'],
        annotation_text=f"Avg: {avg_range:.1f} miles",
        annotation_position="top right",
        annotation_font_color=colors['text']
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
    
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Number of Vehicles: %{y:,}',
        marker_line_color=colors['accent'],
        marker_line_width=1
    )
    
    fig.update_layout(xaxis_tickangle=-45)
    
    return apply_theme(fig)

def create_location_map(map_data):
    """
    Create a scatter map of EV locations
    """
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
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    
    fig.update_layout(
        mapbox_style="carto-darkmatter",
        mapbox_accesstoken=None,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return apply_theme(fig)

def create_utility_distribution_chart(utility_data):
    """
    Create a pie chart of EV distribution by electric utility
    """
    fig = px.pie(
        utility_data,
        values='Count',
        names='Utility',
        title='EV Distribution by Electric Utility',
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        marker=dict(line=dict(color=colors['background'], width=2)),
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}'
    )
    
    return apply_theme(fig)

def create_range_by_make_chart(range_df):
    """
    Create a box plot of electric range by manufacturer
    """
    fig = px.box(
        range_df,
        x='Make',
        y='Electric Range',
        color='Make',
        points='outliers',
        labels={'Electric Range': 'Electric Range (miles)'},
        title='Electric Range Distribution by Manufacturer',
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    
    fig.update_traces(
        marker_line_color=colors['background'],
        marker_line_width=1,
        boxmean=True  # Show mean as a dashed line
    )
    
    fig.update_layout(xaxis_tickangle=-45)
    
    return apply_theme(fig)

def create_ev_type_by_make_chart(type_by_make):
    """
    Create a stacked bar chart of EV types by manufacturer
    """
    fig = px.bar(
        type_by_make,
        x='Make',
        y='Count',
        color='Electric Vehicle Type',
        barmode='stack',
        labels={'Count': 'Number of Vehicles'},
        title='EV Type Distribution by Manufacturer',
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    
    fig.update_traces(
        marker_line_color=colors['background'],
        marker_line_width=1
    )
    
    fig.update_layout(xaxis_tickangle=-45)
    
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
        marker_line_color=colors['accent'],
        marker_line_width=1
    )
    
    fig.update_layout(xaxis_tickangle=-45)
    
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
    
    fig.update_traces(
        line_color=colors['text'],
        marker_color=colors['accent'],
        marker_line_color=colors['background'],
        marker_line_width=1,
        marker_size=8
    )
    
    return apply_theme(fig)

def create_ev_type_trend_chart(type_year_counts):
    """
    Create a line chart of EV type adoption over time
    """
    fig = px.line(
        type_year_counts,
        x='Model Year',
        y='Count',
        color='Electric Vehicle Type',
        markers=True,
        labels={'Count': 'Number of Vehicles', 'Model Year': 'Year'},
        title='EV Type Adoption Trend by Year',
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    
    fig.update_traces(
        marker_line_color=colors['background'],
        marker_line_width=1,
        marker_size=8
    )
    
    return apply_theme(fig)

def create_manufacturer_trend_chart(make_year_counts):
    """
    Create a line chart of manufacturer adoption over time
    """
    fig = px.line(
        make_year_counts,
        x='Model Year',
        y='Count',
        color='Make',
        markers=True,
        labels={'Count': 'Number of Vehicles', 'Model Year': 'Year'},
        title='Top 5 Manufacturers Adoption Trend',
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    
    fig.update_traces(
        marker_line_color=colors['background'],
        marker_line_width=1,
        marker_size=8
    )
    
    return apply_theme(fig)

def create_cafv_trend_chart(cafv_year_counts):
    """
    Create a stacked area chart of CAFV eligibility over time
    """
    fig = px.area(
        cafv_year_counts,
        x='Model Year',
        y='Count',
        color='Clean Alternative Fuel Vehicle (CAFV) Eligibility',
        labels={'Count': 'Number of Vehicles', 'Model Year': 'Year'},
        title='CAFV Eligibility Trend by Year',
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    
    fig.update_traces(
        marker_line_color=colors['background'],
        marker_line_width=0.5
    )
    
    return apply_theme(fig)
