
import requests
import json
import pandas as pd

url = "https://api.mfapi.in/mf/125497"

response = requests.get(url, timeout=30)
response.raise_for_status()

data = response.json()

# Save raw JSON
with open("indian_mutual_fund.json", "w") as file:
    json.dump(data, file, indent=4)

# Convert NAV data to DataFrame
df = pd.DataFrame(data["data"])

df["nav"] = pd.to_numeric(df["nav"])
df["scheme_name"] = data["meta"]["scheme_name"]
df["fund_house"] = data["meta"]["fund_house"]
df["scheme_code"] = data["meta"]["scheme_code"]

# Export CSV
df.to_csv("indian_mutual_fund.csv", index=False)

print("API extraction completed successfully!")
print("Total NAV records:", len(df))
print(df.head())
