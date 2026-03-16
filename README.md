Weather Pipeline & Interactive Dashboard
Project Description
This is a data engineering project built for Lesson 14. I created an end-to-end pipeline that scrapes live weather data from over 100 global cities. The project moves data from the web into a structured SQLite database and finally into an interactive dashboard for analysis.

The Environment (Setup)
To keep things clean, I recommend running this project in a virtual environment. This keeps the dependencies isolated from your main Python installation.

1. Create the environment:
python -m venv venv
2. Activate it:
Windows: .\venv\Scripts\activate
3. Install the tools:
pip install -r requirements.txt

How the Pipeline Works
You should run the scripts in the following order to build the data from scratch:

python scraper.py This starts the Selenium bot. I programmed it to handle the "lazy-loading" on the website by scrolling down automatically before it tries to grab the table data. It saves the raw data to a CSV.

python db_import.py This script handles the data cleaning. It uses Pandas to fix the temperature formatting and splits the data into two tables (locations and weather_stats) to ensure the database is relational.

python -m streamlit run app.py This launches the dashboard in your browser. It uses a SQL JOIN to pull data from both tables and visualizes the results.

Key Technical Features
Relational Database: The project uses SQLite. I've excluded the actual .db file from the repository (via .gitignore) because it is "derived data" that the scripts generate automatically.

Selenium Resilience: The scraper uses flexible selectors and headers to avoid being blocked or failing if the website layout shifts slightly.

Interactive Visuals: The dashboard includes a temperature bar chart, a weather condition pie chart, and a statistical box plot.