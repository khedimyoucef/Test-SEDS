import os
import pandas as pd
import streamlit as st

# Base directory of this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "paris-2024-olympic-summer-games", "versions", "27")

# -----------------------------
# Data loading functions
# -----------------------------

@st.cache_data
def load_athletes():
    return pd.read_csv(os.path.join(DATA_PATH, "athletes.csv"))

@st.cache_data
def load_coaches():
    return pd.read_csv(os.path.join(DATA_PATH, "coaches.csv"))

@st.cache_data
def load_events():
    return pd.read_csv(os.path.join(DATA_PATH, "events.csv"))

@st.cache_data
def load_medals():
    return pd.read_csv(os.path.join(DATA_PATH, "medals.csv"))

@st.cache_data
def load_medals_total():
    return pd.read_csv(os.path.join(DATA_PATH, "medals_total.csv"))

@st.cache_data
def load_medalists():
    # Ensure the filename matches your CSV exactly
    return pd.read_csv(os.path.join(DATA_PATH, "medallists.csv"))

@st.cache_data
def load_nocs():
    return pd.read_csv(os.path.join(DATA_PATH, "nocs.csv"))

@st.cache_data
def load_schedule():
    return pd.read_csv(os.path.join(DATA_PATH, "schedules.csv"))

@st.cache_data
def load_teams():
    return pd.read_csv(os.path.join(DATA_PATH, "teams.csv"))

@st.cache_data
def load_venues():
    return pd.read_csv(os.path.join(DATA_PATH, "venues.csv"))

# -----------------------------
# Continent mapping for NOCs
# -----------------------------
@st.cache_data
def get_continent_mapping():
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

# -----------------------------
# Load all data at once
# -----------------------------
@st.cache_data
def load_all_data():
    athletes = load_athletes()
    medals_total = load_medals_total()
    nocs = load_nocs()

    continent_map = get_continent_mapping()
    nocs['continent'] = nocs['code'].map(continent_map).fillna('Other')

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

# -----------------------------
# Filter function
# -----------------------------
def apply_filters(data, filters):
    df = data.copy()

    if filters.get('countries'):
        if 'country_code' in df.columns:
            df = df[df['country_code'].isin(filters['countries'])]
        elif 'code' in df.columns:
            df = df[df['code'].isin(filters['countries'])]

    if filters.get('sports') and 'sport' in df.columns:
        df = df[df['sport'].isin(filters['sports'])]

    if filters.get('medal_types') and 'medal_type' in df.columns:
        df = df[df['medal_type'].isin(filters['medal_types'])]

    if filters.get('continents') and 'continent' in df.columns:
        df = df[df['continent'].isin(filters['continents'])]

    return df
