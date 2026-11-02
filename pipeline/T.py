import json, glob, os
import pandas as pd

os.makedirs("clean", exist_ok= True)

"""
FLATTEN: nested json to clean rows
"""
rows = []
for path in sorted(glob.glob("raw/*.json")):
    for race in json.load(open(path)):
        for result in race["Results"]:
            rows.append({
                "season": int(race["season"]),
                "round": int(race["round"]),
                "gp": race["raceName"],
                "race_date": race["date"],
                "driver": result["Driver"]["givenName"] + "" + result["Driver"]["familyName"],
                "constructor": result["Constructor"]["name"],
                "grid": int(result["grid"]),
                "position": result["position"],
                "points": result["points"],
                "status": result["status"],
            })

if not rows:
    raise SystemExit("No rows found. Check that raw/ contains season JSON files (run E.py first).")

"""
CLEANING
"""
df = pd.DataFrame(rows)
df["race_date"] = pd.to_datetime(df["race_date"])
df = df.drop_duplicates(subset=["season", "round", "driver"])

"""
CHECKS
"""
print("Shape: ", df.shape)
print("\n Nulls per coloumn: ")
print(df.isnull().sum())
print("\n Rows per season: ")
print(df.groupby("season").size())
print("\n Sample: ")
print(df.head())

"""
SAVE TO CSV
"""
df.to_csv("clean/results.csv", index= False)
print("\n Saved clean/results.csv succuessfully with", len(df), "rows")
