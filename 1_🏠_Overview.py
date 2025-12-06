# =============================================================================
# OVERVIEW PAGE - Paris 2024 Olympics Dashboard
# =============================================================================
# This is the main entry point of the Streamlit app. It displays high-level KPIs
# (Key Performance Indicators) and visualizations giving users a quick snapshot
# of the Olympic Games data. The filename starts with "1_" so Streamlit places
# it first in the navigation menu, and the emoji helps make it visually distinct.
# =============================================================================

import streamlit as st  # Streamlit is the main framework for building web apps in Python
import plotly.express as px  # Plotly Express provides easy-to-use functions for creating interactive charts
import plotly.graph_objects as go  # Graph Objects gives more control for custom charts
import pandas as pd  # Pandas is used for data manipulation, especially with DataFrames
import sys
import os

# Add parent directory to path for imports
# This line gets the current file's directory, goes up one level (parent directory),
# and adds it to Python's path so we can import our custom utility modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#This line modifies Python's import path so the script can import modules from the parent directory of the parent directory
from utils.data_loader import load_all_data, apply_filters  # Our custom function to load all CSV data
from utils.filters import create_sidebar_filters, get_filter_summary  # Functions to create filter UI elements

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
# st.set_page_config() must be called as the FIRST Streamlit command in the script
# It sets up the browser tab title, favicon, and page layout options
st.set_page_config(
    page_title="Paris 2024 Olympics Dashboard",  # This appears in the browser tab
    page_icon="🏅",  # The favicon - can be an emoji or path to an image file
    layout="wide",  # "wide" uses the full browser width; "centered" is narrower
    initial_sidebar_state="expanded"  # Sidebar is open by default; can be "collapsed"
)

# =============================================================================
# CUSTOM CSS STYLING
# =============================================================================
# st.markdown() with unsafe_allow_html=True lets us inject raw HTML/CSS into the page
# This is useful for custom styling that Streamlit doesn't provide out of the box
# The triple quotes """ """ allow multi-line strings
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# =============================================================================
# DATA LOADING WITH CACHING
# =============================================================================
# @st.cache_data is a decorator that caches the function's return value
# This means the data is only loaded once from CSV files, then stored in memory
# Subsequent calls to get_data() return the cached data instantly - huge performance boost!
@st.cache_data
def get_data():
    return load_all_data()

# Actually call the function to get our data dictionary
# The data variable now holds all our CSVs as pandas DataFrames
data = get_data()

# =============================================================================
# SIDEBAR FILTERS
# =============================================================================
# This creates the filter widgets (dropdowns, checkboxes) in the sidebar
# The function returns a dictionary with the user's selected filter values
filters = create_sidebar_filters(data)

# =============================================================================
# MAIN PAGE HEADER
# =============================================================================
# Using our custom CSS classes to style the headers
# The HTML div tags with class names reference the CSS we defined above
st.markdown('<div class="main-header">🏅 Paris 2024 Olympic Games Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Comprehensive Analysis of the Paris 2024 Olympic Summer Games</div>', unsafe_allow_html=True)

# Welcome message using standard markdown
# Triple quotes allow us to write multi-line markdown text
# The ### creates a level-3 heading, ** makes text bold
st.markdown("""
### Welcome to the LA28 Volunteer Selection Dashboard! 🎯

This interactive dashboard provides a comprehensive analysis of the Paris 2024 Olympic Summer Games data. 
Explore athlete performances, medal distributions, global trends, and venue information across multiple analytical perspectives.

**Use the sidebar filters** to customize your view and the **navigation menu** to explore different analysis pages.
""")

# st.markdown("---") creates a horizontal divider line - great for visual separation
st.markdown("---")

# =============================================================================
# FILTER SUMMARY DISPLAY
# =============================================================================
# st.info() creates a blue information box - good for non-critical messages
# We're showing users what filters are currently active using our helper function
st.info(f"📊 {get_filter_summary(filters)}")

# =============================================================================
# KPI METRICS SECTION
# =============================================================================
# st.header() creates a large section heading - part of Streamlit's text elements
st.header("📈 Key Performance Indicators")

