# 🏅 Paris 2024 Olympic Games Dashboard

A comprehensive, interactive Streamlit dashboard analyzing the Paris 2024 Olympic Summer Games data. Built for the LA28 Volunteer Selection Challenge.

## 📋 Project Overview

This multi-page Streamlit application provides deep insights into the Paris 2024 Olympics through interactive visualizations and advanced analytics. The dashboard features:

- **🏠 Overview Page**: High-level KPIs and medal standings
- **🗺️ Global Analysis**: Geographic and continental medal distributions
- **👤 Athlete Performance**: Athlete demographics and top performers
- **🏟️ Sports & Events**: Event schedules, venues, and sport-specific analysis

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download this repository**

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure the dataset is in the correct location**

   The application expects the Paris 2024 Olympic dataset to be in:

   ```
   paris-2024-olympic-summer-games/versions/27/
   ```

   If you don't have the dataset, download it from:
   [https://www.kaggle.com/datasets/piterfm/paris-2024-olympic-summer-games](https://www.kaggle.com/datasets/piterfm/paris-2024-olympic-summer-games)

### Running the Application

Run the following command from the project directory:

```bash
streamlit run 1_🏠_Overview.py
```

The dashboard will open automatically in your default web browser at `http://localhost:8501`

## 📁 Project Structure

```
TEST_SEDS/
├── 1_🏠_Overview.py                    # Main landing page
├── pages/
│   ├── 2_🗺️_Global_Analysis.py         # Global/geographical analysis
│   ├── 3_👤_Athlete_Performance.py     # Athlete-focused analysis
│   └── 4_🏟️_Sports_and_Events.py      # Sports and venues analysis
├── utils/
│   ├── __init__.py
│   ├── data_loader.py                 # Data loading & caching utilities
│   └── filters.py                     # Global filter components
├── paris-2024-olympic-summer-games/   # Dataset directory
├── requirements.txt                    # Python dependencies
└── README.md                          # This file
```

## ✨ Key Features

### Global Filters (Available on All Pages)

- **🌍 Country Filter**: Filter by specific countries/NOCs
- **🗺️ Continent Filter**: Group analysis by continent (creative feature!)
- **⚽ Sport Filter**: Focus on specific sports
- **🏅 Medal Type Filter**: Gold, Silver, Bronze selection

### Page-by-Page Features

#### 1. 🏠 Overview

- 5 KPI metrics (Athletes, Countries, Sports, Medals, Events)
- Global medal distribution (Pie/Donut chart)
- Top 10 countries medal standings (Bar chart)

#### 2. 🗺️ Global Analysis

- **World choropleth map** showing medal counts by country
- **Sunburst & Treemap** hierarchical views (Continent → Country → Sport)
- **Continent comparison** bar charts
- **Top 20 countries** detailed medal breakdown

#### 3. 👤 Athlete Performance

- **Athlete profile card** with searchable athlete database
- **Age distribution** analysis (Box & Violin plots)
- **Gender distribution** across continents and countries
- **Top 10 athletes** by medal count

#### 4. 🏟️ Sports & Events

- **Event schedule** Gantt/Timeline chart
- **Medal distribution** by sport (Treemap)
- **Venue locations** on interactive map
- Sport-by-sport medal comparisons

## 🎨 Design Choices

### Technology Stack

- **Streamlit**: Chosen for rapid development and built-in interactivity
- **Plotly**: Interactive visualizations with hover tooltips and drill-down capabilities
- **Pandas**: Efficient data manipulation and analysis

### Data Processing

- **Caching**: Extensive use of `@st.cache_data` for optimal performance
- **Continent Mapping**: Custom mapping of NOC codes to continents (not in original dataset)
- **Data Merging**: Strategic joins across multiple CSV files for comprehensive analysis

### UX Considerations

- **Consistent Layout**: All pages follow the same filter sidebar pattern
- **Responsive Design**: Works across different screen sizes
- **Color Coding**: Consistent medal colors (Gold: #FFD700, Silver: #C0C0C0, Bronze: #CD7F32)
- **Interactive Elements**: Hover tooltips, drill-down charts, and dynamic updates

## 📊 Dataset Information

The dashboard uses the following data files:

- `athletes.csv` - Athlete demographics
- `coaches.csv` - Coach information
- `events.csv` - Event details
- `medals.csv` - Individual medal records
- `medals_total.csv` - Medal counts by country
- `medalists.csv` - Medalist information
- `nocs.csv` - Country/NOC codes
- `schedule.csv` - Event schedules
- `teams.csv` - Team information
- `venues.csv` - Venue details

## 🎯 Meeting Competition Requirements

This dashboard fulfills all mandatory requirements:

✅ Multi-page structure with main entry point and dedicated pages  
✅ Global filters on every page (Country, Sport, Medal Type, + Continent)  
✅ All required visualizations implemented  
✅ Cohesive layout using Streamlit columns and containers  
✅ Dynamic interactivity with filter-responsive charts  
✅ Professional design and user experience

## 👥 Team Information

This project was created as part of the SEDS Streamlit Challenge for the LA28 Volunteer Selection process.

**Team Members**

- Khedim Youcef
- Bensetallah Soufiane
- Zitouni Ahmed
- Houari Mohamed
  **group** 1
  **sepciality** AIDS
  **Course**: Software Engineering for Data Science  
  **Instructor**: Dr. Belkacem KHALDI

## 🔧 Troubleshooting

**Issue**: "No module named 'streamlit'"  
**Solution**: Make sure you've installed dependencies: `pip install -r requirements.txt`

**Issue**: "Dataset files not found"  
**Solution**: Verify the dataset is in `paris-2024-olympic-summer-games/versions/27/`

**Issue**: Page not loading or showing errors  
**Solution**: Check the terminal for error messages and ensure all CSV files are present

## 📝 License

This project is created for educational purposes as part of a university coursework assignment.

## 🙏 Acknowledgments

- Dataset provided by: [piterfm on Kaggle](https://www.kaggle.com/datasets/piterfm/paris-2024-olympic-summer-games)
- Built with: Streamlit, Plotly, and Pandas
- Created for: LA28 Volunteer Selection Challenge

---

**Happy Exploring! 🏅**
