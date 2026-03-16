Weather Scraper & Dashboard
About this project:
I built a tool that automatically goes to a weather website, grabs the latest temperatures for over 100 cities, saves them into a database, and shows them on a digital dashboard.

How I built it
Scraping: I used Selenium to handle the website. It was tricky because the data doesn't load until you scroll down, so I programmed the script to scroll automatically.

Database: I used Pandas to clean up the data (removing extra symbols and fixing numbers) and stored it in SQLite. I used two tables and a SQL "JOIN" to make it a proper relational database.

Dashboard: I used Streamlit to make the charts. You can search for cities and see which ones are the warmest right now.

How to run it: Install everything:

pip install -r requirements.txt
Get the data:python scraper.py
Move data to the database: python db_import.py
Open the dashboard:python -m streamlit run app.py

Files in this project

scraper.py - The web bot.
db_import.py - The cleaner and database builder.
query_tool.py - A simple script to test the database.
app.py - The code for the visual dashboard.
weather_history.db - My SQLite database.