# Make copies of our datasets so filtering doesn't modify the original data
# .copy() is a pandas method that creates an independent copy of the DataFrame
filtered_medals = data['medals_total'].copy()
filtered_events = data['events'].copy()
filtered_athletes = data['athletes'].copy()

# Merge medals with NOCs (National Olympic Committees) to get continent information
# .merge() is like a SQL JOIN - it combines two DataFrames based on matching columns
# left_on and right_on specify which columns to match between the two DataFrames
# how='left' keeps all rows from the left DataFrame, even if no match is found
filtered_medals = filtered_medals.merge(data['nocs'][['code', 'continent']], 
                                       left_on='country_code', 
                                       right_on='code', 
                                       how='left')

# Apply country filter if the user has selected any countries
# filters['countries'] will be an empty list if nothing is selected
if filters['countries']:
    # .isin() checks if each value is in the provided list - returns True/False
    # Using this boolean mask filters the DataFrame to only matching rows
    filtered_medals = filtered_medals[filtered_medals['country_code'].isin(filters['countries'])]
    filtered_athletes = filtered_athletes[filtered_athletes['country_code'].isin(filters['countries'])]

# Apply continent filter similarly
if filters['continents']:
    filtered_medals = filtered_medals[filtered_medals['continent'].isin(filters['continents'])]
    # For athletes, we need to first add continent info by merging with NOCs
    filtered_athletes = filtered_athletes.merge(data['nocs'][['code', 'continent']], 
                                                left_on='country_code', 
                                                right_on='code', 
                                                how='left')
    filtered_athletes = filtered_athletes[filtered_athletes['continent'].isin(filters['continents'])]

# Apply sport filter to events
if filters['sports']:
    filtered_events = filtered_events[filtered_events['sport'].isin(filters['sports'])]

# =============================================================================
# CALCULATE KPI VALUES
# =============================================================================
# len() gives us the number of rows in the DataFrame - i.e., count of athletes
total_athletes = len(filtered_athletes)

# .nunique() counts the number of unique values in a column
# We check if filtered_athletes has any rows first to avoid errors
total_countries = filtered_athletes['country_code'].nunique() if len(filtered_athletes) > 0 else 0
total_sports = filtered_events['sport'].nunique() if len(filtered_events) > 0 else 0

# .sum().sum() does a double sum - first sums each column, then sums those results
# int() converts to integer so we don't display decimal points
total_medals = int(filtered_medals[['Gold Medal', 'Silver Medal', 'Bronze Medal']].sum().sum())
total_events = len(filtered_events)

# =============================================================================
# DISPLAY KPIs IN COLUMNS
# =============================================================================
# st.columns(5) creates 5 equal-width columns and returns them as a tuple
# We unpack them into 5 variables so we can work with each individually
col1, col2, col3, col4, col5 = st.columns(5)

# "with col1:" is a context manager - anything inside this block appears in column 1
with col1:
    # st.metric() creates a nice KPI display with a label and large value
    # label: the text above the number
    # value: the main number displayed - f"{:,}" adds thousand separators (e.g., 10,500)
    # help: tooltip text that appears when hovering over the metric
    st.metric(
        label="👥 Total Athletes",
        value=f"{total_athletes:,}",
        help="Total number of athletes participating"
    )

with col2:
    st.metric(
        label="🌍 Total Countries",
        value=f"{total_countries}",
        help="Total number of participating countries/NOCs"
    )

with col3:
    st.metric(
        label="⚽ Total Sports",
        value=f"{total_sports}",
        help="Total number of different sports"
    )

with col4:
    st.metric(
        label="🏅 Total Medals",
        value=f"{total_medals:,}",
        help="Total number of medals awarded"
    )

with col5:
    st.metric(
        label="🎯 Number of Events",
        value=f"{total_events:,}",
        help="Total number of events held"
    )

st.markdown("---")

# =============================================================================
# VISUALIZATIONS SECTION
# =============================================================================
# Create two columns for side-by-side charts
col_left, col_right = st.columns(2)

