import pandas as pd
from pathlib import Path
from fastapi import FastAPI

app= FastAPI()
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def load_csv(filename):
    filename= DATA_DIR / filename
    df= pd.read_csv(filename)
    return df.astype(object).where(pd.notnull(df), None)

shipments = load_csv("tms_shipments.csv")
tracking = load_csv("tracking_events.csv")
invoices = load_csv("carrier_invoices.csv")


@app.get("/tms/shipments")
def get_shipments():
    return shipments.to_dict(orient="records")

@app.get("/tracking/events")
def get_tracking():
    return tracking.to_dict(orient="records")

@app.get("/invoicing/invoices")
def get_invoices():
    return invoices.to_dict(orient="records")


if __name__ == "__main__":
    print(len(shipments))
    print(len(tracking))
    print(len(invoices))