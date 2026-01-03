import os
import pandas as pd
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "data", "providers.csv")

providers = pd.read_csv(csv_path)


def lookup_provider(first_name, last_name, state=None):
    url = "https://npiregistry.cms.hhs.gov/api/"

    params = {
        "version": "2.1",
        "first_name": first_name,
        "last_name": last_name,
        "limit": 10 }

    if state:
        params["state"] = state

    response = requests.get(url, params=params).json()

    results = response.get("results", [])
    if not results:
        return None

    # Take the first match (you can refine this later)
    provider = results[0]

    # Find the practice location address
    practice = next(
        (a for a in provider["addresses"] if a["address_purpose"] == "LOCATION"),
        None )

    if not practice:
        return None

    return {
        "npi": provider["number"],
        "first_name": provider["basic"].get("first_name"),
        "last_name": provider["basic"].get("last_name"),
        "address": practice.get("address_1"),
        "city": practice.get("city"),
        "state": practice.get("state"),
        "phone": practice.get("telephone_number"),
        "fax": practice.get("fax_number")
    }
results = []

for _, row in providers.iterrows():
    info = lookup_provider(
        first_name=row["first_name"],
        last_name=row["last_name"],
        state=row.get("state")
    )
    results.append(info)

import pandas as pd

df_results = pd.DataFrame(results)

df_results.to_csv("output/providers_with_fax.csv", index=False)