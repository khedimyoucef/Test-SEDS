import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_loader import load_all_data, apply_filters
from utils.filters import create_sidebar_filters, get_filter_summary

# Page configuration
st.set_page_config(
    page_title="Paris 2024 Olympics Dashboard",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
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

# Load data
@st.cache_data
def get_data():
    return load_all_data()

data = get_data()

# Create sidebar filters
filters = create_sidebar_filters(data)

# Main content
st.markdown('<div class="main-header">🏅 Paris 2024 Olympic Games Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Comprehensive Analysis of the Paris 2024 Olympic Summer Games</div>', unsafe_allow_html=True)

# Welcome message
st.markdown("""
### Welcome to the LA28 Volunteer Selection Dashboard! 🎯

This interactive dashboard provides a comprehensive analysis of the Paris 2024 Olympic Summer Games data. 
Explore athlete performances, medal distributions, global trends, and venue information across multiple analytical perspectives.

**Use the sidebar filters** to customize your view and the **navigation menu** to explore different analysis pages.
""")

st.markdown("---")

# Display filter summary
st.info(f"📊 {get_filter_summary(filters)}")

# KPI Metrics Section
st.header("📈 Key Performance Indicators")

# Apply filters to relevant datasets
filtered_medals = data['medals_total'].copy()
filtered_events = data['events'].copy()
filtered_athletes = data['athletes'].copy()

# Merge with NOCs to get continent info for filtering
filtered_medals = filtered_medals.merge(data['nocs'][['code', 'continent']], 
                                       left_on='country_code', 
                                       right_on='code', 
                                       how='left')

if filters['countries']:
    filtered_medals = filtered_medals[filtered_medals['country_code'].isin(filters['countries'])]
    filtered_athletes = filtered_athletes[filtered_athletes['country_code'].isin(filters['countries'])]

if filters['continents']:
    filtered_medals = filtered_medals[filtered_medals['continent'].isin(filters['continents'])]
    # For athletes, need to merge with nocs first
    filtered_athletes = filtered_athletes.merge(data['nocs'][['code', 'continent']], 
                                                left_on='country_code', 
                                                right_on='code', 
                                                how='left')
    filtered_athletes = filtered_athletes[filtered_athletes['continent'].isin(filters['continents'])]

if filters['sports']:
    filtered_events = filtered_events[filtered_events['sport'].isin(filters['sports'])]

# Calculate KPIs
total_athletes = len(filtered_athletes)
total_countries = filtered_athletes['country_code'].nunique() if len(filtered_athletes) > 0 else 0
total_sports = filtered_events['sport'].nunique() if len(filtered_events) > 0 else 0
total_medals = int(filtered_medals[['Gold Medal', 'Silver Medal', 'Bronze Medal']].sum().sum())
total_events = len(filtered_events)

# Display KPIs in columns
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
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

# Visualizations
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🥇 Global Medal Distribution")
    
    # Calculate medal distribution
    medal_dist = pd.DataFrame({
        'Medal Type': ['Gold', 'Silver', 'Bronze'],
        'Count': [
            filtered_medals['Gold Medal'].sum(),
            filtered_medals['Silver Medal'].sum(),
            filtered_medals['Bronze Medal'].sum()
        ]
    })
    
    # Create donut chart
    fig_donut = px.pie(
        medal_dist,
        values='Count',
        names='Medal Type',
        hole=0.4,
        color='Medal Type',
        color_discrete_map={
            'Gold': '#FFD700',
            'Silver': '#C0C0C0',
            'Bronze': '#CD7F32'
        },
        title="Distribution of Medal Types"
    )
    
    fig_donut.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )
    
    fig_donut.update_layout(
        height=400,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    
    st.plotly_chart(fig_donut, use_container_width=True)

with col_right:
    st.subheader("🏆 Top 10 Medal Standings")
    
    # Calculate total medals per country
    filtered_medals['total'] = filtered_medals['Gold Medal'] + filtered_medals['Silver Medal'] + filtered_medals['Bronze Medal']
    top_countries = filtered_medals.nlargest(10, 'total').sort_values('total', ascending=True)
    
    # Create horizontal bar chart
    fig_bar = go.Figure()
    
    fig_bar.add_trace(go.Bar(
        y=top_countries['country'],
        x=top_countries['total'],
        orientation='h',
        marker=dict(
            color=top_countries['total'],
            colorscale='Viridis',
            showscale=False
        ),
        text=top_countries['total'],
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Total Medals: %{x}<extra></extra>'
    ))
    
    fig_bar.update_layout(
        title="Top 10 Countries by Total Medal Count",
        xaxis_title="Total Medals",
        yaxis_title="Country",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# Footer
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
