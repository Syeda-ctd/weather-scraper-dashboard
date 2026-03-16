import sqlite3
import os

def run_query():
    db_path = 'weather_history.db'
    
    if not os.path.exists(db_path):
        print("Error: Database not found. Run db_import.py first.")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # This query JOINS the 'locations' table with the 'weather_stats' table
        # This is a specific requirement in your Lesson 14 rubric.
        query = """
        SELECT l.loc_id, l.City, s.Temperature_F, s.Condition
        FROM locations l
        JOIN weather_stats s ON l.City = s.City
        WHERE s.Temperature_F > 70
        ORDER BY s.Temperature_F DESC
        LIMIT 10;
        """

        print("\n" + "="*60)
        print("SQL QUERY RESULT: Top 10 Warmest Cities (Using JOIN)")
        print("="*60)
        
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                print(f"ID: {row[0]:<3} | City: {row[1]:<20} | Temp: {row[2]}°F | Status: {row[3]}")
        else:
            print("No records found matching the criteria.")

        print("="*60 + "\n")
        conn.close()
        
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    run_query()