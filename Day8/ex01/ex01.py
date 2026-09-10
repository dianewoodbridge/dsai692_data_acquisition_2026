import datetime
import json
import os
import requests

from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi import FastAPI
from google.oauth2 import service_account
from google.cloud import storage

app = FastAPI()


def store_to_gcs(service_account_key: str,
                 project_id: str,
                 bucket_name: str,
                 file_name: str,
                 data: str) -> None:
    credentials = service_account.Credentials.from_service_account_file(
        service_account_key)
    client = storage.Client(project=project_id,
                            credentials=credentials)
    bucket = client.bucket(bucket_name)
    file = bucket.blob(file_name)
    file.upload_from_string(data)


def get_json_response(url: str, api_key: str):
    header = {'X-Api-Key': api_key}
    response = requests.get(url, headers=header)
    return response.json()


@app.get("/retrieve_and_store")
def retrieve_and_store(url: str):
    # # load_dotenv(dotenv_path="/tmp_vol/.env")
    data_gov_api_key = os.getenv("DATA_GOV_API_KEY")
    service_account_key = os.getenv("GCP_SERVICE_ACCOUNT_KEY")
    project_id = os.getenv("GCP_PROJECT_ID")
    bucket_name = os.getenv("GCP_BUCKET_NAME")
    file_name = f"sf_police_report/{datetime.date.today()}.json"
    try:
        data = get_json_response(url, data_gov_api_key)
        try:
            store_to_gcs(service_account_key,
                         project_id,
                         bucket_name,
                         file_name,
                         json.dumps(data, indent=4))
        except Exception as e:
            raise HTTPException(status_code=400,
                                detail=f"Was able to call {url},\
                                    but may not have permission to store in GCS.\
                                    Error Message: {e}")

    except Exception as e:
        raise HTTPException(status_code=403,
                            detail=f"Could not call {url}\n \
                                    Error Message: {e}")

    return {"message": "Successfully stored the extracted data"}
