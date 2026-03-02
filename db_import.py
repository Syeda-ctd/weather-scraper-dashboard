import pandas as pd
import sqlite3
import os
import re

def import_to_db():
    csv_path = "data/raw_weather.csv"
    db_path = "weather_history.db"
    
    if not os.path.exists(csv_path):
        print(f"❌ Error: {csv_path} not found.")
        return

    df = pd.read_csv(csv_path)

    # --- THE "SUPER CLEANER" ---
    def clean_string(text):
        if pd.isna(text): return None
        # Remove non-ASCII characters, newlines, and extra spaces
        text = re.sub(r'[^\x00-\x7F]+', '', str(text)) 
        return text.strip()

    print("🧹 Deep cleaning city names...")
    df['City'] = df['City'].apply(clean_string)
    
    # Convert Temperature and drop rows that aren't numbers
    df['Temperature_C'] = pd.to_numeric(df['Temperature_C'], errors='coerce')
    
    # Drop rows with missing crucial data
    df = df.dropna(subset=['Temperature_C', 'City'])
    df = df.drop_duplicates(subset=['City'])

    # DEBUG: Print exactly what is going into the DB
    print("\n📊 DATABASE PREVIEW (Top 3):")
    print(df[['City', 'Temperature_C']].head(3))

    conn = sqlite3.connect(db_path)
    
    # Re-create tables
    df[['City', 'Link']].to_sql("locations", conn, if_exists="replace", index=False)
    df[['City', 'Temperature_C', 'Condition']].to_sql("weather_stats", conn, if_exists="replace", index=False)

    conn.close()
    print(f"\n✅ Database rebuilt with {len(df)} matching records.")

if __name__ == "__main__":
    import_to_db()