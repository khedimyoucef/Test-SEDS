# =============================================================================
# ATHLETE PERFORMANCE PAGE
# =============================================================================
# This page provides a deep dive into athlete data including:
# - Individual athlete profile cards with detailed information
# - Age distribution analysis with box and violin plots
# - Gender distribution comparisons across different dimensions
# - Top medalists display with stacked bar chart
# This is a comprehensive athlete analytics page.
# =============================================================================

import streamlit as st  # Main framework for building the web interface
import plotly.express as px  # High-level charting library for common chart types
import plotly.graph_objects as go  # Lower-level Plotly for custom chart configurations
import pandas as pd  # Data manipulation library for DataFrames
import sys
import os
from datetime import datetime  # For date calculations (athlete ages)

#testing push

# Add parent directory to path for imports
# This allows us to import our utility modules from the utils folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_loader import load_all_data
from utils.filters import create_sidebar_filters, get_filter_summary
from utils.country_flags import get_flag_html  # For displaying country flags as images

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
# Configure the browser tab and layout for this page
st.set_page_config(
    page_title="Athlete Performance - Paris 2024",
    page_icon="👤",
    layout="wide"
)

# =============================================================================
# DATA LOADING WITH CACHING
# =============================================================================
# @st.cache_data decorator caches the function result
# This means the CSV files are only read once, even if the page reruns
# This is critical for performance - without caching, data would reload on every interaction
@st.cache_data
def get_data():
    return load_all_data()

data = get_data()

# Create sidebar filters and get the user's selections
filters = create_sidebar_filters(data)

# =============================================================================
# PAGE HEADER
# =============================================================================
st.title("👤 Athlete Performance Analysis")
st.markdown("Deep dive into athlete demographics, performance, and achievements")

# Display the current filter status in an info box
st.info(f"📊 {get_filter_summary(filters)}")
st.markdown("---")

# =============================================================================
# SECTION 1: ATHLETE PROFILE VIEWER
# =============================================================================
st.header("🔍 Athlete Profile Viewer")
st.markdown("Search and explore detailed information about individual athletes")

# Make a copy of the athletes data to avoid modifying the original cached data
athletes_df = data['athletes'].copy()

# Merge athletes with NOCs to get country names and continent information
# This join adds 'country' and 'continent' columns to each athlete row
athletes_df = athletes_df.merge(
    data['nocs'][['code', 'country', 'continent']],  # Select only the columns we need
    left_on='country_code',  # Match on country_code in athletes
    right_on='code',  # Match on code in nocs
    how='left',  # Keep all athletes even if no NOC match found
    suffixes=('_src', '')  # Avoid column name conflicts
)

# Create a sorted list of unique athlete names for the search dropdown
# .dropna() removes any missing names, .tolist() converts to a Python list
athlete_names = sorted(athletes_df['name'].dropna().unique().tolist())

# st.selectbox() creates a searchable dropdown
# Users can type to filter the options - great for long lists
selected_athlete = st.selectbox(
    "Search for an athlete by name:",  # Label above the dropdown
    options=athlete_names,  # The list of selectable options
    index=0 if len(athlete_names) > 0 else None,  # Default to first athlete
    help="Type to search for an athlete"  # Tooltip text
)

