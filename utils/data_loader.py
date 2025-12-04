import streamlit as st
import pandas as pd
import os

# Dataset base path
DATA_PATH = r"paris-2024-olympic-summer-games\versions\27"

@st.cache_data
def load_athletes():
    """Load athletes data"""
    return pd.read_csv(os.path.join(DATA_PATH, "athletes.csv"))

@st.cache_data
def load_coaches():
    """Load coaches data"""
    return pd.read_csv(os.path.join(DATA_PATH, "coaches.csv"))

@st.cache_data
def load_events():
    """Load events data"""
    return pd.read_csv(os.path.join(DATA_PATH, "events.csv"))

@st.cache_data
def load_medals():
    """Load medals data"""
    return pd.read_csv(os.path.join(DATA_PATH, "medals.csv"))

@st.cache_data
def load_medals_total():
    """Load total medals data"""
    return pd.read_csv(os.path.join(DATA_PATH, "medals_total.csv"))

@st.cache_data
def load_medalists():
    """Load medalists data"""
    return pd.read_csv(os.path.join(DATA_PATH, "medallists.csv"))

@st.cache_data
def load_nocs():
    """Load NOCs (countries) data"""
    return pd.read_csv(os.path.join(DATA_PATH, "nocs.csv"))

@st.cache_data
def load_schedule():
    """Load schedule data"""
    return pd.read_csv(os.path.join(DATA_PATH, "schedules.csv"))

@st.cache_data
def load_teams():
    """Load teams data"""
    return pd.read_csv(os.path.join(DATA_PATH, "teams.csv"))

@st.cache_data
def load_venues():
    """Load venues data"""
    return pd.read_csv(os.path.join(DATA_PATH, "venues.csv"))

@st.cache_data
def get_continent_mapping():
    """Create a mapping of country codes to continents"""
    # Manual mapping for Olympic NOC codes to continents
    continent_map = {
        # Europe
        'ALB': 'Europe', 'AND': 'Europe', 'ARM': 'Europe', 'AUT': 'Europe', 'AZE': 'Europe',
        'BLR': 'Europe', 'BEL': 'Europe', 'BIH': 'Europe', 'BUL': 'Europe', 'CRO': 'Europe',
        'CYP': 'Europe', 'CZE': 'Europe', 'DEN': 'Europe', 'ESP': 'Europe', 'EST': 'Europe',
        'FIN': 'Europe', 'FRA': 'Europe', 'GBR': 'Europe', 'GEO': 'Europe', 'GER': 'Europe',
        'GRE': 'Europe', 'HUN': 'Europe', 'IRL': 'Europe', 'ISL': 'Europe', 'ISR': 'Europe',
        'ITA': 'Europe', 'KOS': 'Europe', 'LAT': 'Europe', 'LIE': 'Europe', 'LTU': 'Europe',
        'LUX': 'Europe', 'MDA': 'Europe', 'MKD': 'Europe', 'MLT': 'Europe', 'MNE': 'Europe',
        'NED': 'Europe', 'NOR': 'Europe', 'POL': 'Europe', 'POR': 'Europe', 'ROU': 'Europe',
        'SRB': 'Europe', 'SVK': 'Europe', 'SLO': 'Europe', 'SUI': 'Europe', 'SWE': 'Europe',
        'TUR': 'Europe', 'UKR': 'Europe', 'SMR': 'Europe', 'MON': 'Europe',
        
        # Asia
        'AFG': 'Asia', 'BRN': 'Asia', 'BAN': 'Asia', 'BHU': 'Asia', 'BRU': 'Asia',
        'CAM': 'Asia', 'CHN': 'Asia', 'TPE': 'Asia', 'IND': 'Asia', 'INA': 'Asia',
        'IRI': 'Asia', 'IRQ': 'Asia', 'JPN': 'Asia', 'JOR': 'Asia', 'KAZ': 'Asia',
        'KOR': 'Asia', 'KUW': 'Asia', 'KGZ': 'Asia', 'LAO': 'Asia', 'LBN': 'Asia',
        'MAS': 'Asia', 'MDV': 'Asia', 'MGL': 'Asia', 'MYA': 'Asia', 'NEP': 'Asia',
        'OMA': 'Asia', 'PAK': 'Asia', 'PLE': 'Asia', 'PHI': 'Asia', 'QAT': 'Asia',
        'KSA': 'Asia', 'SGP': 'Asia', 'SRI': 'Asia', 'SYR': 'Asia', 'TJK': 'Asia',
        'THA': 'Asia', 'TLS': 'Asia', 'TKM': 'Asia', 'UAE': 'Asia', 'UZB': 'Asia',
        'VIE': 'Asia', 'YEM': 'Asia', 'HKG': 'Asia', 'PRK': 'Asia',
        
        # Africa
        'ALG': 'Africa', 'ANG': 'Africa', 'BEN': 'Africa', 'BOT': 'Africa', 'BUR': 'Africa',
        'BDI': 'Africa', 'CMR': 'Africa', 'CPV': 'Africa', 'CAF': 'Africa', 'CHA': 'Africa',
        'COM': 'Africa', 'CGO': 'Africa', 'CIV': 'Africa', 'COD': 'Africa', 'DJI': 'Africa',
        'EGY': 'Africa', 'GEQ': 'Africa', 'ERI': 'Africa', 'ETH': 'Africa', 'GAB': 'Africa',
        'GAM': 'Africa', 'GHA': 'Africa', 'GUI': 'Africa', 'GBS': 'Africa', 'KEN': 'Africa',
        'LES': 'Africa', 'LBR': 'Africa', 'LBA': 'Africa', 'MAD': 'Africa', 'MAW': 'Africa',
        'MLI': 'Africa', 'MRI': 'Africa', 'MAR': 'Africa', 'MOZ': 'Africa', 'NAM': 'Africa',
        'NIG': 'Africa', 'NGR': 'Africa', 'RWA': 'Africa', 'STP': 'Africa', 'SEN': 'Africa',
        'SEY': 'Africa', 'SLE': 'Africa', 'SOM': 'Africa', 'RSA': 'Africa', 'SSD': 'Africa',
        'SUD': 'Africa', 'TAN': 'Africa', 'TOG': 'Africa', 'TUN': 'Africa', 'UGA': 'Africa',
        'ZAM': 'Africa', 'ZIM': 'Africa',
        
        # North America
        'ANT': 'North America', 'ARU': 'North America', 'BAH': 'North America', 'BAR': 'North America',
        'BIZ': 'North America', 'BER': 'North America', 'CAN': 'North America', 'CAY': 'North America',
        'CRC': 'North America', 'CUB': 'North America', 'DMA': 'North America', 'DOM': 'North America',
        'ESA': 'North America', 'GRN': 'North America', 'GUA': 'North America', 'HAI': 'North America',
        'HON': 'North America', 'JAM': 'North America', 'MEX': 'North America', 'NCA': 'North America',
        'PAN': 'North America', 'PUR': 'North America', 'SKN': 'North America', 'LCA': 'North America',
        'VIN': 'North America', 'TTO': 'North America', 'USA': 'North America', 'ISV': 'North America',
        
        # South America
        'ARG': 'South America', 'BOL': 'South America', 'BRA': 'South America', 'CHI': 'South America',
        'COL': 'South America', 'ECU': 'South America', 'GUY': 'South America', 'PAR': 'South America',
        'PER': 'South America', 'SUR': 'South America', 'URU': 'South America', 'VEN': 'South America',
        
        # Oceania
        'ASA': 'Oceania', 'AUS': 'Oceania', 'COK': 'Oceania', 'FIJ': 'Oceania', 'FSM': 'Oceania',
        'GUM': 'Oceania', 'KIR': 'Oceania', 'MHL': 'Oceania', 'NRU': 'Oceania', 'NZL': 'Oceania',
        'PLW': 'Oceania', 'PNG': 'Oceania', 'SAM': 'Oceania', 'SOL': 'Oceania', 'TGA': 'Oceania',
        'TUV': 'Oceania', 'VAN': 'Oceania',
    }
    return continent_map

