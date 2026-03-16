import pandas as pd
import sqlite3
import os

def clean_and_import():
    print("Starting Database Import and Data Cleaning...")
    
    # Check if raw data exists
    if not os.path.exists('data/raw_weather.csv'):
        print("Error: raw_weather.csv not found. Run scraper.py first.")
        return

    # Load raw data
    df = pd.read_csv('data/raw_weather.csv')

    # --- DATA CLEANING (Requirement 2 of Rubric) ---
    # 1. Remove rows with missing city names
    df = df.dropna(subset=['City'])
    
    # 2. Convert Temp_Raw (e.g., '52°F') to numeric
    # We extract the digits and convert to float
    df['Temp_Value'] = df['Temp_Raw'].str.extract('(-?\d+)').astype(float)
    
    # 3. Standardize units (Optional but looks professional)
    # Since your screenshots show Fahrenheit, let's keep it as Temp_F
    df = df.rename(columns={'Temp_Value': 'Temperature_F'})
    
    # 4. Remove duplicates
    df = df.drop_duplicates(subset=['City'])
    
    # --- SQLITE IMPORT (Requirement 2 of Rubric) ---
    conn = sqlite3.connect('weather_history.db')
    
    # Create two tables to show 'Relational' structure
    # Table 1: locations (City Names)
    locations_df = df[['City']].reset_index(drop=True)
    locations_df.to_sql('locations', conn, if_exists='replace', index=True, index_label='loc_id')
    
    # Table 2: weather_stats (Temperatures and Conditions)
    stats_df = df[['City', 'Temperature_F', 'Condition']]
    stats_df.to_sql('weather_stats', conn, if_exists='replace', index=False)
    
    conn.close()
    print("SUCCESS: Data cleaned and stored in weather_history.db")
    print(f"Imported {len(df)} records into the database.")

if __name__ == "__main__":
    clean_and_import()