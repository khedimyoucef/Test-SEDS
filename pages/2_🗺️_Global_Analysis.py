# =============================================================================
# GLOBAL ANALYSIS PAGE - Geographic and Continental Medal Analysis
# =============================================================================
# This page provides geographic visualizations of Olympic data including:
# - A world map (choropleth) showing medal distribution
# - Sunburst and treemap charts for hierarchical data exploration
# - Continental medal comparisons and country rankings
# The "2_" prefix places this second in the navigation menu.
# =============================================================================

import streamlit as st  # Main framework for building the web interface
import plotly.express as px  # High-level charting library for quick visualizations
import plotly.graph_objects as go  # Lower-level Plotly for custom charts
import pandas as pd  # Data manipulation library
import sys
import os

# Add parent directory to path so we can import our utility modules
# os.path.abspath(__file__) gets the absolute path of THIS file
# os.path.dirname() gets the directory containing that file
# Doing it twice goes up two directory levels (from pages/ to project root)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_loader import load_all_data
from utils.filters import create_sidebar_filters, get_filter_summary
from utils.ioc_iso_mapping import get_iso_code  # Converts IOC country codes to ISO codes for maps

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
# Each page in a multi-page Streamlit app needs its own set_page_config()
# This sets the browser tab title and icon for when this page is active
st.set_page_config(
    page_title="Global Analysis - Paris 2024",
    page_icon="🗺️",
    layout="wide"  # Use full width of the browser
)

# =============================================================================
# DATA LOADING
# =============================================================================
# Using the same caching pattern as the main page
# Even though we load data on every page, caching means it's only actually
# loaded from disk once - all pages share the same cached data
@st.cache_data
def get_data():
    return load_all_data()

data = get_data()

# Create sidebar filters - this function handles all the UI widgets
# and returns a dictionary with the user's selections
filters = create_sidebar_filters(data)

# =============================================================================
# PAGE HEADER
# =============================================================================
# st.title() creates the largest heading size - the main page title
st.title("🗺️ Global & Continental Analysis")

# Regular markdown for a subtitle/description
st.markdown("Explore medal distributions across continents and countries with interactive geographical visualizations")

# Show which filters are currently active using an info box
st.info(f"📊 {get_filter_summary(filters)}")

# Horizontal divider line
st.markdown("---")

# =============================================================================
# PREPARE MEDALS DATA WITH CONTINENT INFORMATION
# =============================================================================
# Start with a copy of the medal totals by country
medals_df = data['medals_total'].copy()

# Merge with NOCs data to add continent information to each country
# We're selecting only the 'code' and 'continent' columns from nocs
# The merge joins on country_code (left) matching code (right)
medals_df = medals_df.merge(
    data['nocs'][['code', 'continent']], 
    left_on='country_code', 
    right_on='code', 
    how='left'  # Keep all rows from medals_df even if no NOC match
)

# =============================================================================
# APPLY USER FILTERS
# =============================================================================
# Only filter if the user has made selections (empty list = no filter)
if filters['countries']:
    medals_df = medals_df[medals_df['country_code'].isin(filters['countries'])]

if filters['continents']:
    medals_df = medals_df[medals_df['continent'].isin(filters['continents'])]

# Calculate total medals per country (sum of gold + silver + bronze)
medals_df['total_medals'] = medals_df['Gold Medal'] + medals_df['Silver Medal'] + medals_df['Bronze Medal']
#this is a new cell in the medals df dataframe
# Add ISO codes for the map - Plotly maps use ISO-3 country codes
# Our data uses IOC codes (like 'USA', 'GBR') which are similar but not identical
# The get_iso_code function converts them (e.g., 'GER' -> 'DEU')
medals_df['iso_code'] = medals_df['country_code'].apply(get_iso_code)
#getting a new cell form the country code by appluing the get iso code from country code
# =============================================================================
# SECTION 1: WORLD MEDAL MAP (CHOROPLETH)
# =============================================================================
st.header("🌍 World Medal Map")
st.markdown("Countries colored by their total medal count")

# px.choropleth() creates a world map with countries colored by data values
# A choropleth is a thematic map where areas are shaded based on a variable
fig_map = px.choropleth(
    medals_df,  # The DataFrame containing our data with the filters applied when needed
    locations='iso_code',  # Column with country identifiers (as said prev the colorpleth takes ISO 3 codes for locations as input)
    locationmode='ISO-3',  # Tells Plotly we're using ISO alpha-3 codes
    color='total_medals',  # Column that determines the color intensity
    hover_name='country',  # What to show as the main text when hovering
    hover_data={  # Additional data to show in the tooltip
        'country_code': False,  # Hide this field in hover
        'Gold Medal': True,  # Show these fields
        'Silver Medal': True,
        'Bronze Medal': True,
        'total_medals': True
    },
    color_continuous_scale='Viridis',  # Color gradient from purple to yellow
    labels={'total_medals': 'Total Medals'},  # Rename columns in the legend/tooltip
    title='Global Medal Distribution by Country'
)

