# =============================================================================
# HEAD-TO-HEAD COMPARISON PAGE
# =============================================================================
# This page lets users compare two countries side-by-side to see how they
# performed against each other at the Paris 2024 Olympics. It shows metrics
# like total medals, gold medals, athlete counts, and top sports for each.
# The "3_" prefix and 🆚 emoji help with navigation organization.
# =============================================================================

import streamlit as st  # The main framework for building this web app
import plotly.express as px  # For creating interactive charts easily
import pandas as pd  # For data manipulation with DataFrames
from utils.data_loader import load_all_data  # Our custom function to load CSV data

# Configure the page settings - must be called first before any other Streamlit commands
st.set_page_config(
    page_title="Head-to-Head Comparison",  # Browser tab title
    page_icon="🆚",  # Favicon emoji
    layout="wide"  # Use full browser width
)

# Set the main title for this page
st.title("🆚 Head-to-Head Country Comparison")
st.markdown("Compare the performance of two countries side-by-side.")

# =============================================================================
# LOAD DATA
# =============================================================================
# Load all datasets from our data loader utility
# This returns a dictionary where each key is a dataset name and value is a DataFrame
data = load_all_data()

# Extract the specific DataFrames we need for this page
medals_total = data['medals_total']  # Aggregated medal counts per country
nocs = data['nocs']  # National Olympic Committee info (country names, codes, etc.)
athletes = data['athletes']  # Individual athlete information
medals = data['medals']  # Detailed medal records (each medal won)

# =============================================================================
# HELPER FUNCTION
# =============================================================================
def get_country_name(code):
    """
    Convert a country code (like 'USA') to the full country name.
    This function looks up the code in the NOCs DataFrame.
    Returns the code itself if no matching name is found.
    """
    # Filter the nocs DataFrame to find the row where code matches
    row = nocs[nocs['code'] == code]
    if not row.empty:
        # .values[0] gets the first value from the resulting series
        # pd.notna() checks if the value is not NaN (missing)
        return row['note'].values[0] if pd.notna(row['note'].values[0]) else code
    return code

# =============================================================================
# COUNTRY SELECTION
# =============================================================================
# Get a sorted list of all countries that have medal data
# .unique() returns distinct values, sorted() puts them in alphabetical order
available_countries = sorted(medals_total['country_code'].unique())

# Create two columns for the country selectors to appear side by side
col1, col2 = st.columns(2)

with col1:
    # st.selectbox() creates a dropdown menu
    # First argument is the label, second is the list of options
    # index=0 means the first option is selected by default
    country_a = st.selectbox("Select Country A", available_countries, index=0)

with col2:
    # For Country B, we try to select a different default than Country A
    # This prevents both dropdowns from starting with the same country
    default_index_b = 1 if len(available_countries) > 1 else 0
    country_b = st.selectbox("Select Country B", available_countries, index=default_index_b)

# =============================================================================
# VALIDATION CHECK
# =============================================================================
# Warn the user if they've selected the same country twice
# st.warning() displays an orange warning box
if country_a == country_b:
    st.warning("Please select two different countries to compare.")
