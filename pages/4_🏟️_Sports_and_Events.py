# =============================================================================
# SPORTS AND EVENTS PAGE
# =============================================================================
# This page focuses on the sports, events, and venues of the Paris 2024 Olympics.
# Features include:
# - Event schedule timeline visualized as a Gantt chart
# - Medal distribution by sport shown as a treemap
# - Interactive map of Olympic venues using scatter_mapbox
# - Sport-by-sport medal comparison
# =============================================================================

import streamlit as st  # The main framework for building web apps
import plotly.express as px  # High-level charting library
import plotly.graph_objects as go  # Lower-level Plotly for custom charts
import pandas as pd  # Data manipulation library
import sys
import os

# Add parent directory to path so we can import our utility modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_loader import load_all_data
from utils.filters import create_sidebar_filters, get_filter_summary

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="Sports & Events - Paris 2024",
    page_icon="🏟️",
    layout="wide"
)

# =============================================================================
# DATA LOADING
# =============================================================================
# Use caching to avoid reloading data on every user interaction
@st.cache_data
def get_data():
    return load_all_data()

data = get_data()

# Create sidebar filters for user interaction
filters = create_sidebar_filters(data)

# =============================================================================
# PAGE HEADER
# =============================================================================
st.title("🏟️ Sports, Events & Venues")
st.markdown("Explore event schedules, sport-specific medal distributions, and Olympic venue locations")

# Show active filters
st.info(f"📊 {get_filter_summary(filters)}")
st.markdown("---")

# =============================================================================
# SECTION 1: EVENT SCHEDULE TIMELINE (GANTT CHART)
# =============================================================================
st.header("📅 Event Schedule Timeline")
st.markdown("Visualize when events took place during the Games")

# Get the schedule data
schedule_df = data['schedule'].copy()

# st.radio() creates a horizontal set of options for the user to choose from
# horizontal=True places the options in a row instead of a vertical list
timeline_view = st.radio("View schedule by:", ["Discipline", "Venue"], horizontal=True)

# Show different selectors based on the user's choice
if timeline_view == "Discipline":
    # st.selectbox() creates a searchable dropdown menu
    selected_discipline = st.selectbox(
        "Select a discipline to view its schedule:",
        options=sorted(schedule_df['discipline'].dropna().unique().tolist())
    )
    # Filter the schedule to only the selected discipline
    schedule_filtered = schedule_df[schedule_df['discipline'] == selected_discipline].copy()
else:
    selected_venue = st.selectbox(
        "Select a venue to view its schedule:",
        options=sorted(schedule_df['venue'].dropna().unique().tolist())
    )
    schedule_filtered = schedule_df[schedule_df['venue'] == selected_venue].copy()