# Only show profile if an athlete is selected
if selected_athlete:
    # Get the row for the selected athlete
    # .iloc[0] gets the first row (there should only be one match)
    athlete_info = athletes_df[athletes_df['name'] == selected_athlete].iloc[0]
    
    # =============================================================================
    # ATHLETE PROFILE CARD
    # =============================================================================
    # Create 4 columns with relative widths specified as a list
    # [1, 2, 2, 2] means the first column is half the width of the others
    col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
    
    with col1:
        # Placeholder for athlete photo - using an emoji icon instead
        st.markdown("### 📸")
        # .get() safely retrieves a value, returning 'N/A' if the key doesn't exist
        st.markdown(f"**{athlete_info.get('gender', 'N/A')}**")
        
    with col2:
        # Get the flag image HTML for this athlete's country
        athlete_flag = get_flag_html(athlete_info.get('country_code', ''), 20)
        
        # Display the athlete name as a heading
        st.markdown(f"### {athlete_info['name']}")
        # Use HTML to render the flag image alongside country info
        st.markdown(
            f"**Country:** {athlete_flag} {athlete_info.get('country', 'N/A')} ({athlete_info.get('country_code', 'N/A')})",
            unsafe_allow_html=True
        )
        st.markdown(f"**Continent:** {athlete_info.get('continent', 'N/A')}")
        
    with col3:
        st.markdown("### Physical Stats")
        # Get height and weight, handling missing values
        height = athlete_info.get('height', 'N/A')
        weight = athlete_info.get('weight', 'N/A')
        # pd.notna() checks if the value is not NaN (Not a Number / missing)
        st.markdown(f"**Height:** {height if pd.notna(height) else 'N/A'}")
        st.markdown(f"**Weight:** {weight if pd.notna(weight) else 'N/A'}")
        
    with col4:
        st.markdown("### Competition Info")
        
        # The disciplines and events columns are stored as string representations of lists
        # We need to parse them back into actual Python lists
        disciplines_str = str(athlete_info.get('disciplines', ''))
        events_str = str(athlete_info.get('events', ''))
        
        # Use ast.literal_eval to safely convert string to Python object
        import ast
        try:
            # ast.literal_eval safely parses a string as a Python literal (list, dict, etc.)
            disciplines = ast.literal_eval(disciplines_str) if disciplines_str and disciplines_str != 'nan' else []
            events_list = ast.literal_eval(events_str) if events_str and events_str != 'nan' else []
        except:
            # Fallback if eval fails - manually parse the string
            disciplines = [d.strip(" []'\"") for d in disciplines_str.split(',')] if disciplines_str and disciplines_str != 'nan' else []
            events_list = [e.strip(" []'\"") for e in events_str.split(',')] if events_str and events_str != 'nan' else []

        # Display disciplines and events
        st.markdown(f"**Disciplines:** {', '.join(disciplines)}")
        
        st.markdown(f"**Events ({len(events_list)}):**")
        if len(events_list) > 0:
            # Show up to 5 events to avoid cluttering the display
            for event in events_list[:5]:
                st.markdown(f"- {event}")
            if len(events_list) > 5:
                # Indicate there are more events not shown
                st.markdown(f"*...and {len(events_list)-5} more*")

    # =============================================================================
    # COACH INFORMATION SECTION
    # =============================================================================
    coach_info = athlete_info.get('coach', '')
    # Check if coach info exists and is not empty
    if pd.notna(coach_info) and coach_info:
        st.markdown("### 🧢 Coaching Staff")
        # Handle different possible formats for coach data
        # Some datasets use <br> tags or newlines to separate multiple coaches
        coaches = str(coach_info).replace('<br>', '\n').split('\n')
        
        for coach in coaches:
            coach = coach.strip()  # Remove whitespace
            if coach:
                st.markdown(f"- {coach}")
    
    st.markdown("---")

# =============================================================================
# SECTION 2: ATHLETE AGE DISTRIBUTION
# =============================================================================
st.header("📊 Athlete Age Distribution")
st.markdown("Analyze age patterns across sports and genders")

# Make a copy for analysis to avoid modifying the merged DataFrame
athletes_analysis = athletes_df.copy()

# Apply filters based on user selections
if filters['countries']:
    athletes_analysis = athletes_analysis[athletes_analysis['country_code'].isin(filters['countries'])]

if filters['continents']:
    athletes_analysis = athletes_analysis[athletes_analysis['continent'].isin(filters['continents'])]

# st.radio() creates a horizontal list of mutually exclusive options
# horizontal=True places them in a row instead of a column
age_view = st.radio("View age distribution by:", ["Sport", "Gender"], horizontal=True)

