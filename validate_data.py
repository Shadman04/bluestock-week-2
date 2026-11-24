"""Validate AMFI scheme codes in fund master against supplied NAV history."""
from pathlib import Path
import json
import pandas as pd
ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data/raw"
REPORTS = ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)
master = pd.read_csv(RAW / "01_fund_master.csv", dtype={"amfi_code": "string"})
nav = pd.read_csv(RAW / "02_nav_history.csv", dtype={"scheme_code": "string"})
master_codes = set(master["amfi_code"].dropna().str.strip())
nav_codes = set(nav["scheme_code"].dropna().str.strip())
matched, missing = sorted(master_codes & nav_codes), sorted(master_codes - nav_codes)
validation = master[["amfi_code", "scheme_name", "fund_house"]].copy()
validation["present_in_nav_history"] = validation["amfi_code"].isin(nav_codes)
validation.to_csv(ROOT / "data/processed/amfi_code_validation.csv", index=False)
summary = {
    "fund_master_unique_codes": len(master_codes),
    "nav_history_unique_codes": len(nav_codes),
    "matched_codes": len(matched),
    "fund_master_codes_missing_from_supplied_nav_history": len(missing),
    "match_rate_pct": round(100 * len(matched) / len(master_codes), 2) if master_codes else 0,
    "matched_codes": matched,
    "missing_codes": missing,
    "interpretation": "Missing means no matching code was present in the supplied NAV history file; it does not prove that the AMFI code is invalid.",
}
(REPORTS / "data_quality_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
lines = ["# Day 1 Data Quality Summary", "", f"- Fund master unique AMFI codes: **{len(master_codes)}**", f"- Supplied NAV history unique scheme codes: **{len(nav_codes)}**", f"- Codes matched: **{len(matched)}**", f"- Fund master codes absent from supplied NAV history: **{len(missing)}**", f"- Match rate: **{summary['match_rate_pct']}%**", "", "## Interpretation", summary["interpretation"], "", "## Data anomaly", "The supplied NAV history file contains scheme code 125497 with the name `SBI SMALL CAP FUND - Direct Plan - Growth`. The assignment labels 125497 as HDFC Top 100 Direct. Verify the code/name mapping against MFAPI metadata before treating it as HDFC data.", "", "## Important scope note", "The supplied NAV history contains only the scheme codes present in that file. This check tests presence in the supplied file; it is not a complete live-AMFI validity check."]
(REPORTS / "DATA_QUALITY_SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("Fund master unique codes:", len(master_codes))
print("NAV history unique codes:", len(nav_codes))
print("Matched:", len(matched), "| Missing from supplied NAV history:", len(missing), "| Match rate:", summary["match_rate_pct"], "%")
print("Saved data/processed/amfi_code_validation.csv and reports/data_quality_summary.json")
