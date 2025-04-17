import pandas as pd
import numpy as np
import re

def preprocess_data(df):
    """
    Preprocess the EV dataset for analysis
    """
    # Create a copy to avoid modifying the original
    df = df.copy()
    
    # Convert Model Year to numeric, coercing errors to NaN
    df['Model Year'] = pd.to_numeric(df['Model Year'], errors='coerce')
    
    # Handle Electric Range - convert to numeric
    df['Electric Range'] = pd.to_numeric(df['Electric Range'], errors='coerce')
    df['Electric Range'] = df['Electric Range'].fillna(0)
    
    # Handle Base MSRP - convert to numeric
    if 'Base MSRP' in df.columns:
        df['Base MSRP'] = pd.to_numeric(df['Base MSRP'], errors='coerce')
        df['Base MSRP'] = df['Base MSRP'].fillna(0)
    
    # Process Vehicle Location if it exists
    if 'Vehicle Location' in df.columns:
        df = process_location_column(df)
    
    return df

def process_location_column(df):
    """
    Extract latitude and longitude from the Vehicle Location column
    Format expected: POINT (-xxx.xxx xx.xxx)
    """
    if 'Vehicle Location' in df.columns:
        # Create new columns for lat/long
        df['Longitude'] = np.nan
        df['Latitude'] = np.nan
        
        # Use regex to extract coordinates
        pattern = r'POINT \(([-\d.]+) ([-\d.]+)\)'
        
        # Apply regex to extract coordinates
        coords = df['Vehicle Location'].str.extract(pattern)
        
        if not coords.empty and coords.shape[1] == 2:
            df['Longitude'] = pd.to_numeric(coords[0], errors='coerce')
            df['Latitude'] = pd.to_numeric(coords[1], errors='coerce')
    
    return df

def process_location_data(df):
    """
    Process location data for mapping
    """
    # Create a copy with only rows that have valid lat/long
    map_df = df.copy()
    
    # Check if lat/long columns already exist
    if 'Latitude' not in map_df.columns or 'Longitude' not in map_df.columns:
        map_df = process_location_column(map_df)
    
    # Filter to rows with valid coordinates
    map_df = map_df.dropna(subset=['Latitude', 'Longitude'])
    
    # If there are too many points, sample to make visualization manageable
    if len(map_df) > 5000:
        map_df = map_df.sample(5000, random_state=42)
    
    return map_df

def process_utility_data(df):
    """
    Process electric utility data, handling multiple utilities per vehicle
    """
    if 'Electric Utility' not in df.columns:
        return pd.DataFrame(columns=['Utility', 'Count'])
    
    # Create a list to store utility-count pairs
    utility_counts = {}
    
    # Loop through each utility entry
    for utilities in df['Electric Utility'].dropna():
        # Split by pipe if multiple utilities
        for utility in utilities.split('|'):
            # Clean utility name
            utility = utility.strip()
            if utility.endswith(' - (WA)'):
                utility = utility[:-7]
                
            if utility in utility_counts:
                utility_counts[utility] += 1
            else:
                utility_counts[utility] = 1
    
    # Convert to DataFrame
    utility_df = pd.DataFrame({
        'Utility': list(utility_counts.keys()),
        'Count': list(utility_counts.values())
    })
    
    # Sort by count
    utility_df = utility_df.sort_values('Count', ascending=False).head(10)
    
    return utility_df
