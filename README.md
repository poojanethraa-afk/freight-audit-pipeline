# Freight Audit Pipeline

A simulated data flow between three logistics source systems, from a REST API through a Python pipeline into PostgreSQL, where SQL rules find invoicing errors. Built as a portfolio project to practice the tasks of a software or data consultant: interface, process flow, business logic and reporting.

> **All data is synthetic.** The carriers, routes and invoices are generated and fictional. The three source systems are simulated and do not belong to any real company.

## Architecture

```
3 CSV exports -> REST API (FastAPI) -> Pipeline (Python, pandas) -> PostgreSQL -> SQL audit rules
```

| Step | Component | What it does |
|---|---|---|
| 1 | Source data | 3 CSV exports: TMS, Tracking, Invoicing |
| 2 | REST API (`api/main.py`) | Serves each export as JSON: `/tms/shipments`, `/tracking/events`, `/invoicing/invoices` |
| 3 | Pipeline (`pipeline/pipeline.py`) | Fetches from the API, cleans the dates and loads the tables into PostgreSQL |
| 4 | Database | PostgreSQL tables `shipments`, `tracking`, `invoices` |
| 5 | SQL layer (`sql/`) | Audit rules and reports |

## The data

Synthetic logistics data for June to August 2026: 6 carriers and 12 routes across Germany, Austria, the Netherlands and Italy.

| Source system | Content | Rows |
|---|---|---|
| TMS (transport management) | Orders, routes, pallets, weight, planned vs. actual transit time, status, carrier | 400 shipments |
| Tracking | GPS events with truck, fill rate, CO2 per trip, planned vs. driven km | 1,152 events on 275 trips |
| Invoicing | Base price, fuel surcharge, extras and the agreed contract rates per invoice, linked to TMS by `shipment_id` | 413 invoices |

### Injected errors and answer key

107 of the 413 invoices (26%) contain deliberately injected deviations that the SQL rules have to find. The file [data/answer_key_injected_errors.csv](data/answer_key_injected_errors.csv) lists the true error type for every invoice, so the results can be checked against a known answer.

| Error type in the answer key | Invoices |
|---|---|
| rate_above_contract | 21 |
| billed_cancelled_shipment | 16 |
| pallets_overbilled | 16 |
| unagreed_extra_charge | 16 |
| wrong_fuel_surcharge | 15 |
| small_deviation_within_tolerance | 10 |
| duplicate_invoice | 8 |
| unknown_shipment | 5 |
| none | 306 |

## SQL queries

| File | Question |
|---|---|
| [sql/duplicate_invoices.sql](sql/duplicate_invoices.sql) | How many invoices are duplicates (the same shipment billed again)? Only the later invoice counts. |
| [sql/detours.sql](sql/detours.sql) | How many trips drove more than 10% further than planned? |
| [sql/fill_rate_per_carrier.sql](sql/fill_rate_per_carrier.sql) | Average truck fill rate per carrier, worst first, counting each trip once. |

The queries use CTEs, window functions (`ROW_NUMBER`) and `DISTINCT` to avoid double counting.

## Run it

```bash
pip install -r requirements.txt

# 1. start the API (from the repository root)
uvicorn api.main:app --port 8000

# 2. in a second terminal: run the pipeline (needs PostgreSQL on port 5433, database "freight_audit")
export PGPASSWORD=your_password      # Windows PowerShell: $env:PGPASSWORD="your_password"
python pipeline/pipeline.py
```

The database password is read from the environment variable `PGPASSWORD` and is never stored in the code. After the pipeline has run, execute the queries in `sql/` against the `freight_audit` database.

## Documentation

- [docs/Freight_Audit_Pipeline_EN.pptx](docs/Freight_Audit_Pipeline_EN.pptx): overview slides (English)
- [docs/Freight_Audit_Pipeline_DE.pptx](docs/Freight_Audit_Pipeline_DE.pptx): overview slides (German)

## Tech stack

Python, pandas, FastAPI, requests, SQLAlchemy, PostgreSQL, SQL
