# =============================================================================
# FILTERS UTILITY
# =============================================================================
# This module provides functions for creating sidebar filter widgets and
# generating filter summaries. These filters are used across all pages of
# the dashboard to allow users to drill down into specific subsets of data.
# 
# The sidebar filters let users filter by:
# - Country (NOC code)
# - Continent
# - Sport
# - Medal type (Gold, Silver, Bronze)
# =============================================================================

import streamlit as st  # The main framework for building the filter UI
from utils.country_flags import get_flag_html  # For displaying country flags

def create_sidebar_filters(data):
    """
    Create global filter widgets in the Streamlit sidebar.
    
    This function builds the entire filter UI in the sidebar, including
    dropdowns for countries, continents, and sports, plus checkboxes for
    medal types. All filter selections are returned in a dictionary.
    
    Args:
        data: Dictionary of DataFrames from load_all_data(), needed to
              populate the filter options (list of countries, sports, etc.)
    
    Returns:
        dict: A dictionary with filter selections:
            - 'countries': List of selected country codes (empty if none selected)
            - 'continents': List of selected continent names
            - 'sports': List of selected sport names
            - 'medal_types': List of selected medal types (e.g., ['Gold Medal'])
    """
    # st.sidebar gives us access to the sidebar area of the Streamlit app
    # Anything called with st.sidebar.X appears in the sidebar instead of main area
    
    # Title and divider for the filter section
    st.sidebar.title("🔍 Global Filters")
    st.sidebar.markdown("---")  # Creates a horizontal line
    
    # Initialize the filters dictionary to store user selections
    filters = {}
    
    # ==========================================================================
    # COUNTRY FILTER (MULTI-SELECT DROPDOWN)
    # ==========================================================================
    #creating subheaders for each filter
    st.sidebar.subheader("🌍 Country (NOC)")
    
    # Get all unique country codes from the NOCs data, sorted alphabetically
    # .unique() returns distinct values, sorted() puts them in order
    # .tolist() converts from numpy array to Python list
    all_countries = sorted(data['nocs']['code'].unique().tolist())
    # The 'code' attribute is a column directly within the 'nocs' DataFrame,
    # representing the NOC code for each entry.
    
    # st.sidebar.multiselect() creates a dropdown where users can select multiple items
    # It returns a list of selected items (empty list if nothing selected)
    filters['countries'] = st.sidebar.multiselect(
        "Select Countries",  # Label shown above the widget
        options=all_countries,  # The list of available options
        default=[],  # No countries selected by default (show all data)
        help="Filter by country/NOC code"  # Tooltip text on hover
    )
    
    # Display selected countries with their flags (if any are selected)
    if filters['countries']:
        flags_html = " ".join([f"{get_flag_html(c, 20)}" for c in filters['countries']])
        st.sidebar.markdown(f"Selected: {flags_html}", unsafe_allow_html=True)
    
    # ==========================================================================
    # CONTINENT FILTER
    # ==========================================================================
    st.sidebar.subheader("🗺️ Continent")
    
    # Get unique continents from the NOCs data (we added this column in data_loader)
    all_continents = sorted(data['nocs']['continent'].unique().tolist())
    
    filters['continents'] = st.sidebar.multiselect(
        "Select Continents",
        options=all_continents,
        default=[],
        help="Filter by continent - a creative filter!"
    )
    
    # ==========================================================================
    # SPORT FILTER
    # ==========================================================================
    st.sidebar.subheader("⚽ Sport")
    
    # Get unique sports from the events data
    # .dropna() removes any missing (NaN) values from the list
    all_sports = sorted(data['events']['sport'].dropna().unique().tolist())
    
    filters['sports'] = st.sidebar.multiselect(
        "Select Sports",
        options=all_sports,
        default=[],
        help="Filter by sport"
    )
    
    # ==========================================================================
    # MEDAL TYPE FILTER (CHECKBOXES)
    # ==========================================================================
    st.sidebar.subheader("🏅 Medal Type")
    
    # Define the valid medal types
    medal_types = ['Gold Medal', 'Silver Medal', 'Bronze Medal']
    
    # Create three columns in the sidebar for the medal checkboxes
    # This arranges them horizontally instead of vertically
    col1, col2, col3 = st.sidebar.columns(3)
    
    # st.checkbox() creates a toggle checkbox
    # Returns True if checked, False if unchecked
    # value=True means it starts checked by default
    with col1:
        gold = st.checkbox("🥇", value=True, help="Gold")
    with col2:
        silver = st.checkbox("🥈", value=True, help="Silver")
    with col3:
        bronze = st.checkbox("🥉", value=True, help="Bronze")
    
    # Build the medal_types list based on which checkboxes are checked
    filters['medal_types'] = []
    if gold:
        filters['medal_types'].append('Gold Medal')
    if silver:
        filters['medal_types'].append('Silver Medal')
    if bronze:
        filters['medal_types'].append('Bronze Medal')
    
    st.sidebar.markdown("---")
    
    # ==========================================================================
    # CLEAR FILTERS BUTTON
    # ==========================================================================
    # st.sidebar.button() creates a clickable button
    # Returns True when clicked, False otherwise
    if st.sidebar.button("🔄 Clear All Filters"):
        # st.rerun() refreshes the entire page, which resets all widget values
        # This is a simple way to clear all filter selections
        st.rerun()
    
    return filters


def get_filter_summary(filters):
    """
    Generate a human-readable summary of the active filters.
    
    This function takes the filters dictionary and returns a string
    describing what filters are currently applied. This is displayed
    at the top of each page so users know what data they're looking at.
    
    Args:
        filters: Dictionary of filter selections from create_sidebar_filters()
    
    Returns:
        str: A summary string like "Active filters: 3 countries, 2 sports"
             or "No filters active (showing all data)" if no filters applied
    """
    summaries = []  # List to collect summary parts
    
    # Check each filter type and add a summary if selections exist
    # filters.get('key') returns the value or None if key doesn't exist
    
    if filters.get('countries'):
        # len() gives the number of selected countries
        summaries.append(f"{len(filters['countries'])} countries")
    
    if filters.get('continents'):
        summaries.append(f"{len(filters['continents'])} continents")
    
    if filters.get('sports'):
        summaries.append(f"{len(filters['sports'])} sports")
    
    # For medal types, only mention them if not all three are selected
    # (since all three selected is the same as no filter)
    if filters.get('medal_types') and len(filters['medal_types']) < 3:
        summaries.append(f"{len(filters['medal_types'])} medal types")
    
    # Build the final summary string
    if summaries:
        # Join all parts with commas
        return "Active filters: " + ", ".join(summaries)
    else:
        return "No filters active (showing all data)"
