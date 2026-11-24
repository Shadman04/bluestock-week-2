<<<<<<< HEAD
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
=======
 Bluestock Week 2 — REST API & JSON Deliverable

## Project
Fetch Indian mutual fund NAV history from the public MFapi.in REST API, inspect the JSON response, and convert the NAV records into CSV using Python, Requests and Pandas.

## API
- HTTP method: GET
- Endpoint: https://api.mfapi.in/mf/125497
- Scheme code: 125497
- Scheme: SBI SMALL CAP FUND - Direct Plan - Growth
- Fund house: SBI Mutual Fund

## Included files
- `indian_mutual_fund.py` — Python script that calls the API, saves the raw response as `indian_mutual_fund.json`, and exports NAV history to `indian_mutual_fund.csv`.
- `indian_mutual_fund.csv` — complete CSV dataset supplied for this submission.
- `validation_report.json` — checks performed on the supplied CSV.
- `fetch_to_csv_reference.py` — earlier generic JSONPlaceholder example; retained only as reference, not the main Indian-finance exercise.

## Validation
The supplied CSV contains 3,211 records and 5 columns: `date`, `nav`, `scheme_name`, `fund_house`, and `scheme_code`. NAV is numeric.

## Generate the raw JSON response
The raw API JSON file was not included among the uploaded files. Run the script below with internet access to create it directly from the API. The same run will also regenerate the CSV.

```bash
pip install requests pandas
python indian_mutual_fund.py
```

The script creates:
- `indian_mutual_fund.json` — raw JSON response returned by the API
- `indian_mutual_fund.csv` — tabular NAV dataset

## Concepts demonstrated
1. REST API and HTTP GET request
2. Successful response handling and error checking
3. JSON parsing
4. Data inspection and tabular transformation
5. CSV export with Pandas
>>>>>>> 69e4ca56a9613e80ad6d75676bac9c283408eec7
