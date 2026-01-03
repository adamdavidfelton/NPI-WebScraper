import os
import pandas as pd
from npi.lookup import lookup_provider

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "data", "providers.csv")

providers = pd.read_csv(csv_path)

results = []

for _, row in providers.iterrows():
    info = lookup_provider(
        first_name=row["first_name"],
        last_name=row["last_name"],
        state=row.get("state")
    )
    results.append(info)

df_results = pd.DataFrame(results)
df_results.to_csv(os.path.join(BASE_DIR, "output", "providers_with_fax.csv"), index=False)

