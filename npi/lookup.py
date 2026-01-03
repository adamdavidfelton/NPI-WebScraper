import requests
from .scoring import score_provider

def lookup_provider(first_name, last_name, state=None, city=None, taxonomy=None):
    url = "https://npiregistry.cms.hhs.gov/api/"

    params = {
        "version": "2.1",
        "first_name": first_name,
        "last_name": last_name,
        "limit": 10
    }

    if state:
        params["state"] = state

    response = requests.get(url, params=params).json()
    results = response.get("results", [])
    if not results:
        return None

    # Score all providers
    scored = []
    for p in results:
        s = score_provider(
            p,
            first_name=first_name,
            last_name=last_name,
            state=state,
            city=city,
            taxonomy=taxonomy
        )
        scored.append((s, p))

    scored.sort(key=lambda x: x[0], reverse=True)
    best_score, provider = scored[0]

    if best_score == 0:
        return None

    practice = next(
        (a for a in provider["addresses"] if a["address_purpose"] == "LOCATION"),
        None
    )

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
        "fax": practice.get("fax_number"),
        "confidence": best_score
    }

