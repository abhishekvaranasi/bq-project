from google.cloud import bigquery
import os 
# Instantiates a client with service account
# client = bigquery.Client.from_service_account_json(os.path.join(os.getcwd(),"validation-193604-3a770385fc34.json"))
client = bigquery.Client()

PROJECTID = os.environ["GCP_PROJECT"]
BUCKETID = os.environ["GCP_BUCKET"]
# BUCKETID = "validation-backup/bigquery-backup"