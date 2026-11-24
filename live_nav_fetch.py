"""
Fetch live NAV history for every unique AMFI code in data/raw/01_fund_master.csv.

Run from the project root:
    python live_nav_fetch.py

Outputs:
    data/raw/NAV_<AMFI_CODE>.csv
    data/raw/NAV_<AMFI_CODE>.json
    data/raw/combined_nav_history.csv
    reports/live_nav_fetch_status.json
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent
MASTER_PATH = ROOT / "data" / "raw" / "01_fund_master.csv"
RAW_DIR = ROOT / "data" / "raw"
REPORT_PATH = ROOT / "reports" / "live_nav_fetch_status.json"
API_URL = "https://api.mfapi.in/mf/{code}"
TIMEOUT_SECONDS = 25
REQUEST_DELAY_SECONDS = 0.35

CODE_COLUMNS = (
    "amfi_code", "amfi scheme code", "scheme_code", "scheme code",
    "scheme_code_amfi", "code",
)
NAME_COLUMNS = (
    "scheme_name", "scheme name", "fund_name", "fund name",
    "scheme", "name", "scheme_title",
)


def normalized_column(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")


def find_column(columns, candidates):
    lookup = {normalized_column(col): col for col in columns}
    for candidate in candidates:
        key = normalized_column(candidate)
        if key in lookup:
            return lookup[key]
    return None


def load_schemes() -> list[tuple[str, str]]:
    if not MASTER_PATH.exists():
        raise FileNotFoundError(f"Fund master not found: {MASTER_PATH}")

    master = pd.read_csv(MASTER_PATH, dtype=str)
    code_col = find_column(master.columns, CODE_COLUMNS)
    if code_col is None:
        raise ValueError(
            "Could not identify the AMFI code column. "
            f"Available columns: {list(master.columns)}"
        )

    name_col = find_column(master.columns, NAME_COLUMNS)
    master[code_col] = master[code_col].fillna("").str.strip()
    master = master[master[code_col].str.fullmatch(r"\d+", na=False)]
    master = master.drop_duplicates(subset=[code_col])

    schemes = []
    for _, row in master.iterrows():
        code = str(row[code_col]).strip()
        label = str(row[name_col]).strip() if name_col and pd.notna(row[name_col]) else ""
        schemes.append((code, label))
    return schemes


def fetch_one(session: requests.Session, code: str, master_label: str):
    response = session.get(API_URL.format(code=code), timeout=TIMEOUT_SECONDS)
    response.raise_for_status()
    payload = response.json()

    meta = payload.get("meta") or {}
    nav_rows = payload.get("data") or []
    api_name = str(meta.get("scheme_name") or "").strip()
    api_code = str(meta.get("scheme_code") or code).strip()

    if not nav_rows:
        raise ValueError("API returned no NAV history rows")

    frame = pd.DataFrame(nav_rows)
    if "date" not in frame.columns or "nav" not in frame.columns:
        raise ValueError(f"Unexpected NAV response columns: {list(frame.columns)}")

    frame["scheme_code"] = code
    frame["scheme_name"] = api_name
    frame["master_scheme_name"] = master_label
    frame["api_scheme_code"] = api_code
    frame["name_mismatch"] = bool(
        master_label and api_name and
        re.sub(r"\W+", "", master_label).lower() !=
        re.sub(r"\W+", "", api_name).lower()
    )

    # Preserve the complete raw response as well as the normalized NAV rows.
    (RAW_DIR / f"NAV_{code}.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    frame.to_csv(RAW_DIR / f"NAV_{code}.csv", index=False)
    return frame, api_name, len(frame)


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    schemes = load_schemes()
    print(f"Found {len(schemes)} unique AMFI codes in fund master.")

    successes = []
    failures = []

    with requests.Session() as session:
        session.headers.update({
            "User-Agent": "Bluestock-Day1-Data-Ingestion/2.0"
        })

        for index, (code, label) in enumerate(schemes, start=1):
            print(f"[{index}/{len(schemes)}] Fetching AMFI code {code} ...", end=" ")
            try:
                frame, api_name, rows = fetch_one(session, code, label)
                successes.append({
                    "amfi_code": code,
                    "master_scheme_name": label,
                    "api_scheme_name": api_name,
                    "nav_rows": rows,
                    "name_mismatch": bool(
                        label and api_name and
                        re.sub(r"\W+", "", label).lower() !=
                        re.sub(r"\W+", "", api_name).lower()
                    ),
                })
                print(f"OK ({rows} NAV rows)")
            except (requests.RequestException, ValueError, KeyError, TypeError) as exc:
                failures.append({
                    "amfi_code": code,
                    "master_scheme_name": label,
                    "error": f"{type(exc).__name__}: {exc}",
                })
                print(f"FAILED ({type(exc).__name__}: {exc})")

            if index < len(schemes):
                time.sleep(REQUEST_DELAY_SECONDS)

    if successes:
        frames = []
        for item in successes:
            path = RAW_DIR / f"NAV_{item['amfi_code']}.csv"
            frames.append(pd.read_csv(path, dtype=str))
        combined = pd.concat(frames, ignore_index=True)
        combined.to_csv(RAW_DIR / "combined_nav_history.csv", index=False)

    report = {
        "fund_master_unique_codes": len(schemes),
        "attempted_schemes": len(schemes),
        "successful_schemes": len(successes),
        "failed_scheme_count": len(failures),
        "failed_schemes": failures,
        "successful_scheme_details": successes,
        "coverage_pct": round(100 * len(successes) / len(schemes), 2) if schemes else 0,
        "note": (
            "A failed request means the API did not return usable NAV data during this run; "
            "it does not by itself prove that an AMFI code is invalid."
        ),
    }
    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print("\n----- LIVE NAV FETCH SUMMARY -----")
    print(f"Attempted:  {len(schemes)}")
    print(f"Successful: {len(successes)}")
    print(f"Failed:     {len(failures)}")
    print(f"Coverage:   {report['coverage_pct']}%")
    print(f"Report:     {REPORT_PATH.relative_to(ROOT)}")
    print("Review failed_schemes and name_mismatch flags before interpreting coverage.")


if __name__ == "__main__":
    main()
