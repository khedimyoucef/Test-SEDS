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

# Page configuration
st.set_page_config(
    page_title="Sports & Events - Paris 2024",
    page_icon="🏟️",
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
st.title("🏟️ Sports, Events & Venues")
st.markdown("Explore event schedules, sport-specific medal distributions, and Olympic venue locations")
st.info(f"📊 {get_filter_summary(filters)}")
st.markdown("---")

# 1. Event Schedule Timeline/Gantt Chart
st.header("📅 Event Schedule Timeline")
st.markdown("Visualize when events took place during the Games")

# Prepare schedule data
schedule_df = data['schedule'].copy()

# Sport/Venue selector for timeline
timeline_view = st.radio("View schedule by:", ["Discipline", "Venue"], horizontal=True)

if timeline_view == "Discipline":
    selected_discipline = st.selectbox(
        "Select a discipline to view its schedule:",
        options=sorted(schedule_df['discipline'].dropna().unique().tolist())
    )
    schedule_filtered = schedule_df[schedule_df['discipline'] == selected_discipline].copy()
else:
    selected_venue = st.selectbox(
        "Select a venue to view its schedule:",
        options=sorted(schedule_df['venue'].dropna().unique().tolist())
    )
    schedule_filtered = schedule_df[schedule_df['venue'] == selected_venue].copy()

# Convert date columns
if 'start_date' in schedule_filtered.columns and 'end_date' in schedule_filtered.columns:
    schedule_filtered['start_date'] = pd.to_datetime(schedule_filtered['start_date'], errors='coerce')
    schedule_filtered['end_date'] = pd.to_datetime(schedule_filtered['end_date'], errors='coerce')
    
    # Remove rows with invalid dates
    schedule_filtered = schedule_filtered.dropna(subset=['start_date', 'end_date'])
    
    if len(schedule_filtered) > 0:
        # Create Gantt chart
        fig_gantt = px.timeline(
            schedule_filtered.head(50),  # Limit to 50 events for readability
            x_start='start_date',
            x_end='end_date',
            y='event',
            color='discipline' if timeline_view == "Venue" else 'venue',
            title=f'Event Schedule for {selected_discipline if timeline_view == "Discipline" else selected_venue}',
            labels={'event': 'Event', 'discipline': 'Discipline', 'venue': 'Venue'}
        )
        
        fig_gantt.update_layout(
            height=600,
            xaxis_title='Date',
            yaxis_title='Event',
            showlegend=True
        )
        
        st.plotly_chart(fig_gantt, use_container_width=True)
        
        if len(schedule_filtered) > 50:
            st.info(f"📊 Showing 50 of {len(schedule_filtered)} events. Use filters to narrow down the view.")
    else:
        st.warning("No valid date information available for the selected filter.")
else:
    # Fallback: Show event count by date if timeline data not available
    st.info("Detailed timeline data not available. Showing event distribution instead.")
    
    # Simple bar chart of events
    event_counts = schedule_filtered.groupby('event').size().reset_index(name='count').head(20)
    fig_bar = px.bar(
        event_counts,
        x='event',
        y='count',
        title=f'Events in {selected_discipline if timeline_view == "Discipline" else selected_venue}',
        labels={'count': 'Occurrences', 'event': 'Event'}
    )
    fig_bar.update_layout(height=400)
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# 2. Medal Count by Sport (Treemap)
st.header("🎯 Medal Count by Sport")
st.markdown("Hierarchical view of medals distributed across different sports")

# Prepare medals by sport
medals_detail = data['medals'].copy()

# Apply filters
if filters['countries']:
    medals_detail = medals_detail[medals_detail['country_code'].isin(filters['countries'])]

if filters['sports']:
    medals_detail = medals_detail[medals_detail['discipline'].isin(filters['sports'])]

if filters['medal_types']:
    medals_detail = medals_detail[medals_detail['medal_type'].isin(filters['medal_types'])]

# Add continent info
medals_detail = medals_detail.merge(
    data['nocs'][['code', 'continent']],
    left_on='country_code',
    right_on='code',
    how='left'
)

if filters['continents']:
    medals_detail = medals_detail[medals_detail['continent'].isin(filters['continents'])]

# Count medals by sport
sport_medals = medals_detail.groupby(['discipline', 'medal_type']).size().reset_index(name='count')
sport_totals = sport_medals.groupby('discipline')['count'].sum().reset_index(name='total')

# Create treemap
fig_treemap = px.treemap(
    sport_totals,
    path=['discipline'],
    values='total',
    title='Medal Distribution Across Sports',
    color='total',
    color_continuous_scale='Viridis',
    labels={'total': 'Total Medals'}
)

fig_treemap.update_traces(
    textposition='middle center',
    textfont_size=12
)

fig_treemap.update_layout(height=500)
st.plotly_chart(fig_treemap, use_container_width=True)

# Detailed breakdown
with st.expander("📊 View Detailed Sport-wise Medal Breakdown"):
    sport_breakdown = medals_detail.groupby(['discipline', 'medal_type']).size().reset_index(name='count')
    sport_breakdown_pivot = sport_breakdown.pivot(index='discipline', columns='medal_type', values='count').fillna(0)
    sport_breakdown_pivot['Total'] = sport_breakdown_pivot.sum(axis=1)
    sport_breakdown_pivot = sport_breakdown_pivot.sort_values('Total', ascending=False)
    
    st.dataframe(sport_breakdown_pivot, use_container_width=True)

st.markdown("---")

# 3. Venue Map (Scatter Mapbox)
st.header("🗼 Olympic Venues in Paris")
st.markdown("Explore the locations of Olympic venues across the Paris region")

# Prepare venues data
venues_df = data['venues'].copy()

# Check if we have coordinates
if 'lat' in venues_df.columns and 'lon' in venues_df.columns:
    venues_df = venues_df.dropna(subset=['lat', 'lon'])
    
    if len(venues_df) > 0:
        # Create scatter mapbox
        fig_map = px.scatter_mapbox(
            venues_df,
            lat='lat',
            lon='lon',
            hover_name='venue',
            hover_data={
                'lat': False,
                'lon': False,
                'venue': True
            },
            color_discrete_sequence=['#FF6B6B'],
            zoom=10,
            height=600,
            title='Olympic Venues Map'
        )
        
        fig_map.update_layout(
            mapbox_style='open-street-map',
            margin={"r": 0, "t": 40, "l": 0, "b": 0}
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
        
        # Venue statistics
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Venues", len(venues_df))
        
        with col2:
            # Count events per venue
            venue_events = schedule_df.groupby('venue').size().reset_index(name='event_count')
            if len(venue_events) > 0:
                busiest_venue = venue_events.nlargest(1, 'event_count')
                st.metric(
                    "Busiest Venue",
                    busiest_venue.iloc[0]['venue'][:30] + "..." if len(busiest_venue.iloc[0]['venue']) > 30 else busiest_venue.iloc[0]['venue'],
                    f"{int(busiest_venue.iloc[0]['event_count'])} events"
                )
    else:
        st.warning("No coordinate data available for venues.")
        st.info("Showing venue list instead:")
        st.dataframe(venues_df[['venue']].drop_duplicates(), use_container_width=True)
else:
    # Fallback: Show venue list
    st.info("Geographic coordinates not available. Showing venue information:")
    
    # Show venues with event counts
    venue_events = schedule_df.groupby('venue').size().reset_index(name='event_count').sort_values('event_count', ascending=False)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.dataframe(venue_events, use_container_width=True, height=400)
    
    with col2:
        # Pie chart of top venues by event count
        fig_venues = px.pie(
            venue_events.head(10),
            values='event_count',
            names='venue',
            title='Top 10 Venues by Event Count'
        )
        st.plotly_chart(fig_venues, use_container_width=True)

st.markdown("---")

# Additional insights
st.subheader("📊 Sports & Events Insights")

col1, col2, col3 = st.columns(3)

with col1:
    total_sports = schedule_df['discipline'].nunique()
    st.metric("Total Disciplines", total_sports)

with col2:
    total_events = len(schedule_df)
    st.metric("Total Events", f"{total_events:,}")

with col3:
    if len(sport_totals) > 0:
        top_sport = sport_totals.nlargest(1, 'total')
        st.metric(
            "Most Medals Awarded",
            top_sport.iloc[0]['discipline'][:25] + "..." if len(top_sport.iloc[0]['discipline']) > 25 else top_sport.iloc[0]['discipline'],
            f"{int(top_sport.iloc[0]['total'])} medals"
        )

# Sport comparison
st.markdown("---")
st.subheader("⚔️ Sport-by-Sport Medal Comparison")

# Bar chart comparing sports
fig_sport_compare = px.bar(
    sport_medals,
    x='discipline',
    y='count',
    color='medal_type',
    barmode='stack',
    title='Medal Distribution Across All Disciplines',
    labels={'count': 'Number of Medals', 'discipline': 'Discipline'},
    color_discrete_map={
        'Gold Medal': '#FFD700',
        'Silver Medal': '#C0C0C0',
        'Bronze Medal': '#CD7F32'
    },
    height=500
)

fig_sport_compare.update_layout(
    xaxis={'categoryorder': 'total descending'},
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig_sport_compare, use_container_width=True)
