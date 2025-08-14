# vehicle-etl-pipeline

Vehicle Data ETL Pipeline
An ETL (Extract, Transform, Load) pipeline that fetches real-time vehicle data from the Car API via RapidAPI, transforms it into a clean tabular format, and loads it into a PostgreSQL database for analysis and dashboard creation.
Table of Contents

1. Overview
2. Features
3. Architecture
4. Tech Stack
5. Installation
6. Configuration
7. How It Works
8. Sample Output
9. Future Improvements
10. License

Overview
ETL stands for Extract, Transform, Load. In this project:
- Extract: Vehicle years, makes, models, and trims are fetched from Car API.
- Transform: Data is cleaned using Pandas (formatted names, numeric conversions).
- Load: Final dataset is inserted into a PostgreSQL table.
Features

- Fetches real-time vehicle specs from API
- Cleans and standardizes data
- Stores structured data in PostgreSQL
- Easily configurable for more years/makes
- Scalable for dashboards (Power BI, Tableau, etc.)

Architecture

Car API -> Extract -> Transform -> Load -> PostgreSQL

Tech Stack

- Language: Python 3.x
- Libraries: Pandas, Requests, SQLAlchemy
- Database: PostgreSQL
- API Provider: RapidAPI (Car API)
- Tools: pgAdmin, GitHub

Installation

1. Clone the Repository:
   git clone https://github.com/yourusername/vehicle-etl-pipeline.git
   cd vehicle-etl-pipeline

2. Install Dependencies:
   pip install -r requirements.txt

3. Set Up PostgreSQL:
   - Create a database (e.g., vehicle_db)
   - Note your PostgreSQL username & password

4. Get API Key:
   - Sign up on RapidAPI
   - Subscribe to Car API
   - Copy your API key

Configuration

Update these variables in etl_pipeline.py:

API_KEY = "YOUR_RAPIDAPI_KEY"
POSTGRES_URI = "postgresql://username:password@localhost:5432/vehicle_db"
TABLE_NAME = "vehicle_specs"

How It Works

1. Extract: extract_data() calls the Car API for years, makes, models, and trims.
2. Transform: transform_data() cleans the data (e.g., title-case names, numeric MSRP).
3. Load: load_to_postgres() writes data into PostgreSQL.
4. Output: Data is ready for analysis or dashboard building.

Sample Output

Example DataFrame before loading to DB:

year | make  | model                         | trim   | body | engine | fuel_type | transmission | msrp
-----|-------|--------------------------------|--------|------|--------|-----------|--------------|-------
2026 | Acura | *** (Subscription Required)   | Premium| None | None   | None      | None         | 51800
2026 | BMW   | *** (Subscription Required)   | Luxury | None | None   | None      | None         | 54000

Future Improvements

- Automate pipeline using Airflow
- Connect directly to Power BI/Tableau
- Expand to historical data for all available years
- Add error handling & logging

License
This project is licensed under the MIT License - for educational purposes only.
