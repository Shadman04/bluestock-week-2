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