@st.cache_data
def load_all_data():
    """Load all necessary data and add continent information"""
    athletes = load_athletes()
    medals_total = load_medals_total()
    nocs = load_nocs()
    
    # Add continent information to NOCs
    continent_map = get_continent_mapping()
    nocs['continent'] = nocs['code'].map(continent_map)
    
    # Fill missing continents with 'Other'
    nocs['continent'] = nocs['continent'].fillna('Other')
    
    return {
        'athletes': athletes,
        'coaches': load_coaches(),
        'events': load_events(),
        'medals': load_medals(),
        'medals_total': medals_total,
        'medalists': load_medalists(),
        'nocs': nocs,
        'schedule': load_schedule(),
        'teams': load_teams(),
        'venues': load_venues(),
    }

def apply_filters(data, filters):
    """Apply filters to dataframe based on filter dictionary"""
    filtered_data = data.copy()
    
    if filters.get('countries') and len(filters['countries']) > 0:
        if 'country_code' in filtered_data.columns:
            filtered_data = filtered_data[filtered_data['country_code'].isin(filters['countries'])]
        elif 'code' in filtered_data.columns:
            filtered_data = filtered_data[filtered_data['code'].isin(filters['countries'])]
    
    if filters.get('sports') and len(filters['sports']) > 0:
        if 'sport' in filtered_data.columns:
            filtered_data = filtered_data[filtered_data['sport'].isin(filters['sports'])]
    
    if filters.get('medal_types') and len(filters['medal_types']) > 0:
        if 'medal_type' in filtered_data.columns:
            filtered_data = filtered_data[filtered_data['medal_type'].isin(filters['medal_types'])]
    
    if filters.get('continents') and len(filters['continents']) > 0:
        if 'continent' in filtered_data.columns:
            filtered_data = filtered_data[filtered_data['continent'].isin(filters['continents'])]
    
    return filtered_data
