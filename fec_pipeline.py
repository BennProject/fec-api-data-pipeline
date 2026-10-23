import os
import time
import json
from datetime import date

import boto3
import requests

API_KEY = os.getenv("FEC_API_KEY")

url = "https://api.open.fec.gov/v1/candidates/"

params = {
    "api_key": API_KEY,
    "election_year": 2026,
    "office": ["H", "S"],
    "is_active_candidate": True,
    "per_page": 100,
    "page": 1
}

all_results = []

while True:
    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    current_page = data["pagination"]["page"]
    total_pages = data["pagination"]["pages"]
    total_count = data["pagination"]["count"]

    all_results.extend(data["results"])

    print(
        f"Page {current_page} of {total_pages} "
        f"- collected {len(all_results)} records so far"
    )

    if current_page >= total_pages:
        break

    params["page"] += 1
    time.sleep(1)

print("\nFinished.")
print("API reported total records:", total_count)
print("Records collected:", len(all_results))

if len(all_results) == total_count:
    print("Record count matches.")
else:
    print("WARNING: Record count does not match.")

raw_payload = {
    "snapshot_date": str(date.today()),
    "record_count": len(all_results),
    "results": all_results
}

bucket_name = "corey-fec-data-pipeline-2026"

s3_key = (
    f"raw/fec/candidates/"
    f"snapshot_date={date.today()}/"
    f"candidates.json"
)

s3 = boto3.client("s3")

s3.put_object(
    Bucket=bucket_name,
    Key=s3_key,
    Body=json.dumps(raw_payload),
    ContentType="application/json"
)

print("\nUpload complete.")
print(f"s3://{bucket_name}/{s3_key}")
