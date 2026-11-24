"""Explore fund master dimensions and explain AMFI scheme codes."""
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parent
master = pd.read_csv(ROOT / "data/raw/01_fund_master.csv", dtype={"amfi_code": "string"})
for col in ["fund_house", "category", "sub_category", "risk_category"]:
    print(f"\nUnique {col} ({master[col].nunique()}):")
    print("\n".join(sorted(master[col].dropna().astype(str).unique())))
print("\nAMFI scheme code notes:")
print("AMFI scheme codes are identifiers assigned to schemes; do not infer fund house, category, plan, or growth/IDCW from the digits.")
print("Use the official scheme master/API metadata to map a code to its scheme name.")
