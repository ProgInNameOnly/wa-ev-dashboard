import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import data_processor as dp
import visualizations as viz
import os
import time

# Page configuration
st.set_page_config(
    page_title="WA Electric Vehicle Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open('custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Title and description
st.title("Washington State Electric Vehicle Population Dashboard")
st.markdown("Explore and analyze electric vehicle data across Washington State.")

# Load data with a spinner
@st.cache_data
def load_data():
    start = time.time()
    try:
        # Load the data
        df = pd.read_csv('attached_assets/Electric_Vehicle_Population_Data.csv')
        
        # Process the data for analysis
        df = dp.preprocess_data(df)
        
        end = time.time()
        st.session_state['load_time'] = end - start
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Display loading message
with st.spinner("Loading and processing electric vehicle data..."):
    df = load_data()

if df is None:
    st.error("Failed to load data. Please check the file path and try again.")
    st.stop()

# Data loaded successfully
if 'load_time' in st.session_state:
    st.success(f"Data loaded successfully in {st.session_state['load_time']:.2f} seconds. {len(df)} vehicle records found.")

# Sidebar filters
st.sidebar.header("Data Filters")

# Year range filter
min_year = int(df['Model Year'].min())
max_year = int(df['Model Year'].max())
year_range = st.sidebar.slider(
    "Model Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# Make filter (multiselect)
all_makes = sorted(df['Make'].unique())
selected_makes = st.sidebar.multiselect(
    "Vehicle Make",
    options=all_makes,
    default=[]
)

# EV Type filter
ev_types = sorted(df['Electric Vehicle Type'].unique())
selected_ev_types = st.sidebar.multiselect(
    "EV Type",
    options=ev_types,
    default=[]
)

# County filter
all_counties = sorted(df['County'].unique())
selected_counties = st.sidebar.multiselect(
    "County",
    options=all_counties,
    default=[]
)

# CAFV Eligibility filter
cafv_options = sorted(df['Clean Alternative Fuel Vehicle (CAFV) Eligibility'].unique())
selected_cafv = st.sidebar.multiselect(
    "CAFV Eligibility",
    options=cafv_options,
    default=[]
)

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

# Show the number of records after filtering
st.sidebar.write(f"Filtered records: {len(filtered_df)}")

# Dashboard Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Geographical Analysis", "Manufacturer Analysis", "Time Trends"])

with tab1:
    st.header("Electric Vehicle Population Overview")
    
    # Top metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_evs = len(filtered_df)
        st.metric("Total EVs", f"{total_evs:,}")
    
    with col2:
        bev_count = len(filtered_df[filtered_df['Electric Vehicle Type'].str.contains('Battery Electric Vehicle')])
        st.metric("Battery Electric Vehicles", f"{bev_count:,}")
    
    with col3:
        phev_count = len(filtered_df[filtered_df['Electric Vehicle Type'].str.contains('Plug-in Hybrid')])
        st.metric("Plug-in Hybrid Vehicles", f"{phev_count:,}")
    
    with col4:
        avg_range = int(filtered_df['Electric Range'].mean())
        st.metric("Average Electric Range (miles)", avg_range)
    
    # Distribution by Make and Model
    st.subheader("Vehicle Distribution by Make")
    
    # Top 10 makes bar chart
    make_counts = filtered_df['Make'].value_counts().reset_index()
    make_counts.columns = ['Make', 'Count']
    make_counts = make_counts.head(10)
    
    fig_makes = viz.create_make_distribution_chart(make_counts)
    st.plotly_chart(fig_makes, use_container_width=True)
    
    # Top models by popularity
    st.subheader("Most Popular EV Models")
    
    model_counts = filtered_df.groupby(['Make', 'Model']).size().reset_index(name='Count')
    model_counts = model_counts.sort_values('Count', ascending=False).head(10)
    
    fig_models = viz.create_model_distribution_chart(model_counts)
    st.plotly_chart(fig_models, use_container_width=True)
    
    # Electric Range Distribution
    st.subheader("Electric Range Distribution")
    
    # Filter out rows with 0 or invalid electric range for this chart
    range_df = filtered_df[filtered_df['Electric Range'] > 0]
    
    fig_range = viz.create_range_distribution_chart(range_df)
    st.plotly_chart(fig_range, use_container_width=True)

with tab2:
    st.header("Geographical Distribution")
    
    # County distribution
    st.subheader("EV Distribution by County")
    
    county_counts = filtered_df['County'].value_counts().reset_index()
    county_counts.columns = ['County', 'Count']
    
    fig_counties = viz.create_county_distribution_chart(county_counts)
    st.plotly_chart(fig_counties, use_container_width=True)
    
    # Map visualization
    st.subheader("EV Locations Map")
    
    # Check if location data is available
    has_location_data = 'Vehicle Location' in filtered_df.columns and not filtered_df['Vehicle Location'].isna().all()
    
    if has_location_data:
        # Process location data
        map_data = dp.process_location_data(filtered_df)
        
        if not map_data.empty:
            fig_map = viz.create_location_map(map_data)
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.warning("No valid location data available for mapping.")
    else:
        st.warning("Location data is not available in the dataset.")
    
    # Electric Utility Distribution
    if 'Electric Utility' in filtered_df.columns:
        st.subheader("EVs by Electric Utility")
        
        # Process utility data (handling multiple utilities per record)
        utility_data = dp.process_utility_data(filtered_df)
        
        fig_utilities = viz.create_utility_distribution_chart(utility_data)
        st.plotly_chart(fig_utilities, use_container_width=True)

with tab3:
    st.header("Manufacturer Analysis")
    
    # Select manufacturers for comparison
    top_makes = filtered_df['Make'].value_counts().head(8).index.tolist()
    
    # Electric range by manufacturer
    st.subheader("Electric Range by Manufacturer")
    
    # Filter for valid range data
    range_comp_df = filtered_df[(filtered_df['Make'].isin(top_makes)) & (filtered_df['Electric Range'] > 0)]
    
    if not range_comp_df.empty:
        fig_range_by_make = viz.create_range_by_make_chart(range_comp_df)
        st.plotly_chart(fig_range_by_make, use_container_width=True)
    else:
        st.warning("Not enough data available for range comparison.")
    
    # EV Type Distribution by Manufacturer
    st.subheader("EV Type Distribution by Manufacturer")
    
    type_by_make = filtered_df[filtered_df['Make'].isin(top_makes)].groupby(['Make', 'Electric Vehicle Type']).size().reset_index(name='Count')
    
    fig_type_by_make = viz.create_ev_type_by_make_chart(type_by_make)
    st.plotly_chart(fig_type_by_make, use_container_width=True)
    
    # Model distribution by manufacturer
    st.subheader("Model Distribution for Selected Manufacturers")
    
    # Allow user to select manufacturers
    selected_mfr = st.selectbox("Select Manufacturer", options=top_makes)
    
    mfr_models = filtered_df[filtered_df['Make'] == selected_mfr]['Model'].value_counts().reset_index()
    mfr_models.columns = ['Model', 'Count']
    
    fig_mfr_models = viz.create_manufacturer_models_chart(mfr_models, selected_mfr)
    st.plotly_chart(fig_mfr_models, use_container_width=True)

with tab4:
    st.header("Time Trends Analysis")
    
    # EV adoption over time
    st.subheader("EV Adoption Trend by Model Year")
    
    year_counts = filtered_df.groupby('Model Year').size().reset_index(name='Count')
    
    fig_trend = viz.create_adoption_trend_chart(year_counts)
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # EV type adoption over time
    st.subheader("EV Type Adoption Over Time")
    
    type_year_counts = filtered_df.groupby(['Model Year', 'Electric Vehicle Type']).size().reset_index(name='Count')
    
    fig_type_trend = viz.create_ev_type_trend_chart(type_year_counts)
    st.plotly_chart(fig_type_trend, use_container_width=True)
    
    # Manufacturer adoption over time
    st.subheader("Top Manufacturers Adoption Trend")
    
    # Get top 5 manufacturers
    top5_makes = filtered_df['Make'].value_counts().head(5).index.tolist()
    
    make_year_counts = filtered_df[filtered_df['Make'].isin(top5_makes)].groupby(['Model Year', 'Make']).size().reset_index(name='Count')
    
    fig_make_trend = viz.create_manufacturer_trend_chart(make_year_counts)
    st.plotly_chart(fig_make_trend, use_container_width=True)
    
    # CAFV eligibility over time
    st.subheader("CAFV Eligibility Trend")
    
    cafv_year_counts = filtered_df.groupby(['Model Year', 'Clean Alternative Fuel Vehicle (CAFV) Eligibility']).size().reset_index(name='Count')
    
    fig_cafv_trend = viz.create_cafv_trend_chart(cafv_year_counts)
    st.plotly_chart(fig_cafv_trend, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Data source: Electric Vehicle Population Data from Washington State Department of Licensing")
st.markdown("Dashboard created with Streamlit and Plotly")
