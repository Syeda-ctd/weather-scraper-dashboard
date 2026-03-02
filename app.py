import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os

st.set_page_config(page_title="Global Weather Dashboard", layout="wide")

# --- DATA LOADING ---
def get_data():
    db_path = "weather_history.db"
    if not os.path.exists(db_path):
        return pd.DataFrame(), "Database file missing!"
    
    conn = sqlite3.connect(db_path)
    
    # 1. Check if tables have data individually
    loc_count = pd.read_sql("SELECT COUNT(*) as count FROM locations", conn).iloc[0]['count']
    stat_count = pd.read_sql("SELECT COUNT(*) as count FROM weather_stats", conn).iloc[0]['count']
    
    if loc_count == 0 or stat_count == 0:
        conn.close()
        return pd.DataFrame(), f"Tables exist but are empty (Locations: {loc_count}, Stats: {stat_count})"

    # 2. Try the JOIN
    query = """
    SELECT l.City, s.Temperature_C, s.Condition, l.Link
    FROM locations l
    JOIN weather_stats s ON LOWER(TRIM(l.City)) = LOWER(TRIM(s.City))
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df, None

# --- UI LOGIC ---
st.title(" Global Weather Dashboard")

df, error_msg = get_data()

if not df.empty:
    # Sidebar Filters
    st.sidebar.header("Filters")
    selected_condition = st.sidebar.multiselect("Conditions:", df['Condition'].unique(), default=df['Condition'].unique())
    
    # Filter data
    filtered_df = df[df['Condition'].isin(selected_condition)]

    # Viz 1: Bar Chart
    fig1 = px.bar(filtered_df, x='City', y='Temperature_C', color='Temperature_C', title="City vs Temp")
    st.plotly_chart(fig1, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        # Viz 2: Pie Chart
        fig2 = px.pie(filtered_df, names='Condition', title="Weather Mix")
        st.plotly_chart(fig2, use_container_width=True)
    with col2:
        # Viz 3: Histogram
        fig3 = px.histogram(filtered_df, x='Temperature_C', title="Temp Distribution")
        st.plotly_chart(fig3, use_container_width=True)

    st.write("### Raw Database (Joined)", filtered_df)
else:
    st.error(f" No data to display: {error_msg}")
    st.info("Try running 'python db_import.py' again to refresh the database.")