with col_left:
    # st.subheader() creates a smaller heading than st.header()
    st.subheader("🥇 Global Medal Distribution")
    
    # Create a simple DataFrame to hold our medal distribution data
    # This is a common pattern - prepare data in the format the chart needs
    medal_dist = pd.DataFrame({
        'Medal Type': ['Gold', 'Silver', 'Bronze'],
        'Count': [
            filtered_medals['Gold Medal'].sum(),  # Sum up all gold medals
            filtered_medals['Silver Medal'].sum(),
            filtered_medals['Bronze Medal'].sum()
        ]
    })
    
    # px.pie() creates a pie/donut chart
    # values: the numerical data that determines slice sizes
    # names: the labels for each slice
    # hole: 0.4 means 40% of the center is empty, making it a donut chart
    # color: which column to use for coloring
    # color_discrete_map: explicitly map categories to specific colors
    fig_donut = px.pie(
        medal_dist,
        values='Count',
        names='Medal Type',
        hole=0.4,  # Makes it a donut chart instead of a full pie
        color='Medal Type',
        color_discrete_map={
            'Gold': '#FFD700',  # Hex color code for gold
            'Silver': '#C0C0C0',  # Silver
            'Bronze': '#CD7F32'  # Bronze
        },
        title="Distribution of Medal Types"
    )
    
    # .update_traces() modifies the chart's visual elements
    # textposition: where to place labels ('inside', 'outside', 'auto')
    # textinfo: what text to show ('percent', 'label', 'value', or combinations)
    # hovertemplate: custom tooltip HTML - %{} are placeholders for data values
    fig_donut.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )
    
    # .update_layout() modifies the overall chart layout
    # height: chart height in pixels
    # showlegend: whether to display the legend
    # legend: dict to customize legend position and orientation
    fig_donut.update_layout(
        height=400,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    
    # st.plotly_chart() renders the Plotly figure in Streamlit
    # use_container_width=True makes the chart fill the available width
    st.plotly_chart(fig_donut, use_container_width=True)

with col_right:
    st.subheader("🏆 Top 10 Medal Standings")
    
    # Calculate total medals per country by summing the three medal columns
    filtered_medals['total'] = filtered_medals['Gold Medal'] + filtered_medals['Silver Medal'] + filtered_medals['Bronze Medal']
    
    # .nlargest(10, 'total') gets the top 10 rows by the 'total' column
    # .sort_values() sorts the data - ascending=True means smallest at bottom (for horizontal bar)
    top_countries = filtered_medals.nlargest(10, 'total').sort_values('total', ascending=True)
    
    # go.Figure() creates an empty Plotly figure that we can add traces to
    # This gives us more control than px.bar() for complex customizations
    fig_bar = go.Figure()
    
    # .add_trace() adds a new data series to the chart
    # go.Bar() creates a bar chart trace
    fig_bar.add_trace(go.Bar(
        y=top_countries['country'],  # y-axis values (country names)
        x=top_countries['total'],  # x-axis values (medal counts)
        orientation='h',  # 'h' for horizontal bars, 'v' for vertical
        marker=dict(
            color=top_countries['total'],  # Color bars by their value
            colorscale='Viridis',  # Use the Viridis color palette
            showscale=False  # Don't show the color scale legend
        ),
        text=top_countries['total'],  # Text to display on each bar
        textposition='auto',  # Let Plotly decide best text position
        hovertemplate='<b>%{y}</b><br>Total Medals: %{x}<extra></extra>'
    ))
    
    # Configure the layout
    fig_bar.update_layout(
        title="Top 10 Countries by Total Medal Count",
        xaxis_title="Total Medals",
        yaxis_title="Country",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# =============================================================================
# FOOTER / NAVIGATION GUIDE
# =============================================================================
# Multi-line markdown with navigation instructions
# The - at the start of lines creates a bullet list
st.markdown("""
---
### 🎯 Navigation Guide

Use the **sidebar menu** to explore different analytical perspectives:

- **🏠 Overview** (Current Page): High-level KPIs and medal standings
- **🗺️ Global Analysis**: Geographic and continent-based medal analysis
- **👤 Athlete Performance**: Athlete demographics and top performers
- **🏟️ Sports and Events**: Event schedules, venues, and sport-specific analysis

---

💡 **Tip**: Use the filters in the sidebar to customize your analysis!

*Dashboard created for the LA28 Volunteer Selection Challenge*
""")
