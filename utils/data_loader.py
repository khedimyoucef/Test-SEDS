# =============================================================================
# DATA LOADER UTILITY
# =============================================================================
# This module is responsible for loading all the CSV data files used in the
# Paris 2024 Olympics Dashboard. It uses Streamlit's caching to ensure data
# is only loaded from disk once, even when multiple pages need the same data.
# 
# The module provides:
# - Individual loading functions for each CSV file
# - A continent mapping for countries (since the raw data doesn't include this)
# - A combined function to load all data at once
# - A filter function to filter DataFrames based on user selections
# =============================================================================

import os  # For file path operations
import pandas as pd  # For reading CSVs and working with DataFrames
import streamlit as st  # For the caching decorator

# =============================================================================
# PATH CONFIGURATION
# =============================================================================
# These paths tell Python where to find the data files

# __file__ is a special variable containing the path to THIS Python file
# os.path.abspath() converts it to an absolute path
# os.path.dirname() gets the directory containing that file (i.e., the 'utils' folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the data folder
# os.path.join() creates paths in a cross-platform way (handles / vs \ automatically)
# We go up one level (..) from utils to the project root, then into the data folder
DATA_PATH = os.path.join(BASE_DIR, "..", "paris-2024-olympic-summer-games", "versions", "27")
#using the base dir and data path to handle different operating systems

# =============================================================================
# INDIVIDUAL DATA LOADING FUNCTIONS
# =============================================================================
# Each function loads one CSV file. We use @st.cache_data on each one to ensure
# the file is only read from disk once. After the first load, the data is cached
# in memory and returned instantly on subsequent calls.

#using the streamlit cache function for every csv read to prevent the reload after each user action
@st.cache_data
def load_athletes():
    """Load the athletes.csv file containing information about all athletes."""
    # pd.read_csv() reads a CSV file into a pandas DataFrame
    # os.path.join() safely combines the DATA_PATH with the filename
    return pd.read_csv(os.path.join(DATA_PATH, "athletes.csv"))

@st.cache_data
def load_coaches():
    """Load the coaches.csv file containing information about coaches."""
    return pd.read_csv(os.path.join(DATA_PATH, "coaches.csv"))

@st.cache_data
def load_events():
    """Load the events.csv file containing information about all Olympic events."""
    return pd.read_csv(os.path.join(DATA_PATH, "events.csv"))

@st.cache_data
def load_medals():
    """Load the medals.csv file containing detailed records of each medal awarded."""
    return pd.read_csv(os.path.join(DATA_PATH, "medals.csv"))

@st.cache_data
def load_medals_total():
    """Load the medals_total.csv file with aggregated medal counts per country."""
    return pd.read_csv(os.path.join(DATA_PATH, "medals_total.csv"))

@st.cache_data
def load_medalists():
    """Load the medallists.csv file with information about medal-winning athletes."""
    return pd.read_csv(os.path.join(DATA_PATH, "medallists.csv"))

@st.cache_data
def load_nocs():
    """Load the nocs.csv file containing National Olympic Committee information."""
    return pd.read_csv(os.path.join(DATA_PATH, "nocs.csv"))

@st.cache_data
def load_schedule():
    """Load the schedules.csv file containing the event schedule."""
    return pd.read_csv(os.path.join(DATA_PATH, "schedules.csv"))

@st.cache_data
def load_teams():
    """Load the teams.csv file containing team information."""
    return pd.read_csv(os.path.join(DATA_PATH, "teams.csv"))

@st.cache_data
def load_venues():
    """Load the venues.csv file containing venue information."""
    return pd.read_csv(os.path.join(DATA_PATH, "venues.csv"))

# =============================================================================
# CONTINENT MAPPING
# =============================================================================
# The raw data doesn't include continent information for countries.
# This function provides a mapping from IOC country codes to continent names.
# This allows us to group and filter countries by continent in the dashboard.