# Calculate ages from birth dates if available
if 'birth_date' in athletes_analysis.columns:
    # pd.to_datetime() converts strings to datetime objects
    # errors='coerce' turns unparseable dates into NaT (Not a Time) instead of raising an error
    athletes_analysis['birth_date'] = pd.to_datetime(athletes_analysis['birth_date'], errors='coerce')
    
    # Calculate age as current year minus birth year
    # .dt.year extracts just the year from a datetime
    athletes_analysis['age'] = 2024 - athletes_analysis['birth_date'].dt.year
    
    # Filter out missing ages and implausible values
    athletes_analysis = athletes_analysis[athletes_analysis['age'].notna()]
    athletes_analysis = athletes_analysis[(athletes_analysis['age'] >= 10) & (athletes_analysis['age'] <= 80)]
    
    # Prepare data for sport view if sports filter is active
    athletes_with_sport = None
    if age_view == "Sport" and filters['sports']:
        # Parse the disciplines column which contains list strings
        import ast
        def parse_disciplines(x):
            """Convert string representation of list to actual list"""
            try:
                return ast.literal_eval(x) if pd.notna(x) else []
            except:
                return [d.strip(" []'\"") for d in str(x).split(',')] if pd.notna(x) else []

        # Create a copy and add parsed disciplines
        athletes_exploded = athletes_analysis.copy()
        athletes_exploded['sport_list'] = athletes_exploded['disciplines'].apply(parse_disciplines)
        
        # "Explode" the list column so each sport gets its own row
        # If an athlete participates in 3 sports, they now have 3 rows
        athletes_with_sport = athletes_exploded.explode('sport_list')
        athletes_with_sport = athletes_with_sport.rename(columns={'sport_list': 'sport'})
        
        # Filter to only the sports the user selected
        athletes_with_sport = athletes_with_sport[athletes_with_sport['sport'].isin(filters['sports'])]

    # Create two columns for side-by-side charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Box plot shows distribution with quartiles, median, and outliers
        if age_view == "Sport" and filters['sports'] and athletes_with_sport is not None:
            # px.box() creates a box plot (also called box-and-whisker plot)
            fig_box = px.box(
                athletes_with_sport,
                x='sport',  # Categories on x-axis
                y='age',  # Numerical values on y-axis
                color='sport',  # Color boxes by sport
                title='Age Distribution by Sport (Box Plot)',
                labels={'age': 'Age (years)', 'sport': 'Sport'}
            )
        elif age_view == "Gender":
            fig_box = px.box(
                athletes_analysis,
                x='gender',
                y='age',
                color='gender',
                title='Age Distribution by Gender (Box Plot)',
                labels={'age': 'Age (years)', 'gender': 'Gender'}
            )
        else:
            # No grouping - just overall distribution
            fig_box = px.box(
                athletes_analysis,
                y='age',
                title='Overall Age Distribution (Box Plot)',
                labels={'age': 'Age (years)'}
            )
        
        fig_box.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)
    
    with col2:
        # Violin plot shows the full distribution shape (like a sideways histogram)
        if age_view == "Sport" and filters['sports'] and athletes_with_sport is not None:
            # px.violin() creates a violin plot
            # box=True adds a mini box plot inside the violin
            fig_violin = px.violin(
                athletes_with_sport,
                x='sport',
                y='age',
                color='sport',
                box=True,  # Show box plot inside the violin
                title='Age Distribution by Sport (Violin Plot)',
                labels={'age': 'Age (years)', 'sport': 'Sport'}
            )
        elif age_view == "Gender":
            fig_violin = px.violin(
                athletes_analysis,
                x='gender',
                y='age',
                color='gender',
                box=True,
                title='Age Distribution by Gender (Violin Plot)',
                labels={'age': 'Age (years)', 'gender': 'Gender'}
            )
        else:
            fig_violin = px.violin(
                athletes_analysis,
                y='age',
                box=True,
                title='Overall Age Distribution (Violin Plot)',
                labels={'age': 'Age (years)'}
            )
        
        fig_violin.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_violin, use_container_width=True)

st.markdown("---")

# =============================================================================
# SECTION 3: GENDER DISTRIBUTION ANALYSIS
# =============================================================================
st.header("⚖️ Gender Distribution Analysis")
st.markdown("Explore gender balance across continents and countries")

# st.selectbox() creates a dropdown for selecting the view type
gender_view = st.selectbox(
    "View gender distribution for:",
    ["World", "By Continent", "By Country (Top 20)"]
)

# Group athletes by gender and count them
gender_data = athletes_analysis.groupby('gender').size().reset_index(name='count')

if gender_view == "World":
    # Pie chart for global gender distribution
    fig_gender = px.pie(
        gender_data,
        values='count',  # Size of each slice
        names='gender',  # Labels for each slice
        title='Global Gender Distribution of Athletes',
        color='gender',
        # Handle both 'Male'/'Female' and 'M'/'F' labels
        color_discrete_map={'Male': '#4A90E2', 'Female': '#E24A90', 'M': '#4A90E2', 'F': '#E24A90'}
    )
    # Update traces to show percentages inside the pie
    fig_gender.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_gender, use_container_width=True)

elif gender_view == "By Continent":
    # Group by both continent and gender
    gender_continent = athletes_analysis.groupby(['continent', 'gender']).size().reset_index(name='count')
    
    # Grouped bar chart showing gender split per continent
    fig_gender = px.bar(
        gender_continent,
        x='continent',
        y='count',
        color='gender',
        barmode='group',  # Side-by-side bars
        title='Gender Distribution by Continent',
        labels={'count': 'Number of Athletes', 'continent': 'Continent'},
        color_discrete_map={'Male': '#4A90E2', 'Female': '#E24A90', 'M': '#4A90E2', 'F': '#E24A90'}
    )
    st.plotly_chart(fig_gender, use_container_width=True)

else:  # By Country (Top 20)
    # Group by country and gender
    gender_country = athletes_analysis.groupby(['country', 'gender']).size().reset_index(name='count')
    
    # Find the top 20 countries by total athlete count
    top_countries = gender_country.groupby('country')['count'].sum().nlargest(20).index
    
    # Filter to only include top 20 countries
    gender_country = gender_country[gender_country['country'].isin(top_countries)]
    
    fig_gender = px.bar(
        gender_country,
        x='country',
        y='count',
        color='gender',
        barmode='group',
        title='Gender Distribution by Country (Top 20)',
        labels={'count': 'Number of Athletes', 'country': 'Country'},
        color_discrete_map={'Male': '#4A90E2', 'Female': '#E24A90', 'M': '#4A90E2', 'F': '#E24A90'}
    )
    fig_gender.update_layout(height=500)
    st.plotly_chart(fig_gender, use_container_width=True)

