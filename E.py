import requests, json, os, time

BASE = 'https://api.jolpi.ca/ergast/f1'
os.makedirs("raw", exist_ok= True)

def fetch_season(year):
    races, offset = [], 0
    while True:
        r = requests.get(f"{BASE}/{year}/results.json",
            params={"limit": 30, "offset": offset}, timeout=30)
        r.raise_for_status()
        data = r.json()["MRData"]
        races.extend(data["RaceTable"]["Races"])
        offset += 100

        if offset >= int(data["total"]):
            break
        
        time.sleep(1)

    return races

for year in [2023]:
    path = f"raw/{year}.json"

    if os.path.exists(path):
        print(year, "already downloaded", "skipping...")
        continue

    races = fetch_season(year)

    with open(path, 'w') as f:
        json.dump(races, f)
    
    print(f"{year} saved. \n {len(races)}: saved entries.")
    print(json.dumps(races[0]["Results"][0], indent=2))
    
