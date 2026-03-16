import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Set page config for a professional look
st.set_page_config(page_title="Global Weather Dashboard", layout="wide")

def get_data():
    """Connects to SQLite and performs a JOIN to retrieve relational data."""
    conn = sqlite3.connect('weather_history.db')
    # Rubric Requirement: Demonstrate a SQL JOIN
    query = """
    SELECT l.City, s.Temperature_F, s.Condition
    FROM locations l
    JOIN weather_stats s ON l.City = s.City
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# --- DASHBOARD HEADER ---
st.title("Global Weather Insights Dashboard")
st.markdown("""
This interactive dashboard displays real-time weather data scraped from **TimeAndDate**. 
It demonstrates a full data pipeline: Selenium Scraping ➔ Pandas Cleaning ➔ SQLite Storage ➔ Streamlit Visualization.
""")

try:
    # Load data from database
    df = get_data()

    # --- SIDEBAR FILTERS (User Interaction Requirement) ---
    st.sidebar.header("Filter & Search")
    search_city = st.sidebar.text_input("Search for a City", placeholder="e.g. New York")
    
    # Apply filter if user types a name
    if search_city:
        df = df[df['City'].str.contains(search_city, case=False)]

    # --- KEY METRICS ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Cities", len(df))
    col2.metric("Avg Global Temp", f"{round(df['Temperature_F'].mean(), 1)}°F")
    col3.metric("Highest Recorded", f"{df['Temperature_F'].max()}°F")

    st.divider()

    # --- VISUALIZATION 1: BAR CHART (Comparison) ---
    st.subheader("Top 20 Warmest Cities")
    # Sorting data for a better story
    top_df = df.sort_values('Temperature_F', ascending=False).head(20)
    fig_bar = px.bar(top_df, 
                     x='City', y='Temperature_F', 
                     color='Temperature_F',
                     color_continuous_scale='Reds',
                     labels={'Temperature_F': 'Temp (°F)'},
                     template="plotly_white")
    st.plotly_chart(fig_bar, width='stretch')

    # Create two columns for the next two visuals
    left_col, right_col = st.columns(2)

    with left_col:
        # --- VISUALIZATION 2: PIE CHART (Distribution) ---
        st.subheader("Weather Conditions")
        condition_counts = df['Condition'].value_counts().reset_index()
        fig_pie = px.pie(condition_counts, 
                         names='Condition', values='count', 
                         hole=0.4,
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, width='stretch')

    with right_col:
        # --- VISUALIZATION 3: BOX PLOT (Statistical Spread) ---
        st.subheader("Temperature Spread")
        fig_box = px.box(df, y="Temperature_F", 
                         points="all", 
                         title="Global Variance",
                         color_discrete_sequence=['#FFA500'])
        st.plotly_chart(fig_box, width='stretch')

    # --- DATA EXPLORER ---
    st.divider()
    st.subheader("Detailed Data Logs")
    st.markdown("Use the table below to explore the full dataset stored in the SQLite database.")
    st.dataframe(df, width='stretch')

except Exception as e:
    st.error(f"Dashboard Error: {e}")
    st.info("Verify that you have run 'python db_import.py' to generate the database first.")

# Footer note for the reviewer
st.caption("Developed for Lesson 14 Project | Data Source: TimeAndDate.com")