# Check if we have the date columns needed for a timeline/Gantt chart
if 'start_date' in schedule_filtered.columns and 'end_date' in schedule_filtered.columns:
    # Convert date columns to datetime objects
    # errors='coerce' turns invalid dates into NaT (Not a Time) instead of raising an error
    schedule_filtered['start_date'] = pd.to_datetime(schedule_filtered['start_date'], errors='coerce')
    schedule_filtered['end_date'] = pd.to_datetime(schedule_filtered['end_date'], errors='coerce')
    
    # Remove any rows with invalid dates
    schedule_filtered = schedule_filtered.dropna(subset=['start_date', 'end_date'])
    
    if len(schedule_filtered) > 0:
        # px.timeline() creates a Gantt chart - perfect for showing time ranges
        # Gantt charts show when activities start and end over time
        fig_gantt = px.timeline(
            schedule_filtered.head(50),  # Limit to 50 events for readability
            x_start='start_date',  # When each event starts
            x_end='end_date',  # When each event ends
            y='event',  # Event names on the y-axis
            # Color by the opposite of what we selected (show venue if filtering by discipline)
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
        
        # Show note if we're limiting results
        if len(schedule_filtered) > 50:
            st.info(f"📊 Showing 50 of {len(schedule_filtered)} events. Use filters to narrow down the view.")
    else:
        # st.warning() displays an orange warning box
        st.warning("No valid date information available for the selected filter.")
else:
    # Fallback when detailed timing data isn't available
    st.info("Detailed timeline data not available. Showing event distribution instead.")
    
    # Simple bar chart counting events
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

# =============================================================================
# SECTION 2: MEDAL COUNT BY SPORT (TREEMAP)
# =============================================================================
st.header("🎯 Medal Count by Sport")
st.markdown("Hierarchical view of medals distributed across different sports")

# Get detailed medals data
medals_detail = data['medals'].copy()

# Apply all user filters
if filters['countries']:
    medals_detail = medals_detail[medals_detail['country_code'].isin(filters['countries'])]

if filters['sports']:
    medals_detail = medals_detail[medals_detail['discipline'].isin(filters['sports'])]

if filters['medal_types']:
    medals_detail = medals_detail[medals_detail['medal_type'].isin(filters['medal_types'])]

# Add continent information
medals_detail = medals_detail.merge(
    data['nocs'][['code', 'continent']],
    left_on='country_code',
    right_on='code',
    how='left'
)

if filters['continents']:
    medals_detail = medals_detail[medals_detail['continent'].isin(filters['continents'])]

# Count medals by sport and medal type
sport_medals = medals_detail.groupby(['discipline', 'medal_type']).size().reset_index(name='count')

# Also get total medals per sport for the treemap
sport_totals = sport_medals.groupby('discipline')['count'].sum().reset_index(name='total')

# px.treemap() creates a rectangular hierarchical visualization
# Each rectangle's size represents its value - great for showing proportions
fig_treemap = px.treemap(
    sport_totals,
    path=['discipline'],  # The hierarchy (just one level here)
    values='total',  # Size of each rectangle
    title='Medal Distribution Across Sports',
    color='total',  # Color by the total value
    color_continuous_scale='Viridis',  # Color gradient
    labels={'total': 'Total Medals'}
)

# Update visual appearance of the treemap
fig_treemap.update_traces(
    textposition='middle center',  # Center the text in each rectangle
    textfont_size=12
)

fig_treemap.update_layout(height=500)
st.plotly_chart(fig_treemap, use_container_width=True)

# st.expander() creates a collapsible section - saves space on the page
# Users can click to expand and see more details
with st.expander("📊 View Detailed Sport-wise Medal Breakdown"):
    # Create a pivot table showing medal breakdown by type for each sport
    sport_breakdown = medals_detail.groupby(['discipline', 'medal_type']).size().reset_index(name='count')
    
    # .pivot() transforms from long to wide format
    # This creates columns for each medal type
    sport_breakdown_pivot = sport_breakdown.pivot(index='discipline', columns='medal_type', values='count').fillna(0)
    
    # Add a total column
    sport_breakdown_pivot['Total'] = sport_breakdown_pivot.sum(axis=1)
    
    # Sort by total descending
    sport_breakdown_pivot = sport_breakdown_pivot.sort_values('Total', ascending=False)
    
    # Display as an interactive table
    st.dataframe(sport_breakdown_pivot, use_container_width=True)

st.markdown("---")

# =============================================================================
# SECTION 3: OLYMPIC VENUES MAP
# =============================================================================
st.header("🗼 Olympic Venues in Paris")
st.markdown("Explore the locations of Olympic venues across the Paris region")

# Get venues data
venues_df = data['venues'].copy()

# Check if we have geographic coordinates
if 'lat' in venues_df.columns and 'lon' in venues_df.columns:
    # Remove venues without coordinates
    venues_df = venues_df.dropna(subset=['lat', 'lon'])
    
    if len(venues_df) > 0:
        # px.scatter_mapbox() creates an interactive map with markers
        # This is great for showing point locations on a geographic map
        fig_map = px.scatter_mapbox(
            venues_df,
            lat='lat',  # Latitude column
            lon='lon',  # Longitude column
            hover_name='venue',  # Main text when hovering
            hover_data={  # Additional hover info
                'lat': False,  # Hide raw lat/lon in tooltip
                'lon': False,
                'venue': True
            },
            color_discrete_sequence=['#FF6B6B'],  # Marker color
            zoom=10,  # Initial zoom level (higher = more zoomed in)
            height=600,
            title='Olympic Venues Map'
        )
        
        # Configure the map style
        fig_map.update_layout(
            mapbox_style='open-street-map',  # Use OpenStreetMap tiles (free, no API key needed)
            margin={"r": 0, "t": 40, "l": 0, "b": 0}  # Reduce margins around the map
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
        
        # Show venue statistics
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Venues", len(venues_df))
        
        with col2:
            # Find the venue that hosted the most events
            venue_events = schedule_df.groupby('venue').size().reset_index(name='event_count')
            if len(venue_events) > 0:
                busiest_venue = venue_events.nlargest(1, 'event_count')
                venue_name = busiest_venue.iloc[0]['venue']
                # Truncate long names
                display_name = venue_name[:30] + "..." if len(venue_name) > 30 else venue_name
                st.metric(
                    "Busiest Venue",
                    display_name,
                    f"{int(busiest_venue.iloc[0]['event_count'])} events"
                )
    else:
        st.warning("No coordinate data available for venues.")
        st.info("Showing venue list instead:")
        st.dataframe(venues_df[['venue']].drop_duplicates(), use_container_width=True)
else:
    # Fallback when we don't have lat/lon data
    st.info("Geographic coordinates not available. Showing venue information:")
    
    # Show venues with their event counts
    venue_events = schedule_df.groupby('venue').size().reset_index(name='event_count').sort_values('event_count', ascending=False)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # st.dataframe() with height parameter limits how tall the table is
        st.dataframe(venue_events, use_container_width=True, height=400)
    
    with col2:
        # Pie chart showing distribution of events across top venues
        fig_venues = px.pie(
            venue_events.head(10),
            values='event_count',
            names='venue',
            title='Top 10 Venues by Event Count'
        )
        st.plotly_chart(fig_venues, use_container_width=True)

st.markdown("---")

# =============================================================================
# ADDITIONAL INSIGHTS
# =============================================================================
st.subheader("📊 Sports & Events Insights")

col1, col2, col3 = st.columns(3)

with col1:
    # Count unique disciplines in the schedule
    total_sports = schedule_df['discipline'].nunique()
    st.metric("Total Disciplines", total_sports)

with col2:
    # Total number of events
    total_events = len(schedule_df)
    st.metric("Total Events", f"{total_events:,}")

with col3:
    # Find the sport with the most medals awarded
    if len(sport_totals) > 0:
        top_sport = sport_totals.nlargest(1, 'total')
        sport_name = top_sport.iloc[0]['discipline']
        # Truncate long sport names
        display_name = sport_name[:25] + "..." if len(sport_name) > 25 else sport_name
        st.metric(
            "Most Medals Awarded",
            display_name,
            f"{int(top_sport.iloc[0]['total'])} medals"
        )

# =============================================================================
# SPORT-BY-SPORT MEDAL COMPARISON
# =============================================================================
st.markdown("---")
st.subheader("⚔️ Sport-by-Sport Medal Comparison")

# Stacked bar chart showing medal breakdown by sport
fig_sport_compare = px.bar(
    sport_medals,
    x='discipline',  # Sports on x-axis
    y='count',  # Medal counts on y-axis
    color='medal_type',  # Stack by medal type
    barmode='stack',  # Stack the bars on top of each other
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
    xaxis={'categoryorder': 'total descending'},  # Order by total medals
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig_sport_compare, use_container_width=True)
