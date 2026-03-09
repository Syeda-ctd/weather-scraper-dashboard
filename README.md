<<<<<<< HEAD
# 🌦️ Global Weather Data Pipeline & Dashboard

An end-to-end data engineering project that scrapes live weather data, stores it in a relational SQLite database, and provides an interactive dashboard for climate analysis.

## 🚀 Overview
This project demonstrates a full data lifecycle:
1. **Extraction:** Scraping live data using **Selenium**.
2. **Storage:** Organizing data into a relational **SQLite** database with normalized tables.
3. **Transformation:** Using **SQL JOINs** to merge location and weather metrics.
4. **Visualization:** An interactive **Streamlit** dashboard with real-time filters and **Plotly** charts.

## 🛠️ Technical Stack
- **Language:** Python 3.12
- **Libraries:** Selenium, Pandas, Streamlit, Plotly, SQLite3
- **Drivers:** Webdriver-manager (Chrome)

## 📊 Dashboard Functionality
- **City Temperature Comparison:** A dynamic bar chart showing current heat levels across regions.
- **Weather Condition Distribution:** A pie chart showing the global mix of sunny, cloudy, or rainy areas.
- **Relational Data View:** A live table showing the results of the SQL JOIN operation between the `locations` and `weather_stats` tables.

## 🏃 How to Run
1. Install dependencies:  
   `pip install selenium webdriver-manager pandas streamlit plotly`
2. Scrape live data:  
   `python scraper.py`
3. Populate the Database:  
   `python db_import.py`
4. Launch the Dashboard:  
   `python -m streamlit run app.py`
=======
# 🌦️ Global Weather Data Pipeline & Dashboard

An end-to-end data engineering project that scrapes live weather data, stores it in a relational SQLite database, and provides an interactive dashboard for climate analysis.
## 🚀 Overview
This project demonstrates a full data lifecycle:
1. **Extraction:** Scraping live data using **Selenium**.
2. **Storage:** Organizing data into a relational **SQLite** database with normalized tables.
3. **Transformation:** Using **SQL JOINs** to merge location and weather metrics.
4. **Visualization:** An interactive **Streamlit** dashboard with real-time filters and **Plotly** charts.

## 🛠️ Technical Stack
- **Language:** Python 3.12
- **Libraries:** Selenium, Pandas, Streamlit, Plotly, SQLite3
- **Drivers:** Webdriver-manager (Chrome)

## 📊 Dashboard Functionality
- **City Temperature Comparison:** A dynamic bar chart showing current heat levels across regions.
- **Weather Condition Distribution:** A pie chart showing the global mix of sunny, cloudy, or rainy areas.
- **Relational Data View:** A live table showing the results of the SQL JOIN operation between the `locations` and `weather_stats` tables.

## 🏃 How to Run
1. Install dependencies:  
   `pip install selenium webdriver-manager pandas streamlit plotly`
2. Scrape live data:  
   `python scraper.py`
3. Populate the Database:  
   `python db_import.py`
4. Launch the Dashboard:  
   `python -m streamlit run app.py`
>>>>>>> aac7070 (Small readme update for PR practice)
