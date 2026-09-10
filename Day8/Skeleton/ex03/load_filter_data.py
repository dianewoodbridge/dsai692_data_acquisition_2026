import json
import os
from dotenv import load_dotenv

from google.oauth2 import service_account
from google.cloud import storage
import streamlit as st
import pandas as pd


def retrieve_data_from_gcs(service_account_key: str,
                           project_id: str,
                           bucket_name: str,
                           file_name_prefix: str,
                           key_list: list
                           ) -> list:
    credentials = service_account.Credentials.from_service_account_file(
        service_account_key)
    client = storage.Client(project=project_id,
                            credentials=credentials)
    bucket = client.bucket(bucket_name)
    output = []
    for blob in bucket.list_blobs():
        if blob.name.startswith(file_name_prefix):
            print(blob.name)
            file = bucket.blob(blob.name)
            content = json.loads(file.download_as_string())

            for data in content:
                row = []

                for key in key_list:
                    row.append(data.get(key, None))
                output.append(row)
    return output


@st.cache_data  # caching data as transforming date, and time takes long
def load_data():
    load_dotenv()
    service_account_key = os.getenv("GCP_SERVICE_ACCOUNT_KEY")
    project_id = os.getenv("GCP_PROJECT_ID")
    bucket_name = os.getenv("GCP_BUCKET_NAME")
    file_name_prefix = f"sf_police_report/"
    key_list = ['incident_datetime', 'report_datetime', 'incident_code',
                'incident_category', 'incident_description', 'latitude',
                'longitude', 'police_district']
    data = retrieve_data_from_gcs(service_account_key,
                                  project_id,
                                  bucket_name,
                                  file_name_prefix,
                                  key_list)
    crime_pd = pd.DataFrame(data, columns=key_list)
    crime_pd["longitude"] = crime_pd["longitude"].astype(float)
    crime_pd["latitude"] = crime_pd["latitude"].astype(float)
    # # Convert TIME OCC to string and pad with leading zeros if necessary
    crime_pd["incident_datetime"] = crime_pd["incident_datetime"].astype(
        "datetime64[s]")
    crime_pd["report_datetime"] = crime_pd["report_datetime"].astype(
        "datetime64[s]")
    return crime_pd


def filter_data(data, filter_column):
    if filter_column in ["incident_datetime", "report_datetime",
                         "latitude", "longitude"]:
        if filter_column in ["incident_datetime", "report_datetime"]:
            filter_value_start = st.date_input("Start Date")
            filter_value_end = st.date_input("End Date")
            if filter_value_start and filter_value_end:
                # Use logical AND for boolean series comparison
                data = data[(data[filter_column].dt.date >= filter_value_start) & (
                    data[filter_column].dt.date <= filter_value_end)]
        else:
            filter_value_start = st.text_input("Start Value")
            filter_value_end = st.text_input("End Value")

            if filter_value_start and filter_value_end:
                data = data[(data[filter_column] >= float(filter_value_start))
                            & (data[filter_column] <= float(filter_value_end))]
    else:
        filter_value = st.text_input("Enter the value to show in the table ")
        if filter_value:
            data = data[data[filter_column] == filter_value]
    return data
