# Bluestock — Day 1 Data Ingestion

This project organizes and profiles the 10 provided mutual-fund CSV datasets, explores the fund master, validates AMFI codes against the supplied NAV-history file, and fetches live NAV history from MFAPI.

## Project structure

```text
Bluestock-Day1-Complete/
├── data/
│   ├── raw/          # 10 supplied CSVs + fetched raw API JSON/CSV
│   └── processed/    # AMFI code validation output
├── notebooks/
├── sql/
├── dashboard/
├── reports/
├── data_ingestion.py
├── live_nav_fetch.py
├── fund_master_explore.py
├── validate_data.py
└── requirements.txt
```

## Setup in VS Code (Windows PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the Day 1 tasks

```powershell
python data_ingestion.py
python live_nav_fetch.py
python fund_master_explore.py
python validate_data.py
```

`data_ingestion.py` prints each CSV's shape, dtypes, first five rows, missing values, and duplicate-row count. It saves `reports/ingestion_inventory.json`.

`live_nav_fetch.py` requests codes 125497, 119551, 120503, 118632, 119092, and 120841 from `https://api.mfapi.in/mf/{code}`. It saves each response as raw JSON and normalized CSV, plus a combined NAV CSV. It requires internet access. API metadata is treated as authoritative for the returned scheme name.

## Findings from the supplied files

- All 10 requested source CSV files are present.
- The SIP inflows dataset has 12 missing values in `yoy_growth_pct`; inspect whether these are expected initial-period blanks before imputing.
- The supplied NAV history file has 3,211 rows but only one unique scheme code.
- The fund master contains 40 unique AMFI codes, so a one-file comparison cannot establish presence for all 40. `validate_data.py` reports absent-from-supplied-file codes without declaring them invalid.
- The supplied NAV file labels code 125497 as `SBI SMALL CAP FUND - Direct Plan - Growth`, while the assignment describes it as HDFC Top 100 Direct. The live fetch script warns if MFAPI metadata confirms a mismatch.
- AMFI scheme codes are identifiers. Their digits should not be parsed as a reliable encoding of fund house/category/plan; resolve scheme attributes through scheme master/API metadata.

## Git

```powershell
git init
git add .
git commit -m "Day 1: Data ingestion complete"
git branch -M main
git remote add origin https://github.com/Shadman04/bluestock-week-2.git
git push -u origin main
```
