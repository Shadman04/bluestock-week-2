# Bluestock Week 2 — FinTech & Software Development

This repository contains the Week 2 learning deliverables, organised by topic.

## Repository structure

- `Stock_Market/` — stock market fundamentals summary and TCS FY 2025–26 financial analysis workbook.
- `REST_API_JSON/` — Python project using MFapi.in to retrieve Indian mutual fund NAV data, inspect JSON and export a complete CSV dataset.
- `Software_Architecture/` — software data-flow diagram.
- `FinTech_Research/` — consolidated Week 2 assignment document, including the FinTech and software development research sections.

## REST API project

The API exercise uses HTTP GET with the public MFapi.in endpoint for scheme code `125497` (SBI Small Cap Fund – Direct Plan – Growth). Python Requests retrieves the response, JSON is parsed, and Pandas converts the NAV history to CSV.

To regenerate the JSON and CSV files:

```bash
pip install requests pandas
cd REST_API_JSON
python indian_mutual_fund.py
```

The script generates `indian_mutual_fund.json` and `indian_mutual_fund.csv`.

## Notes

- The CSV in `REST_API_JSON/` is the complete dataset supplied for this submission.
- The raw full JSON response was not among the files uploaded into this chat. Run the Python script to generate it from the live API.
- Check the assignment brief for any required naming, submission portal or privacy settings before final submission.
