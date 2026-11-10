import pandas as pd
import requests
import os
from sqlalchemy import create_engine

API_URL= "http://localhost:8000"

DB_URL = f"postgresql://postgres:{os.environ['PGPASSWORD']}@localhost:5433/freight_audit"

def fetch(endpoint):
    response= requests.get(f"{API_URL}{endpoint}")
    response.raise_for_status()
    return pd.DataFrame(response.json())

def clean_data(df, columns):
    for col in columns:
        df[col]= pd.to_datetime(df[col])
    return df

def load(df, table_name, engine):
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"Loaded {len(df)} rows into {table_name}")

if __name__ == "__main__":
    shipments = fetch("/tms/shipments")
    tracking = fetch("/tracking/events")
    invoices = fetch("/invoicing/invoices")

    shipments= clean_data(shipments, ["pickup_date"])
    tracking= clean_data(tracking, ["event_timestamp", "tour_date"])
    invoices= clean_data(invoices, ["invoice_date"])

    engine= create_engine(DB_URL)
    load(shipments, "shipments", engine)
    load(tracking, "tracking", engine)
    load(invoices, "invoices", engine)

