"""Load and profile all CSV files in data/raw."""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "data" / "raw"
REPORT_DIR = ROOT / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    files = sorted(RAW_DIR.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files found in {RAW_DIR}")
    inventory = []
    print(f"Found {len(files)} CSV datasets (assignment expects 10).")
    for path in files:
        df = pd.read_csv(path, low_memory=False)
        print("\n" + "=" * 88)
        print(f"FILE: {path.name}")
        print("SHAPE:", df.shape)
        print("DTYPES:\n", df.dtypes.to_string())
        print("HEAD (first 5 rows):\n", df.head().to_string(index=False))
        missing = df.isna().sum()
        duplicate_rows = int(df.duplicated().sum())
        print("MISSING VALUES:\n", missing[missing.gt(0)].to_string() if missing.gt(0).any() else "None")
        print("DUPLICATE ROWS:", duplicate_rows)
        inventory.append({
            "file": path.name,
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "shape": list(df.shape),
            "dtypes": {str(c): str(t) for c, t in df.dtypes.items()},
            "missing_values": {str(c): int(v) for c, v in missing.items() if v},
            "duplicate_rows": duplicate_rows,
        })
    out = REPORT_DIR / "ingestion_inventory.json"
    out.write_text(json.dumps(inventory, indent=2), encoding="utf-8")
    print(f"\nSaved dataset inventory to: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
