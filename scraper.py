import pandas as pd
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def scrape_weather():
    print("Initializing Selenium (Scroll-to-Table Mode)...")
    if not os.path.exists('data'): os.makedirs('data')

    options = webdriver.ChromeOptions()
    options.add_argument('--window-size=1920,1080')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.timeanddate.com/weather/")
        
        print("Scrolling down to find the table...")
        time.sleep(5)
        
        # We search for the blue header seen in your screenshot to scroll to it
        try:
            header = driver.find_element(By.XPATH, "//*[contains(text(), 'Local Time and Weather Around the World')]")
            driver.execute_script("arguments[0].scrollIntoView();", header)
            print("Header found. Waiting for table to render...")
        except:
            # Fallback: Scroll down by 1000 pixels if header text isn't found
            driver.execute_script("window.scrollBy(0, 1000);")
            print("Header not found by text, using manual scroll...")
            
        time.sleep(5) # Wait for table to load after scrolling

        weather_list = []
        
        # Now we find the table by tag name to be safe
        tables = driver.find_elements(By.TAG_NAME, "table")
        
        target_table = None
        for t in tables:
            # The correct table is the one that contains 'zebra' in its class
            if "zebra" in t.get_attribute("class"):
                target_table = t
                break

        if target_table:
            rows = target_table.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                # Capture both headers (th) and data (td)
                cells = row.find_elements(By.CSS_SELECTOR, "td, th")
                
                row_cities = []
                row_temps = []

                for cell in cells:
                    text = cell.text.strip().replace('*', '')
                    if "°" in text:
                        row_temps.append(text)
                    elif text and not any(char.isdigit() for char in text) and len(text) > 2:
                        # Filter out common UI words
                        if text not in ["City", "Time", "Weather", "Expected"]:
                            row_cities.append(text)

                for i in range(min(len(row_cities), len(row_temps))):
                    weather_list.append({
                        "City": row_cities[i],
                        "Temp_Raw": row_temps[i],
                        "Condition": "Maintained"
                    })

        if weather_list:
            df = pd.DataFrame(weather_list).drop_duplicates(subset=['City'])
            df.to_csv("data/raw_weather.csv", index=False)
            print(f"SUCCESS! Extracted {len(df)} cities.")
            print(df.head(10))
        else:
            print("Extraction failed. The table did not load after scrolling.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_weather()