# Customize the map appearance
fig_map.update_layout(
    height=500,  # Chart height in pixels
    geo=dict(
        showframe=False,  # Hide the border around the map
        showcoastlines=True,  # Show coastline boundaries
        projection_type='natural earth'  # Map projection style (how 3D earth is shown in 2D)
    )
)

# Display the map in Streamlit
st.plotly_chart(fig_map, use_container_width=True)

st.markdown("---")

# =============================================================================
# SECTION 2: MEDAL HIERARCHY (SUNBURST AND TREEMAP)
# =============================================================================
st.header("☀️ Medal Hierarchy: Continent → Country → Discipline")
st.markdown("Drill down from continent to country to discipline to see medal distributions")

# For this visualization, we need the detailed medals data (each medal awarded)
# rather than the aggregated totals
medals_detail = data['medals'].copy()

# Add continent information by merging with NOCs
medals_detail = medals_detail.merge(
    data['nocs'][['code', 'continent']],
    left_on='country_code',
    right_on='code',
    how='left'
)

# Apply all the user's filters to this dataset too
if filters['countries']:
    medals_detail = medals_detail[medals_detail['country_code'].isin(filters['countries'])]

if filters['continents']:
    medals_detail = medals_detail[medals_detail['continent'].isin(filters['continents'])]

if filters['sports']:
    # The detailed medals DataFrame uses 'discipline' instead of 'sport'
    medals_detail = medals_detail[medals_detail['discipline'].isin(filters['sports'])]

if filters['medal_types']:
    medals_detail = medals_detail[medals_detail['medal_type'].isin(filters['medal_types'])]

# Create hierarchical data by grouping and counting
# .groupby() groups rows by the specified columns
# .size() counts the rows in each group
# .reset_index(name='medal_count') converts the result back to a DataFrame
hierarchy_data = medals_detail.groupby(['continent', 'country', 'discipline']).size().reset_index(name='medal_count')

# Create two columns to show sunburst and treemap side by side
col1, col2 = st.columns(2)

with col1:
    # px.sunburst() creates a radial hierarchical chart
    # Great for showing part-to-whole relationships across multiple levels
    fig_sunburst = px.sunburst(
        hierarchy_data,
        path=['continent', 'country', 'discipline'],  # The hierarchy levels from center outward
        values='medal_count',  # Size of each segment
        title='Medal Hierarchy - Sunburst View',
        color='medal_count',  # Also color by medal count
        color_continuous_scale='RdYlGn'  # Red-Yellow-Green color scale
    )
    
    fig_sunburst.update_layout(height=500)
    st.plotly_chart(fig_sunburst, use_container_width=True)

with col2:
    # px.treemap() creates a rectangular hierarchical chart
    # Shows the same hierarchy but with nested rectangles instead of rings
    fig_treemap = px.treemap(
        hierarchy_data,
        path=['continent', 'country', 'discipline'],  # Same hierarchy as sunburst
        values='medal_count',
        title='Medal Hierarchy - Treemap View',
        color='medal_count',
        color_continuous_scale='Blues'  # Different color scheme for variety
    )
    
    fig_treemap.update_layout(height=500)
    st.plotly_chart(fig_treemap, use_container_width=True)

st.markdown("---")

# =============================================================================
# SECTION 3: CONTINENT VS MEDALS BAR CHART
# =============================================================================
st.header("🌐 Medal Distribution by Continent")
st.markdown("Compare medal performance across continents")

# Aggregate medals by continent using .groupby() and .agg()
# .agg() lets us apply different functions to different columns
# Here we're summing up all medal columns for each continent
continent_medals = medals_df.groupby('continent').agg({
    'Gold Medal': 'sum',
    'Silver Medal': 'sum',
    'Bronze Medal': 'sum'
}).reset_index()
# reset_index() is needed here because the 'continent' column, after groupby(),
# becomes the DataFrame's index. The subsequent .melt() operation expects
# 'continent' to be a regular column, specified by id_vars='continent'.
# Without reset_index(), 'continent' would not be found as a column for id_vars.
# If reset_index() were omi tted, you would need to use `continent_medals.index.name`
# or similar to access the continent values, or reset the index before melting.
# For clarity and direct use with id_vars, reset_index() is appropriate.

