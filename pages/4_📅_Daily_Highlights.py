import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_all_data
from utils.venue_coordinates import get_venue_coordinates

st.set_page_config(page_title="Daily Highlights", page_icon="📅", layout="wide")

st.title("📅 Who Won the Day?")
st.markdown("Explore the events and medal winners for each day of the Paris 2024 Olympics.")

# Load data
data = load_all_data()
schedule = data['schedule']
medals = data['medals']

# Convert dates to datetime objects for sorting and formatting
schedule['day'] = pd.to_datetime(schedule['day'])
medals['medal_date'] = pd.to_datetime(medals['medal_date'])

# Get unique dates
available_dates = sorted(schedule['day'].unique())
formatted_dates = [d.strftime('%Y-%m-%d') for d in available_dates]

# Date Selector
selected_date_str = st.select_slider(
    "Select a Date",
    options=formatted_dates,
    value=formatted_dates[0] if formatted_dates else None
)

if selected_date_str:
    selected_date = pd.to_datetime(selected_date_str)
    
    # Filter Data
    daily_schedule = schedule[schedule['day'] == selected_date]
    daily_medals = medals[medals['medal_date'] == selected_date]
    
    # --- Summary Metrics ---
    st.subheader(f"Highlights for {selected_date.strftime('%B %d, %Y')}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Events", len(daily_schedule))
        
    with col2:
        medal_events = daily_schedule[daily_schedule['event_medal'] == 1]
        st.metric("Medal Events", len(medal_events))
        
    with col3:
        st.metric("Medals Awarded", len(daily_medals))

    # --- Top Countries of the Day ---
    st.subheader("🏆 Top Countries of the Day")
    
    if not daily_medals.empty:
        daily_country_counts = daily_medals['country'].value_counts().reset_index()
        daily_country_counts.columns = ['Country', 'Medals']
        
        fig_daily_top = px.bar(daily_country_counts.head(10), x='Medals', y='Country', orientation='h',
                               title="Top 10 Countries by Medals Won Today",
                               color='Medals', color_continuous_scale='Viridis')
        fig_daily_top.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_daily_top, use_container_width=True)
    else:
        st.info("No medals recorded for this date yet.")

    # --- Medal Winners ---
    st.subheader("🥇 Medal Winners")
    
    if not daily_medals.empty:
        # Show a table of winners
        display_medals = daily_medals[['medal_type', 'name', 'country', 'discipline', 'event']].copy()
        
        # Sort by medal type (Gold, Silver, Bronze)
        medal_order = {'Gold Medal': 1, 'Silver Medal': 2, 'Bronze Medal': 3}
        display_medals['order'] = display_medals['medal_type'].map(medal_order)
        display_medals = display_medals.sort_values('order').drop('order', axis=1)
        
        st.dataframe(display_medals, use_container_width=True, hide_index=True)
    else:
        st.info("No medal winners data available for this date.")

# ... (existing imports)

# ... (existing code)

    # --- Events Schedule ---
    st.subheader("📅 Events Schedule")
    
    # Filter for interesting columns
    display_schedule = daily_schedule[['start_date', 'discipline', 'event', 'status', 'venue']].copy()
    
    # Format start time
    display_schedule['start_date'] = pd.to_datetime(display_schedule['start_date']).dt.strftime('%H:%M')
    display_schedule.rename(columns={'start_date': 'Time'}, inplace=True)
    
    # Option to filter for only medal events
    show_only_medal_events = st.checkbox("Show only Medal Events", value=False)
    
    if show_only_medal_events:
        display_schedule = display_schedule[daily_schedule['event_medal'] == 1]
    
    st.dataframe(display_schedule.sort_values('Time'), use_container_width=True, hide_index=True)

    # --- Event Map ---
    st.subheader("📍 Event Locations")
    
    # Prepare map data
    map_data = []
    for index, row in daily_schedule.iterrows():
        venue = row['venue']
        coords = get_venue_coordinates(venue)
        if coords:
            map_data.append({
                'lat': coords[0],
                'lon': coords[1],
                'venue': venue,
                'discipline': row['discipline'],
                'event': row['event']
            })
            
    if map_data:
        map_df = pd.DataFrame(map_data)
        
        # Aggregate events per venue for cleaner map
        venue_stats = map_df.groupby(['venue', 'lat', 'lon']).size().reset_index(name='event_count')
        
        fig_map = px.scatter_mapbox(
            venue_stats,
            lat='lat',
            lon='lon',
            hover_name='venue',
            hover_data={'event_count': True, 'lat': False, 'lon': False},
            size='event_count',
            color_discrete_sequence=['#FF4B4B'],
            zoom=10,
            height=500
        )
        fig_map.update_layout(mapbox_style="open-street-map")
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("No location data available for events on this day.")

else:
    st.error("No dates available in the schedule data.")
