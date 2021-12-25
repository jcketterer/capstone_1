import os, requests

URL = "https://api.openbrewerydb.org/breweries?page=401"

res = requests.get(URL)

print(res.status_code)

for r in res.json():
    print(r["name"])
