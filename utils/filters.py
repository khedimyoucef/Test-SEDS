import streamlit as st

def create_sidebar_filters(data):
    """Create global filters in the sidebar"""
    st.sidebar.title("🔍 Global Filters")
    st.sidebar.markdown("---")
    
    filters = {}
    
    # Country filter
    st.sidebar.subheader("🌍 Country (NOC)")
    all_countries = sorted(data['nocs']['code'].unique().tolist())
    filters['countries'] = st.sidebar.multiselect(
        "Select Countries",
        options=all_countries,
        default=[],
        help="Filter by country/NOC code"
    )
    
    # Continent filter (Creativity Challenge!)
    st.sidebar.subheader("🗺️ Continent")
    all_continents = sorted(data['nocs']['continent'].unique().tolist())
    filters['continents'] = st.sidebar.multiselect(
        "Select Continents",
        options=all_continents,
        default=[],
        help="Filter by continent - a creative filter!"
    )
    
    # Sport filter
    st.sidebar.subheader("⚽ Sport")
    all_sports = sorted(data['events']['sport'].dropna().unique().tolist())
    filters['sports'] = st.sidebar.multiselect(
        "Select Sports",
        options=all_sports,
        default=[],
        help="Filter by sport"
    )
    
    # Medal type filter
    st.sidebar.subheader("🏅 Medal Type")
    medal_types = ['Gold Medal', 'Silver Medal', 'Bronze Medal']
    
    col1, col2, col3 = st.sidebar.columns(3)
    with col1:
        gold = st.checkbox("🥇", value=True, help="Gold")
    with col2:
        silver = st.checkbox("🥈", value=True, help="Silver")
    with col3:
        bronze = st.checkbox("🥉", value=True, help="Bronze")
    
    filters['medal_types'] = []
    if gold:
        filters['medal_types'].append('Gold Medal')
    if silver:
        filters['medal_types'].append('Silver Medal')
    if bronze:
        filters['medal_types'].append('Bronze Medal')
    
    st.sidebar.markdown("---")
    
    # Clear filters button
    if st.sidebar.button("🔄 Clear All Filters"):
        st.rerun()
    
    return filters

def get_filter_summary(filters):
    """Generate a summary text of active filters"""
    summaries = []
    
    if filters.get('countries'):
        summaries.append(f"{len(filters['countries'])} countries")
    
    if filters.get('continents'):
        summaries.append(f"{len(filters['continents'])} continents")
    
    if filters.get('sports'):
        summaries.append(f"{len(filters['sports'])} sports")
    
    if filters.get('medal_types') and len(filters['medal_types']) < 3:
        summaries.append(f"{len(filters['medal_types'])} medal types")
    
    if summaries:
        return "Active filters: " + ", ".join(summaries)
    else:
        return "No filters active (showing all data)"
