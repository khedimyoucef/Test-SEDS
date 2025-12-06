# =============================================================================
# DAILY HIGHLIGHTS PAGE
# =============================================================================
# This page allows users to explore what happened on each day of the Olympics.
# Users can select a date using a slider and see:
# - Summary metrics for that day
# - Top countries by medals won that day
# - List of medal winners
# - Event schedule
# - Map showing where events took place
# This provides a day-by-day narrative of the Games.
# =============================================================================

import streamlit as st  # Main framework for building web apps
import plotly.express as px  # For creating interactive charts
import pandas as pd  # Data manipulation library
from utils.data_loader import load_all_data  # Our custom data loading function
from utils.venue_coordinates import get_venue_coordinates  # Get lat/lon for venues

# Configure the page - must be the first Streamlit command
st.set_page_config(
    page_title="Daily Highlights",
    page_icon="📅",
    layout="wide"
)

# Set the main page title and subtitle
st.title("📅 Who Won the Day?")
st.markdown("Explore the events and medal winners for each day of the Paris 2024 Olympics.")

# =============================================================================
# LOAD DATA
# =============================================================================
data = load_all_data()

# Extract the datasets we need for this page
schedule = data['schedule']  # Event schedule data
medals = data['medals']  # Detailed medal records

# =============================================================================
# PREPARE DATE DATA
# =============================================================================
# Convert the date columns from strings to datetime objects
# pd.to_datetime() handles various date formats automatically
schedule['day'] = pd.to_datetime(schedule['day'])
medals['medal_date'] = pd.to_datetime(medals['medal_date'])

# Get a sorted list of all unique dates in the schedule
available_dates = sorted(schedule['day'].unique())

# Convert dates to string format for the slider display
# strftime() formats the date as a string; '%Y-%m-%d' gives 'YYYY-MM-DD' format
formatted_dates = [d.strftime('%Y-%m-%d') for d in available_dates]

# =============================================================================
# DATE SELECTOR
# =============================================================================
# st.select_slider() creates a slider where users can select from discrete options
# Unlike st.slider() which works with ranges, select_slider uses a list of specific values
# This is perfect for dates since we only want dates that have data
selected_date_str = st.select_slider(
    "Select a Date",  # Label above the slider
    options=formatted_dates,  # The list of selectable options
    value=formatted_dates[0] if formatted_dates else None  # Default to first date
)

# Only proceed if a date was selected
if selected_date_str:
    # Convert the selected string back to a datetime for filtering
    selected_date = pd.to_datetime(selected_date_str)
    
    # =============================================================================
    # FILTER DATA FOR SELECTED DATE
    # =============================================================================
    # Filter schedule and medals to only show data for the selected day
    daily_schedule = schedule[schedule['day'] == selected_date]
    daily_medals = medals[medals['medal_date'] == selected_date]
    
    # =============================================================================
    # SUMMARY METRICS
    # =============================================================================
    # st.subheader() creates a medium-sized heading
    # strftime with '%B %d, %Y' formats as "Month Day, Year" (e.g., "July 26, 2024")
    st.subheader(f"Highlights for {selected_date.strftime('%B %d, %Y')}")
    
    # Create three columns for the summary metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # len() counts the number of events scheduled for this day
        st.metric("Total Events", len(daily_schedule))
        
    with col2:
        # Filter for "medal events" - events where medals are awarded
        # event_medal == 1 indicates a medal-awarding event
        medal_events = daily_schedule[daily_schedule['event_medal'] == 1]
        st.metric("Medal Events", len(medal_events))
        
    with col3:
        # Count actual medals awarded (not just medal events)
        st.metric("Medals Awarded", len(daily_medals))

    # =============================================================================
    # TOP COUNTRIES OF THE DAY
    # =============================================================================
    st.subheader("🏆 Top Countries of the Day")
    
    if not daily_medals.empty:
        # .value_counts() counts how many medals each country won
        # Returns a Series with country as index and count as values
        daily_country_counts = daily_medals['country'].value_counts().reset_index()
        # Rename the columns to be more descriptive
        daily_country_counts.columns = ['Country', 'Medals']
        
        # Create a horizontal bar chart of top medal-winning countries
        fig_daily_top = px.bar(
            daily_country_counts.head(10),  # Only show top 10
            x='Medals',  # Medals on x-axis (horizontal bars)
            y='Country',  # Countries on y-axis
            orientation='h',  # Horizontal orientation
            title="Top 10 Countries by Medals Won Today",
            color='Medals',  # Color bars by medal count
            color_continuous_scale='Viridis'  # Purple to yellow gradient
        )
        
        # Sort so highest is at the top
        fig_daily_top.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_daily_top, use_container_width=True)
    else:
        st.info("No medals recorded for this date yet.")

    # =============================================================================
    # MEDAL WINNERS TABLE
    # =============================================================================
    st.subheader("🥇 Medal Winners")
    
    if not daily_medals.empty:
        # Select only the columns we want to display
        display_medals = daily_medals[['medal_type', 'name', 'country', 'discipline', 'event']].copy()
        
        # Sort medals by type: Gold first, then Silver, then Bronze
        # We create a temporary 'order' column to sort by
        medal_order = {'Gold Medal': 1, 'Silver Medal': 2, 'Bronze Medal': 3}
        # .map() replaces each medal_type with its order number
        display_medals['order'] = display_medals['medal_type'].map(medal_order)
        # Sort by the order column, then remove it (we don't want to display it)
        display_medals = display_medals.sort_values('order').drop('order', axis=1)
        
        # st.dataframe() displays the DataFrame as an interactive table
        # use_container_width=True makes it fill the available width
        # hide_index=True removes the row numbers on the left
        st.dataframe(display_medals, use_container_width=True, hide_index=True)
    else:
        st.info("No medal winners data available for this date.")

