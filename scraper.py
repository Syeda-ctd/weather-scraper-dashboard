import pandas as pd
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def scrape_weather():
    print("🚀 Starting the Scraper...")
    if not os.path.exists('data'): os.makedirs('data')

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    # This ignores those "SSL Handshake" errors in your console
    options.add_argument("--log-level=3") 
    options.add_argument("--ignore-certificate-errors")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.timeanddate.com/weather/")
        time.sleep(5) 

        weather_list = []
        rows = driver.find_elements(By.XPATH, "//table[contains(@class, 'zebra')]//tr")

        for row in rows:
            try:
                city_el = row.find_element(By.TAG_NAME, "a")
                city_name = city_el.text
                city_url = city_el.get_attribute("href")
                
                cells = row.find_elements(By.TAG_NAME, "td")
                
                # Logic: Iterate through cells to find the one with the temperature
                temp_val = None
                condition_val = "N/A"
                
                for i, cell in enumerate(cells):
                    text = cell.text
                    if "°" in text: # This is the temperature cell
                        temp_val = text.split("°")[0].replace("−", "-").strip()
                        # Usually, the very next cell is the Condition
                        if i + 1 < len(cells):
                            condition_val = cells[i+1].text
                        break
                
                if city_name and temp_val:
                    weather_list.append({
                        "City": city_name,
                        "Temperature_C": temp_val,
                        "Condition": condition_val,
                        "Link": city_url
                    })
            except:
                continue

        if weather_list:
            df = pd.DataFrame(weather_list).drop_duplicates(subset=['City'])
            df.to_csv("data/raw_weather.csv", index=False)
            print(f"✅ SUCCESS! Scraped {len(df)} cities with ACTUAL temperatures.")
            print(df.head())
        else:
            print("❌ No data found. Check if the table loaded correctly.")

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_weather()