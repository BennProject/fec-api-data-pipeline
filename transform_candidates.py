import json
from io import BytesIO

import boto3
import pandas as pd

bucket_name = "corey-fec-data-pipeline-2026"

raw_key = (
    "raw/fec/candidates/"
    "snapshot_date=2026-10-08/"
    "candidates.json"
)

curated_key = (
    "curated/fec/candidates/"
    "snapshot_date=2026-10-08/"
    "candidates.parquet"
)

curated_fields = [
    "candidate_id",
    "name",
    "office",
    "office_full",
    "state",
    "district",
    "party",
    "party_full",
    "candidate_status",
    "candidate_inactive",
    "incumbent_challenge",
    "incumbent_challenge_full",
    "has_raised_funds",
    "federal_funds_flag",
    "first_file_date",
    "last_file_date",
    "load_date",
    "election_years",
]

s3 = boto3.client("s3")

response = s3.get_object(
    Bucket=bucket_name,
    Key=raw_key
)

raw_data = json.loads(
    response["Body"].read().decode("utf-8")
)

records = raw_data["results"]

df = pd.DataFrame(records)

df = df[curated_fields]

parquet_buffer = BytesIO()

df.to_parquet(
    parquet_buffer,
    index=False,
    engine="pyarrow"
)

s3.put_object(
    Bucket=bucket_name,
    Key=curated_key,
    Body=parquet_buffer.getvalue()
)

print("Transformation complete.")
print("Rows transformed:", len(df))
print("Columns:", len(df.columns))
print(f"s3://{bucket_name}/{curated_key}")