# ... (existing imports)

# ... (existing code)

    # =============================================================================
    # EVENTS SCHEDULE TABLE
    # =============================================================================
    st.subheader("📅 Events Schedule")
    
    # Select and prepare the columns we want to show
    display_schedule = daily_schedule[['start_date', 'discipline', 'event', 'status', 'venue']].copy()
    
    # Format the start time to show just hours and minutes
    # .dt.strftime('%H:%M') formats as 24-hour time
    display_schedule['start_date'] = pd.to_datetime(display_schedule['start_date']).dt.strftime('%H:%M')
    # Rename the column to be clearer
    display_schedule.rename(columns={'start_date': 'Time'}, inplace=True)
    
    # st.checkbox() creates a toggle that returns True when checked
    # This allows users to filter to only see medal events
    show_only_medal_events = st.checkbox("Show only Medal Events", value=False)
    
    if show_only_medal_events:
        # Filter to only rows where event_medal is 1
        # Note: we need to use daily_schedule here, not display_schedule,
        # because display_schedule doesn't have the event_medal column
        display_schedule = display_schedule[daily_schedule['event_medal'] == 1]
    
    # Display the schedule table, sorted by time
    st.dataframe(display_schedule.sort_values('Time'), use_container_width=True, hide_index=True)

    # =============================================================================
    # EVENT LOCATIONS MAP
    # =============================================================================
    st.subheader("📍 Event Locations")
    
    # Build a list of venue locations with coordinates
    map_data = []
    
    # Iterate through each event in the daily schedule
    # iterrows() yields (index, row) pairs for each row in the DataFrame
    for index, row in daily_schedule.iterrows():
        venue = row['venue']
        # Look up the coordinates for this venue
        coords = get_venue_coordinates(venue)
        if coords:  # Only add venues we have coordinates for
            map_data.append({
                'lat': coords[0],
                'lon': coords[1],
                'venue': venue,
                'discipline': row['discipline'],
                'event': row['event']
            })
            
    if map_data:
        # Convert the list of dictionaries to a DataFrame
        map_df = pd.DataFrame(map_data)
        
        # Aggregate to count how many events at each venue
        # This prevents overlapping markers and shows venue busyness
        venue_stats = map_df.groupby(['venue', 'lat', 'lon']).size().reset_index(name='event_count')
        
        # Create an interactive map with markers
        fig_map = px.scatter_mapbox(
            venue_stats,
            lat='lat',  # Latitude column
            lon='lon',  # Longitude column
            hover_name='venue',  # Main text when hovering
            hover_data={  # Additional hover info
                'event_count': True,  # Show event count
                'lat': False,  # Hide coordinates
                'lon': False
            },
            size='event_count',  # Marker size based on event count
            color_discrete_sequence=['#FF4B4B'],  # Red markers
            zoom=10,  # Initial zoom level
            height=500
        )
        
        # Use OpenStreetMap tiles (free, no API key required)
        fig_map.update_layout(mapbox_style="open-street-map")
        # Remove excess margins
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("No location data available for events on this day.")

else:
    # This message appears if no dates are available in the data
    # st.error() displays a red error box
    st.error("No dates available in the schedule data.")