# "Melt" the DataFrame from wide to long format for a grouped bar chart
# Wide format: one column per medal type
# Long format: one row per continent + medal type combination
# This is what Plotly needs for grouped/stacked bar charts with a color dimension
continent_medals_melted = continent_medals.melt(
    id_vars='continent',  # Keep this column as-is
    value_vars=['Gold Medal', 'Silver Medal', 'Bronze Medal'],  # These columns become rows
    var_name='medal_type',  # New column for the original column names
    value_name='count'  # New column for the values
)

# Create a grouped bar chart
fig_continent = px.bar(
    continent_medals_melted,
    x='continent',  # X-axis categories
    y='count',  # Y-axis values (bar heights)
    color='medal_type',  # Different colors for each medal type
    barmode='group',  # 'group' puts bars side by side; 'stack' stacks them
    title='Medal Count by Continent and Type',
    labels={  # Rename columns for display
        'count': 'Number of Medals', 
        'continent': 'Continent', 
        'medal_type': 'Medal Type'
    },
    color_discrete_map={  # Assign specific colors to each medal type
        'Gold Medal': '#FFD700',
        'Silver Medal': '#C0C0C0',
        'Bronze Medal': '#CD7F32'
    }
)

fig_continent.update_layout(height=400)
st.plotly_chart(fig_continent, use_container_width=True)

st.markdown("---")

# =============================================================================
# SECTION 4: TOP 20 COUNTRIES COMPARISON
# =============================================================================
st.header("🏆 Top 20 Countries Medal Comparison")
st.markdown("Detailed medal breakdown for the leading nations")

# Get top 20 countries by total medals using .nlargest()
top_20_countries = medals_df.nlargest(20, 'total_medals')

# Melt to long format for the grouped bar chart (same pattern as continents)
top_20_melted = top_20_countries.melt(
    id_vars='country',
    value_vars=['Gold Medal', 'Silver Medal', 'Bronze Medal'],
    var_name='medal_type',
    value_name='count'
)

# Create grouped bar chart for top 20 countries
fig_top20 = px.bar(
    top_20_melted,
    x='country',
    y='count',
    color='medal_type',
    barmode='group',
    title='Top 20 Countries: Medal Breakdown',
    labels={'count': 'Number of Medals', 'country': 'Country', 'medal_type': 'Medal Type'},
    color_discrete_map={
        'Gold Medal': '#FFD700',
        'Silver Medal': '#C0C0C0',
        'Bronze Medal': '#CD7F32'
    },
    hover_data={'count': True}  # Show count in the hover tooltip
)

fig_top20.update_layout(
    height=500,
    xaxis={'categoryorder': 'total descending'}  # Order bars by total (highest first)
)

st.plotly_chart(fig_top20, use_container_width=True)

# =============================================================================
# ADDITIONAL INSIGHTS - METRIC CARDS
# =============================================================================
st.markdown("---")
st.subheader("📊 Continental Insights")

# Create three columns for insight metrics
col1, col2, col3 ,col4 = st.columns(4)

with col1:
    # Find the continent with the most gold medals
    top_continent = continent_medals.nlargest(1, 'Gold Medal')
    if not top_continent.empty:  # Check the DataFrame isn't empty
        # st.metric() with a delta parameter shows a small secondary value
        st.metric(
            "🥇 Top Continent (Gold)",
            top_continent.iloc[0]['continent'],  # .iloc[0] gets the first row
            f"{int(top_continent.iloc[0]['Gold Medal'])} gold medals"  # This appears as a small value below
        )

with col2:
    # Count how many continents won at least one gold medal
    total_continents = len(continent_medals[continent_medals['Gold Medal'] > 0])
    st.metric(
        "🌍 Continents with Medals",
        total_continents,
        "out of 6 continents"
    )

with col3:
    # Count how many countries won at least one gold medal
    # medals_df['Gold Medal'] > 0 creates a boolean Series
    # .sum() on a boolean Series counts the number of True values
    countries_with_gold = (medals_df['Gold Medal'] > 0).sum()
    st.metric(
        "🥇 Countries with Gold",
        countries_with_gold,
        "nations with at least one gold medal"
    )


with col4:
    # Calculate average medals per country
    avg_medals = medals_df['total_medals'].mean()  # .mean() calculates the average
    st.metric(
        "📈 Average Medals per Country",
        f"{avg_medals:.1f}",  # :.1f formats to 1 decimal place
        "across all participating nations"
    )
