#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import time


# In[3]:


# ---------------- CONFIG ----------------
API_KEY = "6c14be38b7mshd6fac41b5e4a4b3p1c79e8jsnc5a429d7846a" # Replace with your RapidAPI key
BASE_URL = "https://car-api2.p.rapidapi.com/api"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "car-api2.p.rapidapi.com"
}


# In[4]:


# Replace with your actual PostgreSQL credentials
username = "postgres"
password = "12345678"
host = "localhost"
port = "5432"
database = "Vehicle"


# In[5]:


# PostgreSQL connection string
# Correct connection string with your variables
POSTGRES_URI = f"postgresql://{username}:{password}@{host}:{port}/{database}"

TABLE_NAME = "vehicle_specs"


# In[6]:


import psycopg2


# In[7]:


try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(POSTGRES_URI)
    cur = conn.cursor()
    
    # Test query
    cur.execute("SELECT version();")
    db_version = cur.fetchone()
    
    print("✅ Connection successful!")
    print("PostgreSQL version:", db_version[0])
    
    cur.close()
    conn.close()

except Exception as e:
    print("❌ Connection failed!")
    print("Error:", e)


# In[8]:


# ---------------- EXTRACT ----------------
def get_years():
    res = requests.get(f"{BASE_URL}/years", headers=HEADERS)
    data = res.json()
    
    if isinstance(data, dict) and 'data' in data:
        return [y['year'] if isinstance(y, dict) else y for y in data['data']]
    elif isinstance(data, list):
        return [y if isinstance(y, int) else y.get('year') for y in data]
    else:
        print("⚠ Unexpected years format:", data)
        return []

def get_makes(year):
    res = requests.get(f"{BASE_URL}/makes", headers=HEADERS, params={"year": year})
    data = res.json()
    if isinstance(data, dict) and 'data' in data:
        return data['data']
    elif isinstance(data, list):
        return data
    else:
        print(f"⚠ No makes found for year {year}: {data}")
        return []

def get_models(year, make_id):
    res = requests.get(f"{BASE_URL}/models", headers=HEADERS, params={"year": year, "make_id": make_id})
    data = res.json()
    if isinstance(data, dict) and 'data' in data:
        return data['data']
    elif isinstance(data, list):
        return data
    else:
        print(f"⚠ No models found for {year}, make {make_id}: {data}")
        return []

def get_trims(year, make_id, model_id):
    res = requests.get(f"{BASE_URL}/trims", headers=HEADERS, params={"year": year, "make_id": make_id, "model_id": model_id})
    data = res.json()
    if isinstance(data, dict) and 'data' in data:
        return data['data']
    elif isinstance(data, list):
        return data
    else:
        print(f"⚠ No trims found for {year}, make {make_id}, model {model_id}: {data}")
        return []
    
def extract_data(limit_years=1):  
    all_data = []
    years = get_years()[:limit_years]  # Only first year

    for year in years:
        makes = get_makes(year)[:2]  # Only first 2 makes
        for make in makes:
            make_id = make['id']
            models = get_models(year, make_id)[:2]  # Only first 2 models
            for model in models:
                model_id = model['id']
                trims = get_trims(year, make_id, model_id)[:2]  # Only first 2 trims
                for trim in trims:
                    row = {
                        "year": year,
                        "make": make['name'],
                        "model": model['name'],
                        "trim": trim.get('name'),
                        "body": trim.get('body'),
                        "engine": trim.get('engine'),
                        "fuel_type": trim.get('fuel_type'),
                        "transmission": trim.get('transmission'),
                        "msrp": trim.get('msrp')
                    }
                    all_data.append(row)
                time.sleep(0.2)  # shorter delay for testing
    return all_data


# In[9]:



# ---------------- TRANSFORM ----------------
def transform_data(raw_data):
    df = pd.DataFrame(raw_data)
    df.dropna(how="all", inplace=True)  
    df.columns = df.columns.str.lower().str.replace(" ", "_")  
    df['make'] = df['make'].str.title()
    df['model'] = df['model'].str.title()
    if 'msrp' in df.columns:
        df['msrp'] = pd.to_numeric(df['msrp'], errors='coerce')
    return df

# ---------------- LOAD ----------------
def load_to_postgres(df):
    engine = create_engine(POSTGRES_URI)
    df.to_sql(TABLE_NAME, engine, if_exists='replace', index=False)
    print(f"✅ Data loaded to PostgreSQL table '{TABLE_NAME}' ({len(df)} rows)")


# In[10]:


# Quick test request
test_url = f"{BASE_URL}/years"
test_res = requests.get(test_url, headers=HEADERS)
print("Test API Status:", test_res.status_code)
print("Test API Response:", test_res.text)


# In[11]:


# ---------------- MAIN ----------------
if __name__ == "__main__":
    print("📥 Extracting data from API...")
    raw_data = extract_data(limit_years=1)  # First 1 years for testing
    print(f"Extracted {len(raw_data)} records.")

    print("🛠 Transforming data...")
    df_clean = transform_data(raw_data)
    print(df_clean.head())

    print("💾 Loading to PostgreSQL...")
    load_to_postgres(df_clean)

    print("🎯 ETL Pipeline completed successfully!")


# In[12]:


import pandas as pd
from sqlalchemy import create_engine

POSTGRES_URI = f"postgresql://{username}:{password}@{host}:{port}/{database}"

engine = create_engine(POSTGRES_URI)

df_check = pd.read_sql("SELECT * FROM vehicle_specs LIMIT 10", engine)
print(df_check)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