@st.cache_data
def get_continent_mapping():
    """
    Returns a dictionary mapping IOC country codes to their continents.
    This is manually maintained since the Olympics data doesn't include continents.
    """
    continent_map = {
        # Europe - Western, Eastern, Northern, and Southern European countries
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
        
        # Asia - East, Southeast, South, Central, and West Asian countries
        'AFG': 'Asia', 'BRN': 'Asia', 'BAN': 'Asia', 'BHU': 'Asia', 'BRU': 'Asia',
        'CAM': 'Asia', 'CHN': 'Asia', 'TPE': 'Asia', 'IND': 'Asia', 'INA': 'Asia',
        'IRI': 'Asia', 'IRQ': 'Asia', 'JPN': 'Asia', 'JOR': 'Asia', 'KAZ': 'Asia',
        'KOR': 'Asia', 'KUW': 'Asia', 'KGZ': 'Asia', 'LAO': 'Asia', 'LBN': 'Asia',
        'MAS': 'Asia', 'MDV': 'Asia', 'MGL': 'Asia', 'MYA': 'Asia', 'NEP': 'Asia',
        'OMA': 'Asia', 'PAK': 'Asia', 'PLE': 'Asia', 'PHI': 'Asia', 'QAT': 'Asia',
        'KSA': 'Asia', 'SGP': 'Asia', 'SRI': 'Asia', 'SYR': 'Asia', 'TJK': 'Asia',
        'THA': 'Asia', 'TLS': 'Asia', 'TKM': 'Asia', 'UAE': 'Asia', 'UZB': 'Asia',
        'VIE': 'Asia', 'YEM': 'Asia', 'HKG': 'Asia', 'PRK': 'Asia',
        
        # Africa - North, West, East, Central, and Southern African countries
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
        
        # North America - Including Central America and Caribbean nations
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
        
        # Oceania - Australia, New Zealand, and Pacific Island nations
        'ASA': 'Oceania', 'AUS': 'Oceania', 'COK': 'Oceania', 'FIJ': 'Oceania', 'FSM': 'Oceania',
        'GUM': 'Oceania', 'KIR': 'Oceania', 'MHL': 'Oceania', 'NRU': 'Oceania', 'NZL': 'Oceania',
        'PLW': 'Oceania', 'PNG': 'Oceania', 'SAM': 'Oceania', 'SOL': 'Oceania', 'TGA': 'Oceania',
        'TUV': 'Oceania', 'VAN': 'Oceania',
    }
    return continent_map

# =============================================================================
# LOAD ALL DATA AT ONCE
# =============================================================================
# This function loads all datasets and returns them in a single dictionary.
# This is the main function that pages should call to get their data.

@st.cache_data
def load_all_data():
    """
    Load all CSV datasets and return them in a dictionary.
    Also enriches the NOCs data with continent information.
    
    Returns:
        dict: A dictionary where keys are dataset names and values are DataFrames.
              Keys: 'athletes', 'coaches', 'events', 'medals', 'medals_total',
                    'medalists', 'nocs', 'schedule', 'teams', 'venues'
    """
    # Load the datasets we need to process
    athletes = load_athletes()
    medals_total = load_medals_total()
    nocs = load_nocs()

    # Get the continent mapping dictionary
    continent_map = get_continent_mapping()
    
    # Add a 'continent' column to the NOCs DataFrame
    # .map() looks up each 'code' value in the continent_map dictionary
    # If a code isn't found, it returns NaN, which we fill with 'Other'
    nocs['continent'] = nocs['code'].map(continent_map).fillna('Other')
    #adding the continents attribute to the nocs dataframe by using the code to continet map
    #filling empty values with Other
    
    # Return all datasets in a dictionary for easy access
    return {
        'athletes': athletes,
        'coaches': load_coaches(),
        'events': load_events(),
        'medals': load_medals(),
        'medals_total': medals_total,
        'medalists': load_medalists(),
        'nocs': nocs,  # This now includes the continent column
        'schedule': load_schedule(),
        'teams': load_teams(),
        'venues': load_venues(),
    }

# =============================================================================
# FILTER FUNCTION
# =============================================================================
# This function applies user-selected filters to a DataFrame.
# It's used throughout the dashboard to filter data based on sidebar selections.

def apply_filters(data, filters):
    """
    Apply user-selected filters to a DataFrame.
    
    This function takes a DataFrame and a dictionary of filter selections,
    then returns a filtered copy of the DataFrame based on those selections.
    
    Args:
        data: A pandas DataFrame to filter
        filters: A dictionary with keys like 'countries', 'sports', 'medal_types', 'continents'
                Each value is a list of selected values for that filter.
                Empty list means no filter is applied for that category.
    
    Returns:
        A filtered copy of the input DataFrame
    """
    #the filter works here by taking the full dataframe and a dictionary of selected filters
    #then show only the data pertinent to the selected filters
    
    # Make a copy so we don't modify the original DataFrame
    df = data.copy()

    # Apply country filter if countries are selected
    if filters.get('countries'):
        # Check which column name the DataFrame uses for country codes
        if 'country_code' in df.columns:
            # .isin() returns True for rows where the value is in the provided list
            # We use this as a boolean mask to filter the DataFrame
            df = df[df['country_code'].isin(filters['countries'])]
            #keeping the rows whome country code is in the filters of countries list
        elif 'code' in df.columns:
            # Some DataFrames use 'code' instead of 'country_code'
            df = df[df['code'].isin(filters['countries'])]
    
    # Apply sport filter if sports are selected and the column exists
    #if the filter of sports is applied and the sport is in the current dataframe     
    if filters.get('sports') and 'sport' in df.columns:
        df = df[df['sport'].isin(filters['sports'])]

    # Apply medal type filter
    if filters.get('medal_types') and 'medal_type' in df.columns:
        df = df[df['medal_type'].isin(filters['medal_types'])]

    # Apply continent filter
    if filters.get('continents') and 'continent' in df.columns:
        df = df[df['continent'].isin(filters['continents'])]

    return df