st.markdown("---")

# =============================================================================
# SECTION 4: TOP ATHLETES BY MEDAL COUNT
# =============================================================================
st.header("🏅 Top Athletes by Medal Count")
st.markdown("The most decorated athletes of Paris 2024")

# Get the medalists data (athletes who won medals)
medalists_df = data['medalists'].copy()

# Count total medals per athlete
# .groupby('name').size() counts how many rows (medals) each athlete has
athlete_medals = medalists_df.groupby('name').size().reset_index(name='medal_count')

# Get top 10 athletes by medal count
top_athletes = athlete_medals.nlargest(10, 'medal_count')

# Get detailed medal breakdown (gold, silver, bronze) for top athletes
medal_breakdown = medalists_df[medalists_df['name'].isin(top_athletes['name'])].groupby(['name', 'medal_type']).size().reset_index(name='count')

# Pivot the data to have one column per medal type
# This transforms from long format (one row per athlete-medal combo) to wide format
medal_pivot = medal_breakdown.pivot(index='name', columns='medal_type', values='count').fillna(0)
medal_pivot = medal_pivot.reset_index()

# Add country code for each athlete (useful for display)
medal_pivot = medal_pivot.merge(
    medalists_df[['name', 'country_code']].drop_duplicates(),
    on='name',
    how='left'
)

# =============================================================================
# CREATE STACKED HORIZONTAL BAR CHART
# =============================================================================
# Using go.Figure() for more control over the stacked bar chart
fig_top_athletes = go.Figure()

# Add a trace (bar series) for each medal type if it exists in the data
if 'Gold Medal' in medal_pivot.columns:
    fig_top_athletes.add_trace(go.Bar(
        name='Gold',
        y=medal_pivot['name'],  # Athlete names on y-axis (horizontal bars)
        x=medal_pivot['Gold Medal'],  # Medal count on x-axis
        orientation='h',  # Horizontal bars
        marker=dict(color='#FFD700'),  # Gold color
    ))

if 'Silver Medal' in medal_pivot.columns:
    fig_top_athletes.add_trace(go.Bar(
        name='Silver',
        y=medal_pivot['name'],
        x=medal_pivot['Silver Medal'],
        orientation='h',
        marker=dict(color='#C0C0C0'),  # Silver color
    ))

if 'Bronze Medal' in medal_pivot.columns:
    fig_top_athletes.add_trace(go.Bar(
        name='Bronze',
        y=medal_pivot['name'],
        x=medal_pivot['Bronze Medal'],
        orientation='h',
        marker=dict(color='#CD7F32'),  # Bronze color
    ))

# Configure the layout for a stacked bar chart
fig_top_athletes.update_layout(
    barmode='stack',  # Stack the bars on top of each other
    title='Top 10 Athletes by Medal Count',
    xaxis_title='Number of Medals',
    yaxis_title='Athlete',
    height=500,
    showlegend=True,
    # Position the legend horizontally above the chart
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig_top_athletes, use_container_width=True)

# =============================================================================
# ADDITIONAL ATHLETE STATISTICS
# =============================================================================
st.markdown("---")
st.subheader("📈 Athlete Statistics")

# Create three columns for summary stats
col1, col2, col3 = st.columns(3)

with col1:
    # Calculate and display average age
    if len(athletes_analysis) > 0:
        avg_age = athletes_analysis['age'].mean() if 'age' in athletes_analysis.columns else 0
        st.metric("Average Age", f"{avg_age:.1f} years" if avg_age > 0 else "N/A")
 
with col2:
    # Count athletes by gender and show the ratio
    male_count = len(athletes_analysis[athletes_analysis['gender'].isin(['Male', 'M'])])
    female_count = len(athletes_analysis[athletes_analysis['gender'].isin(['Female', 'F'])])
    # Calculate female as percentage of male count
    ratio = (female_count / male_count * 100) if male_count > 0 else 0
    st.metric("Female Athletes", f"{female_count:,}", f"{ratio:.1f}% of male count")

with col3:
    # Show the most decorated athlete
    if len(top_athletes) > 0:
        most_medals = top_athletes.iloc[0]['medal_count']
        top_athlete_name = top_athletes.iloc[0]['name']
        # Truncate long names to fit nicely in the display
        display_name = top_athlete_name[:20] + "..." if len(top_athlete_name) > 20 else top_athlete_name
        st.metric("Most Decorated", display_name, f"{int(most_medals)} medals")
