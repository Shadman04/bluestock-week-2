"""Fetch live NAV histories from MFAPI and preserve raw JSON + normalized CSV."""
from pathlib import Path
import json
import time
import requests
import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)
SCHEMES = {
    "125497": "HDFC Top 100 Direct (assignment label; verify returned metadata)",
    "119551": "SBI Bluechip",
    "120503": "ICICI Bluechip",
    "118632": "Nippon Large Cap",
    "119092": "Axis Bluechip",
    "120841": "Kotak Bluechip",
}
BASE_URL = "https://api.mfapi.in/mf/{}"


def fetch_scheme(session: requests.Session, code: str, assignment_label: str) -> pd.DataFrame:
    response = session.get(BASE_URL.format(code), timeout=(10, 45))
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict) or not payload.get("data"):
        raise ValueError(f"API returned no NAV data for scheme code {code}")
    (RAW_DIR / f"NAV_{code}.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    meta = payload.get("meta") or {}
    actual_name = meta.get("scheme_name") or meta.get("schemeName") or ""
    rows = pd.DataFrame(payload["data"])
    required = {"date", "nav"}
    if not required.issubset(rows.columns):
        raise ValueError(f"Unexpected response schema for {code}: {list(rows.columns)}")
    rows["date"] = pd.to_datetime(rows["date"], format="%d-%m-%Y", errors="coerce")
    rows["nav"] = pd.to_numeric(rows["nav"], errors="coerce")
    rows["scheme_code"] = str(code)
    rows["scheme_name"] = actual_name or assignment_label
    rows["fund_house"] = meta.get("fund_house") or meta.get("fundHouse") or ""
    rows["assignment_label"] = assignment_label
    rows = rows.dropna(subset=["date", "nav"])
    rows.to_csv(RAW_DIR / f"NAV_{code}.csv", index=False)
    if code == "125497" and actual_name and "HDFC" not in actual_name.upper():
        print(f"WARNING: 125497 was labelled HDFC by the assignment, but MFAPI says: {actual_name}")
    print(f"{code}: saved {len(rows):,} NAV rows | API name: {actual_name or 'not supplied'}")
    return rows


def main() -> None:
    all_frames = []
    failures = []
    with requests.Session() as session:
        session.headers.update({"User-Agent": "Bluestock-Day1-Data-Ingestion/1.0"})
        for code, label in SCHEMES.items():
            try:
                all_frames.append(fetch_scheme(session, code, label))
            except (requests.RequestException, ValueError, KeyError) as exc:
                failures.append({"scheme_code": code, "label": label, "error": str(exc)})
                print(f"ERROR {code}: {exc}")
            time.sleep(0.25)
    if all_frames:
        combined = pd.concat(all_frames, ignore_index=True)
        combined.to_csv(RAW_DIR / "combined_nav_history.csv", index=False)
        print(f"Saved combined NAV history: {len(combined):,} rows")
    report = ROOT / "reports" / "live_nav_fetch_status.json"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps({"successful_schemes": len(all_frames), "failed_schemes": failures}, indent=2), encoding="utf-8")
    if failures:
        print(f"{len(failures)} scheme(s) failed. Details: {report.relative_to(ROOT)}")
    if not all_frames:
        raise SystemExit("No NAV data downloaded. Check internet access and MFAPI availability.")


if __name__ == "__main__":
    main()
