import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_loader import load_all_data
from utils.filters import create_sidebar_filters, get_filter_summary
from utils.ioc_iso_mapping import get_iso_code

# Page configuration
st.set_page_config(
    page_title="Global Analysis - Paris 2024",
    page_icon="🗺️",
    layout="wide"
)

# Load data
@st.cache_data
def get_data():
    return load_all_data()

data = get_data()

# Create sidebar filters
filters = create_sidebar_filters(data)

# Page header
st.title("🗺️ Global & Continental Analysis")
st.markdown("Explore medal distributions across continents and countries with interactive geographical visualizations")
st.info(f"📊 {get_filter_summary(filters)}")
st.markdown("---")

# Prepare medals data with continent info
medals_df = data['medals_total'].copy()
medals_df = medals_df.merge(
    data['nocs'][['code', 'continent']], 
    left_on='country_code', 
    right_on='code', 
    how='left'
)

# Apply filters
if filters['countries']:
    medals_df = medals_df[medals_df['country_code'].isin(filters['countries'])]

if filters['continents']:
    medals_df = medals_df[medals_df['continent'].isin(filters['continents'])]

# Calculate total medals
medals_df['total_medals'] = medals_df['Gold Medal'] + medals_df['Silver Medal'] + medals_df['Bronze Medal']

# Add ISO codes for map
medals_df['iso_code'] = medals_df['country_code'].apply(get_iso_code)

# 1. World Medal Map (Choropleth)
st.header("🌍 World Medal Map")
st.markdown("Countries colored by their total medal count")

# Create choropleth map
fig_map = px.choropleth(
    medals_df,
    locations='iso_code',
    locationmode='ISO-3',
    color='total_medals',
    hover_name='country',
    hover_data={
        'country_code': False,
        'Gold Medal': True,
        'Silver Medal': True,
        'Bronze Medal': True,
        'total_medals': True
    },
    color_continuous_scale='Viridis',
    labels={'total_medals': 'Total Medals'},
    title='Global Medal Distribution by Country'
)

fig_map.update_layout(
    height=500,
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='natural earth'
    )
)

st.plotly_chart(fig_map, use_container_width=True)

st.markdown("---")

# 2. Medal Hierarchy by Continent (Sunburst)
st.header("☀️ Medal Hierarchy: Continent → Country → Discipline")
st.markdown("Drill down from continent to country to discipline to see medal distributions")

# Prepare hierarchical data
# Get medals by sport from medals.csv
medals_detail = data['medals'].copy()
medals_detail = medals_detail.merge(
    data['nocs'][['code', 'continent']],
    left_on='country_code',
    right_on='code',
    how='left'
)

# Apply filters
if filters['countries']:
    medals_detail = medals_detail[medals_detail['country_code'].isin(filters['countries'])]

if filters['continents']:
    medals_detail = medals_detail[medals_detail['continent'].isin(filters['continents'])]

if filters['sports']:
    medals_detail = medals_detail[medals_detail['discipline'].isin(filters['sports'])]

if filters['medal_types']:
    medals_detail = medals_detail[medals_detail['medal_type'].isin(filters['medal_types'])]

# Create hierarchy
hierarchy_data = medals_detail.groupby(['continent', 'country', 'discipline']).size().reset_index(name='medal_count')

col1, col2 = st.columns(2)

with col1:
    # Sunburst chart
    fig_sunburst = px.sunburst(
        hierarchy_data,
        path=['continent', 'country', 'discipline'],
        values='medal_count',
        title='Medal Hierarchy - Sunburst View',
        color='medal_count',
        color_continuous_scale='RdYlGn'
    )
    
    fig_sunburst.update_layout(height=500)
    st.plotly_chart(fig_sunburst, use_container_width=True)

with col2:
    # Treemap chart
    fig_treemap = px.treemap(
        hierarchy_data,
        path=['continent', 'country', 'discipline'],
        values='medal_count',
        title='Medal Hierarchy - Treemap View',
        color='medal_count',
        color_continuous_scale='Blues'
    )
    
    fig_treemap.update_layout(height=500)
    st.plotly_chart(fig_treemap, use_container_width=True)

st.markdown("---")

# 3. Continent vs. Medals Bar Chart
st.header("🌐 Medal Distribution by Continent")
st.markdown("Compare medal performance across continents")

# Aggregate medals by continent
continent_medals = medals_df.groupby('continent').agg({
    'Gold Medal': 'sum',
    'Silver Medal': 'sum',
    'Bronze Medal': 'sum'
}).reset_index()

# Melt for grouped bar chart
continent_medals_melted = continent_medals.melt(
    id_vars='continent',
    value_vars=['Gold Medal', 'Silver Medal', 'Bronze Medal'],
    var_name='medal_type',
    value_name='count'
)

# Create grouped bar chart
fig_continent = px.bar(
    continent_medals_melted,
    x='continent',
    y='count',
    color='medal_type',
    barmode='group',
    title='Medal Count by Continent and Type',
    labels={'count': 'Number of Medals', 'continent': 'Continent', 'medal_type': 'Medal Type'},
    color_discrete_map={
        'Gold Medal': '#FFD700',
        'Silver Medal': '#C0C0C0',
        'Bronze Medal': '#CD7F32'
    }
)

fig_continent.update_layout(height=400)
st.plotly_chart(fig_continent, use_container_width=True)

st.markdown("---")

# 4. Country vs. Medals (Top 20)
st.header("🏆 Top 20 Countries Medal Comparison")
st.markdown("Detailed medal breakdown for the leading nations")

# Get top 20 countries
top_20_countries = medals_df.nlargest(20, 'total_medals')

# Melt for grouped bar chart
top_20_melted = top_20_countries.melt(
    id_vars='country',
    value_vars=['Gold Medal', 'Silver Medal', 'Bronze Medal'],
    var_name='medal_type',
    value_name='count'
)

# Create grouped bar chart
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
    hover_data={'count': True}
)

fig_top20.update_layout(
    height=500,
    xaxis={'categoryorder': 'total descending'}
)

st.plotly_chart(fig_top20, use_container_width=True)

# Additional insights
st.markdown("---")
st.subheader("📊 Continental Insights")

col1, col2, col3 = st.columns(3)

with col1:
    top_continent = continent_medals.nlargest(1, 'Gold Medal')
    if not top_continent.empty:
        st.metric(
            "🥇 Top Continent (Gold)",
            top_continent.iloc[0]['continent'],
            f"{int(top_continent.iloc[0]['Gold Medal'])} gold medals"
        )

with col2:
    total_continents = len(continent_medals[continent_medals['Gold Medal'] > 0])
    st.metric(
        "🌍 Continents with Medals",
        total_continents,
        "out of 6 continents"
    )

with col3:
    avg_medals = medals_df['total_medals'].mean()
    st.metric(
        "📈 Average Medals per Country",
        f"{avg_medals:.1f}",
        "across all participating nations"
    )
