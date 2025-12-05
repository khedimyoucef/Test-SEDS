import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
import os
from datetime import datetime
#testing push
# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_loader import load_all_data
from utils.filters import create_sidebar_filters, get_filter_summary

# Page configuration
st.set_page_config(
    page_title="Athlete Performance - Paris 2024",
    page_icon="👤",
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
st.title("👤 Athlete Performance Analysis")
st.markdown("Deep dive into athlete demographics, performance, and achievements")
st.info(f"📊 {get_filter_summary(filters)}")
st.markdown("---")

# 1. Athlete Detailed Profile Card
st.header("🔍 Athlete Profile Viewer")
st.markdown("Search and explore detailed information about individual athletes")

# Prepare athletes data
athletes_df = data['athletes'].copy()

# Merge with NOCs to get country names
athletes_df = athletes_df.merge(
    data['nocs'][['code', 'country', 'continent']],
    left_on='country_code',
    right_on='code',
    how='left',
    suffixes=('_src', '')
)

# Create athlete search
athlete_names = sorted(athletes_df['name'].dropna().unique().tolist())
selected_athlete = st.selectbox(
    "Search for an athlete by name:",
    options=athlete_names,
    index=0 if len(athlete_names) > 0 else None,
    help="Type to search for an athlete"
)

if selected_athlete:
    athlete_info = athletes_df[athletes_df['name'] == selected_athlete].iloc[0]
    
    # Display athlete profile card
    col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
    
    with col1:
        # Placeholder for athlete image
        st.markdown("### 📸")
        st.markdown(f"**{athlete_info.get('gender', 'N/A')}**")
        
    with col2:
        st.markdown(f"### {athlete_info['name']}")
        st.markdown(f"**Country:** {athlete_info.get('country', 'N/A')} ({athlete_info.get('country_code', 'N/A')})")
        st.markdown(f"**Continent:** {athlete_info.get('continent', 'N/A')}")
        
    with col3:
        st.markdown("### Physical Stats")
        height = athlete_info.get('height', 'N/A')
        weight = athlete_info.get('weight', 'N/A')
        st.markdown(f"**Height:** {height if pd.notna(height) else 'N/A'}")
        st.markdown(f"**Weight:** {weight if pd.notna(weight) else 'N/A'}")
        
    with col4:
        st.markdown("### Competition Info")
        
        # Get disciplines and events directly from athlete info
        # The data comes as string representation of lists like "['Sport']", so we clean it
        disciplines_str = str(athlete_info.get('disciplines', ''))
        events_str = str(athlete_info.get('events', ''))
        
        # Clean up the string representation
        import ast
        try:
            disciplines = ast.literal_eval(disciplines_str) if disciplines_str and disciplines_str != 'nan' else []
            events_list = ast.literal_eval(events_str) if events_str and events_str != 'nan' else []
        except:
            # Fallback if eval fails
            disciplines = [d.strip(" []'\"") for d in disciplines_str.split(',')] if disciplines_str and disciplines_str != 'nan' else []
            events_list = [e.strip(" []'\"") for e in events_str.split(',')] if events_str and events_str != 'nan' else []

        st.markdown(f"**Disciplines:** {', '.join(disciplines)}")
        
        st.markdown(f"**Events ({len(events_list)}):**")
        if len(events_list) > 0:
            # Show up to 5 events
            for event in events_list[:5]:
                st.markdown(f"- {event}")
            if len(events_list) > 5:
                st.markdown(f"*...and {len(events_list)-5} more*")

    # Display Coach Information
    coach_info = athlete_info.get('coach', '')
    if pd.notna(coach_info) and coach_info:
        st.markdown("### 🧢 Coaching Staff")
        # Handle multiple coaches often separated by <br> or newlines in some datasets, 
        # though in this CSV it seems to be a single string or comma separated.
        # We'll split by <br> if present, otherwise treat as one block.
        coaches = str(coach_info).replace('<br>', '\n').split('\n')
        
        for coach in coaches:
            coach = coach.strip()
            if coach:
                st.markdown(f"- {coach}")
    
    st.markdown("---")

# 2. Athlete Age Distribution
st.header("📊 Athlete Age Distribution")
st.markdown("Analyze age patterns across sports and genders")

# Calculate ages (using birth_date if available)
athletes_analysis = athletes_df.copy()

# Apply filters
if filters['countries']:
    athletes_analysis = athletes_analysis[athletes_analysis['country_code'].isin(filters['countries'])]

if filters['continents']:
    athletes_analysis = athletes_analysis[athletes_analysis['continent'].isin(filters['continents'])]

# Age distribution plot options
age_view = st.radio("View age distribution by:", ["Sport", "Gender"], horizontal=True)

if 'birth_date' in athletes_analysis.columns:
    athletes_analysis['birth_date'] = pd.to_datetime(athletes_analysis['birth_date'], errors='coerce')
    athletes_analysis['age'] = 2024 - athletes_analysis['birth_date'].dt.year
    athletes_analysis = athletes_analysis[athletes_analysis['age'].notna()]
    athletes_analysis = athletes_analysis[(athletes_analysis['age'] >= 10) & (athletes_analysis['age'] <= 80)]
    
    # Prepare data for sport view if needed
    athletes_with_sport = None
    if age_view == "Sport" and filters['sports']:
        # Parse disciplines column which is a string representation of a list
        import ast
        def parse_disciplines(x):
            try:
                return ast.literal_eval(x) if pd.notna(x) else []
            except:
                return [d.strip(" []'\"") for d in str(x).split(',')] if pd.notna(x) else []

        # Create a copy to avoid SettingWithCopyWarning
        athletes_exploded = athletes_analysis.copy()
        athletes_exploded['sport_list'] = athletes_exploded['disciplines'].apply(parse_disciplines)
        
        # Explode to have one row per sport
        athletes_with_sport = athletes_exploded.explode('sport_list')
        athletes_with_sport = athletes_with_sport.rename(columns={'sport_list': 'sport'})
        
        # Filter for selected sports
        athletes_with_sport = athletes_with_sport[athletes_with_sport['sport'].isin(filters['sports'])]

    col1, col2 = st.columns(2)
    
    with col1:
        if age_view == "Sport" and filters['sports'] and athletes_with_sport is not None:
            
            fig_box = px.box(
                athletes_with_sport,
                x='sport',
                y='age',
                color='sport',
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
            fig_box = px.box(
                athletes_analysis,
                y='age',
                title='Overall Age Distribution (Box Plot)',
                labels={'age': 'Age (years)'}
            )
        
        fig_box.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)
    
    with col2:
        if age_view == "Sport" and filters['sports'] and athletes_with_sport is not None:
            fig_violin = px.violin(
                athletes_with_sport,
                x='sport',
                y='age',
                color='sport',
                box=True,
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

# 3. Gender Distribution
st.header("⚖️ Gender Distribution Analysis")
st.markdown("Explore gender balance across continents and countries")

# Gender distribution options
gender_view = st.selectbox(
    "View gender distribution for:",
    ["World", "By Continent", "By Country (Top 20)"]
)

gender_data = athletes_analysis.groupby('gender').size().reset_index(name='count')

if gender_view == "World":
    fig_gender = px.pie(
        gender_data,
        values='count',
        names='gender',
        title='Global Gender Distribution of Athletes',
        color='gender',
        color_discrete_map={'Male': '#4A90E2', 'Female': '#E24A90', 'M': '#4A90E2', 'F': '#E24A90'}
    )
    fig_gender.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_gender, use_container_width=True)

elif gender_view == "By Continent":
    gender_continent = athletes_analysis.groupby(['continent', 'gender']).size().reset_index(name='count')
    
    fig_gender = px.bar(
        gender_continent,
        x='continent',
        y='count',
        color='gender',
        barmode='group',
        title='Gender Distribution by Continent',
        labels={'count': 'Number of Athletes', 'continent': 'Continent'},
        color_discrete_map={'Male': '#4A90E2', 'Female': '#E24A90', 'M': '#4A90E2', 'F': '#E24A90'}
    )
    st.plotly_chart(fig_gender, use_container_width=True)

else:  # By Country
    gender_country = athletes_analysis.groupby(['country', 'gender']).size().reset_index(name='count')
    top_countries = gender_country.groupby('country')['count'].sum().nlargest(20).index
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

# 4. Top Athletes by Medals
st.header("🏅 Top Athletes by Medal Count")
st.markdown("The most decorated athletes of Paris 2024")

# Get medalists data
medalists_df = data['medalists'].copy()

# Count medals per athlete
athlete_medals = medalists_df.groupby('name').size().reset_index(name='medal_count')
top_athletes = athlete_medals.nlargest(10, 'medal_count')

# Get medal breakdown
medal_breakdown = medalists_df[medalists_df['name'].isin(top_athletes['name'])].groupby(['name', 'medal_type']).size().reset_index(name='count')

# Pivot for stacked bar
medal_pivot = medal_breakdown.pivot(index='name', columns='medal_type', values='count').fillna(0)
medal_pivot = medal_pivot.reset_index()

# Merge with country info
medal_pivot = medal_pivot.merge(
    medalists_df[['name', 'country_code']].drop_duplicates(),
    on='name',
    how='left'
)

# Create stacked bar chart
fig_top_athletes = go.Figure()

if 'Gold Medal' in medal_pivot.columns:
    fig_top_athletes.add_trace(go.Bar(
        name='Gold',
        y=medal_pivot['name'],
        x=medal_pivot['Gold Medal'],
        orientation='h',
        marker=dict(color='#FFD700'),
    ))

if 'Silver Medal' in medal_pivot.columns:
    fig_top_athletes.add_trace(go.Bar(
        name='Silver',
        y=medal_pivot['name'],
        x=medal_pivot['Silver Medal'],
        orientation='h',
        marker=dict(color='#C0C0C0'),
    ))

if 'Bronze Medal' in medal_pivot.columns:
    fig_top_athletes.add_trace(go.Bar(
        name='Bronze',
        y=medal_pivot['name'],
        x=medal_pivot['Bronze Medal'],
        orientation='h',
        marker=dict(color='#CD7F32'),
    ))

fig_top_athletes.update_layout(
    barmode='stack',
    title='Top 10 Athletes by Medal Count',
    xaxis_title='Number of Medals',
    yaxis_title='Athlete',
    height=500,
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig_top_athletes, use_container_width=True)

# Additional stats
st.markdown("---")
st.subheader("📈 Athlete Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    if len(athletes_analysis) > 0:
        avg_age = athletes_analysis['age'].mean() if 'age' in athletes_analysis.columns else 0
        st.metric("Average Age", f"{avg_age:.1f} years" if avg_age > 0 else "N/A")
 
with col2:
    male_count = len(athletes_analysis[athletes_analysis['gender'].isin(['Male', 'M'])])
    female_count = len(athletes_analysis[athletes_analysis['gender'].isin(['Female', 'F'])])
    ratio = (female_count / male_count * 100) if male_count > 0 else 0
    st.metric("Female Athletes", f"{female_count:,}", f"{ratio:.1f}% of male count")

with col3:
    if len(top_athletes) > 0:
        most_medals = top_athletes.iloc[0]['medal_count']
        top_athlete_name = top_athletes.iloc[0]['name']
        st.metric("Most Decorated", top_athlete_name[:20] + "..." if len(top_athlete_name) > 20 else top_athlete_name, 
                 f"{int(most_medals)} medals")