else:
    # =============================================================================
    # DATA PREPARATION
    # =============================================================================
    
    # --- 1. Get Medal Data for Each Country ---
    # Filter medals_total to get just the row for each selected country
    medals_a = medals_total[medals_total['country_code'] == country_a]
    medals_b = medals_total[medals_total['country_code'] == country_b]
    
    def get_medal_counts(df):
        """
        Extract medal counts from a filtered DataFrame.
        Returns a dictionary with Gold, Silver, Bronze, and Total counts.
        Handles the case where a country might have no medals (empty DataFrame).
        """
        if df.empty:
            # Return zeros if the country has no medal records
            return {'Gold': 0, 'Silver': 0, 'Bronze': 0, 'Total': 0}
        return {
            # .values[0] extracts the first (and only) value from the column
            'Gold': df['Gold Medal'].values[0],
            'Silver': df['Silver Medal'].values[0],
            'Bronze': df['Bronze Medal'].values[0],
            # Calculate total - check if 'Total' column exists, otherwise sum the three
            'Total': df['Total'].values[0] if 'Total' in df.columns else df['Gold Medal'].values[0] + df['Silver Medal'].values[0] + df['Bronze Medal'].values[0]
        }

    # Get medal counts for both countries using our helper function
    counts_a = get_medal_counts(medals_a)
    counts_b = get_medal_counts(medals_b)
    
    # --- 2. Get Athlete Counts ---
    # Count how many athletes each country sent
    # The len() function returns the number of rows (athletes) in the filtered DataFrame
    num_athletes_a = len(athletes[athletes['country_code'] == country_a]) if 'country_code' in athletes.columns else 0
    num_athletes_b = len(athletes[athletes['country_code'] == country_b]) if 'country_code' in athletes.columns else 0
    
    # --- 3. Get Top Sports for Each Country ---
    def get_top_sports(country_code):
        """
        Find the top 5 sports/disciplines where a country won the most medals.
        Returns a DataFrame with discipline names and medal counts.
        """
        # Filter the detailed medals DataFrame to just this country
        country_medals = medals[medals['country_code'] == country_code]
        if country_medals.empty:
            return pd.DataFrame()  # Return empty if no medals
        
        # .value_counts() counts occurrences of each unique value
        # This counts how many medals were won in each discipline
        sport_counts = country_medals['discipline'].value_counts().reset_index()
        # Rename columns from the default 'index' and 'discipline' to friendlier names
        sport_counts.columns = ['Discipline', 'Medals']
        # Return only the top 5 sports
        return sport_counts.head(5)

    top_sports_a = get_top_sports(country_a)
    top_sports_b = get_top_sports(country_b)

    # =============================================================================
    # DISPLAY COMPARISON - METRICS ROW
    # =============================================================================
    st.subheader("🏅 Overall Performance")
    
    # Create 4 columns for our comparison metrics
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    
    with m_col1:
        # Display total medals for both countries
        # st.metric() shows a number with an optional label and delta (change indicator)
        st.metric(f"{country_a} Total Medals", counts_a['Total'])
        # For Country B, we add a delta showing the difference from Country A
        # Positive delta (green arrow up) if B has more, negative (red down) if fewer
        st.metric(f"{country_b} Total Medals", counts_b['Total'], delta=int(counts_b['Total'] - counts_a['Total']))
        
    with m_col2:
        # Same pattern for gold medals
        st.metric(f"{country_a} Gold", counts_a['Gold'])
        st.metric(f"{country_b} Gold", counts_b['Gold'], delta=int(counts_b['Gold'] - counts_a['Gold']))
        
    with m_col3:
        # Athlete count comparison
        st.metric(f"{country_a} Athletes", num_athletes_a)
        st.metric(f"{country_b} Athletes", num_athletes_b, delta=int(num_athletes_b - num_athletes_a))
        
    # =============================================================================
    # VISUAL COMPARISON - BAR CHART
    # =============================================================================
    st.subheader("📊 Medal Breakdown")
    
    # Create a DataFrame structured for a grouped bar chart
    # We need one row for each country + medal type combination
    comparison_data = pd.DataFrame({
        'Country': [country_a, country_a, country_a, country_b, country_b, country_b],
        'Medal Type': ['Gold', 'Silver', 'Bronze', 'Gold', 'Silver', 'Bronze'],
        'Count': [counts_a['Gold'], counts_a['Silver'], counts_a['Bronze'], 
                  counts_b['Gold'], counts_b['Silver'], counts_b['Bronze']]
    })
    
    # Create a grouped bar chart comparing medal types between countries
    fig_medals = px.bar(
        comparison_data, 
        x='Country',  # X-axis shows the country names
        y='Count',  # Y-axis shows the medal count
        color='Medal Type',  # Different colors for gold/silver/bronze
        barmode='group',  # Bars side by side rather than stacked
        title="Medal Count Comparison",
        color_discrete_map={  # Assign specific colors to each medal type
            'Gold': '#FFD700', 
            'Silver': '#C0C0C0', 
            'Bronze': '#CD7F32'
        }
    )
    
    # st.plotly_chart() renders the chart in the Streamlit app
    # use_container_width=True makes it fill the available horizontal space
    st.plotly_chart(fig_medals, use_container_width=True)
    
    # =============================================================================
    # TOP SPORTS COMPARISON
    # =============================================================================
    st.subheader("🏆 Top Sports")
    
    # Create two columns to show each country's top sports side by side
    s_col1, s_col2 = st.columns(2)
    
    with s_col1:
        # Markdown with ** makes text bold
        st.markdown(f"**{country_a} Top Sports**")
        if not top_sports_a.empty:
            # st.dataframe() displays a DataFrame as an interactive table
            # hide_index=True removes the row number column on the left
            st.dataframe(top_sports_a, hide_index=True)
        else:
            st.write("No medals found.")
            
    with s_col2:
        st.markdown(f"**{country_b} Top Sports**")
        if not top_sports_b.empty:
            st.dataframe(top_sports_b, hide_index=True)
        else:
            st.write("No medals found.")
