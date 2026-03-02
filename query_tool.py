import sqlite3

def run_query_tool():
    db_path = "weather_history.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("\n--- 🔍 Weather Database Query Tool ---")
        print("This tool uses a SQL JOIN to combine Location URLs with Weather Stats.")
        
        while True:
            print("\nOptions:")
            print("1. View all cities (JOINed data)")
            print("2. Search for a specific city")
            print("3. Filter by 'Hot' cities (> 25°C)")
            print("4. Exit")
            
            choice = input("\nSelect an option (1-4): ")

            if choice == '1':
                # Aggressive JOIN using TRIM and LOWER to force a match
                query = """
                SELECT l.City, s.Temperature_C, s.Condition, l.Link
                FROM locations l
                JOIN weather_stats s ON LOWER(TRIM(l.City)) = LOWER(TRIM(s.City))
                """
                cursor.execute(query)
            
            elif choice == '2':
                city_name = input("Enter city name: ").strip().lower()
                query = """
                SELECT l.City, s.Temperature_C, s.Condition, l.Link
                FROM locations l
                JOIN weather_stats s ON LOWER(TRIM(l.City)) = LOWER(TRIM(s.City))
                WHERE LOWER(l.City) LIKE ?
                """
                cursor.execute(query, (f'%{city_name}%',))

            elif choice == '3':
                query = """
                SELECT l.City, s.Temperature_C, s.Condition, l.Link
                FROM locations l
                JOIN weather_stats s ON LOWER(TRIM(l.City)) = LOWER(TRIM(s.City))
                WHERE s.Temperature_C > 25
                ORDER BY s.Temperature_C DESC
                """
                cursor.execute(query)

            elif choice == '4':
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")
                continue

            results = cursor.fetchall()
            if results:
                print(f"\n{'City':<20} | {'Temp (°C)':<10} | {'Condition':<15} | {'URL'}")
                print("-" * 80)
                for row in results:
                    print(f"{row[0]:<20} | {row[1]:<10} | {row[2]:<15} | {row[3]}")
            else:
                # Debugging info if no results found
                print("\n⚠️ No results found.")
                print("Checking database status...")
                cursor.execute("SELECT COUNT(*) FROM locations")
                loc_count = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM weather_stats")
                stat_count = cursor.fetchone()[0]
                print(f"Total in 'locations' table: {loc_count}")
                print(f"Total in 'weather_stats' table: {stat_count}")
                print("Hint: If both tables have data but Choice 1 fails, the City names don't match exactly.")

    except sqlite3.Error as e:
        print(f"❌ SQLite error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    run_query_tool()