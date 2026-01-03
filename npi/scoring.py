def score_provider(provider, first_name, last_name, middle=None, state=None, city=None, taxonomy=None):
    score = 0

    basic = provider.get("basic", {})
    addresses = provider.get("addresses", [])
    taxonomies = provider.get("taxonomies", [])
    provider_middle = basic.get("middle_name")

    if basic.get("first_name", "").lower() == first_name.lower():
        score += 1

    if basic.get("last_name", "").lower() == last_name.lower():
        score += 1

    if provider_middle:
        if middle and provider_middle.startswith(middle):
            score += 1

    if state and any(a.get("state") == state for a in addresses):
        score += 1

    if city and any(a.get("city", "").lower() == city.lower() for a in addresses):
        score += 1

    if taxonomy and any(t.get("desc", "").lower() == taxonomy.lower() for t in taxonomies):
        score += 1

    return score

