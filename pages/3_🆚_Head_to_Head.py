import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_all_data

st.set_page_config(page_title="Head-to-Head Comparison", page_icon="🆚", layout="wide")

st.title("🆚 Head-to-Head Country Comparison")
st.markdown("Compare the performance of two countries side-by-side.")

# Load data
data = load_all_data()
medals_total = data['medals_total']
nocs = data['nocs']
athletes = data['athletes']
medals = data['medals']

# Helper to get country name
def get_country_name(code):
    row = nocs[nocs['code'] == code]
    if not row.empty:
        return row['note'].values[0] if pd.notna(row['note'].values[0]) else code
    return code

# Get list of countries with medals or athletes
available_countries = sorted(medals_total['country_code'].unique())

# Selectors
col1, col2 = st.columns(2)

with col1:
    country_a = st.selectbox("Select Country A", available_countries, index=0)

with col2:
    # Try to select a different default for Country B
    default_index_b = 1 if len(available_countries) > 1 else 0
    country_b = st.selectbox("Select Country B", available_countries, index=default_index_b)

if country_a == country_b:
    st.warning("Please select two different countries to compare.")
else:
    # --- Data Preparation ---
    
    # 1. Medals
    medals_a = medals_total[medals_total['country_code'] == country_a]
    medals_b = medals_total[medals_total['country_code'] == country_b]
    
    def get_medal_counts(df):
        if df.empty:
            return {'Gold': 0, 'Silver': 0, 'Bronze': 0, 'Total': 0}
        return {
            'Gold': df['Gold Medal'].values[0],
            'Silver': df['Silver Medal'].values[0],
            'Bronze': df['Bronze Medal'].values[0],
            'Total': df['Total'].values[0] if 'Total' in df.columns else df['Gold Medal'].values[0] + df['Silver Medal'].values[0] + df['Bronze Medal'].values[0]
        }

    counts_a = get_medal_counts(medals_a)
    counts_b = get_medal_counts(medals_b)
    
    # 2. Athletes
    # Assuming athletes dataframe has 'country_code' or similar. Let's check columns if needed, but standard is usually 'country_code' or 'NOC'
    # Based on previous files, it seems 'country_code' is standard in processed files, but let's be safe.
    # If 'country_code' not in athletes, we might need to map from NOC.
    # Let's assume 'country_code' exists as per other files, if not we will debug.
    
    num_athletes_a = len(athletes[athletes['country_code'] == country_a]) if 'country_code' in athletes.columns else 0
    num_athletes_b = len(athletes[athletes['country_code'] == country_b]) if 'country_code' in athletes.columns else 0
    
    # 3. Top Sports (by medal count)
    def get_top_sports(country_code):
        country_medals = medals[medals['country_code'] == country_code]
        if country_medals.empty:
            return pd.DataFrame()
        
        # Count medals by discipline
        sport_counts = country_medals['discipline'].value_counts().reset_index()
        sport_counts.columns = ['Discipline', 'Medals']
        return sport_counts.head(5)

    top_sports_a = get_top_sports(country_a)
    top_sports_b = get_top_sports(country_b)

    # --- Display ---
    
    # Metrics Row
    st.subheader("🏅 Overall Performance")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    
    with m_col1:
        st.metric(f"{country_a} Total Medals", counts_a['Total'])
        st.metric(f"{country_b} Total Medals", counts_b['Total'], delta=int(counts_b['Total'] - counts_a['Total']))
        
    with m_col2:
        st.metric(f"{country_a} Gold", counts_a['Gold'])
        st.metric(f"{country_b} Gold", counts_b['Gold'], delta=int(counts_b['Gold'] - counts_a['Gold']))
        
    with m_col3:
        st.metric(f"{country_a} Athletes", num_athletes_a)
        st.metric(f"{country_b} Athletes", num_athletes_b, delta=int(num_athletes_b - num_athletes_a))
        
    # Visual Comparison
    st.subheader("📊 Medal Breakdown")
    
    comparison_data = pd.DataFrame({
        'Country': [country_a, country_a, country_a, country_b, country_b, country_b],
        'Medal Type': ['Gold', 'Silver', 'Bronze', 'Gold', 'Silver', 'Bronze'],
        'Count': [counts_a['Gold'], counts_a['Silver'], counts_a['Bronze'], 
                  counts_b['Gold'], counts_b['Silver'], counts_b['Bronze']]
    })
    
    fig_medals = px.bar(comparison_data, x='Country', y='Count', color='Medal Type', 
                        barmode='group', title="Medal Count Comparison",
                        color_discrete_map={'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': '#CD7F32'})
    st.plotly_chart(fig_medals, use_container_width=True)
    
    # Top Sports Comparison
    st.subheader("🏆 Top Sports")
    s_col1, s_col2 = st.columns(2)
    
    with s_col1:
        st.markdown(f"**{country_a} Top Sports**")
        if not top_sports_a.empty:
            st.dataframe(top_sports_a, hide_index=True)
        else:
            st.write("No medals found.")
            
    with s_col2:
        st.markdown(f"**{country_b} Top Sports**")
        if not top_sports_b.empty:
            st.dataframe(top_sports_b, hide_index=True)
        else:
            st.write("No medals found.")
