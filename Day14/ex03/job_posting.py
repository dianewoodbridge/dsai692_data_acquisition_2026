import json

from google.oauth2 import service_account
from google.cloud import storage
import streamlit as st
import pandas as pd

from user_definition import *


def retrieve_data_from_gcs(service_account_key: str,
                           project_id: str,
                           bucket_name: str,
                           file_name_prefix: str
                           ) -> dict:
    """
    Retrieve file contents from all files starting with 'file_name_prefix'
    in "bucket_name" and returns a dictionary including "results",
    "job_titles", and"company_dict"

    Args:
        service_account_key (str) : path of service account key file(.json)
        project_id (str) : GCP Project ID where bucket is located
        bucket_name (str) : bucket name
        file_name_prefix (str) : prefix of files to retrieve data.
                                 (Ex."job_search/")

    Returns:
        dict: in a following format
            {"results": a list including "results" from all the files
                        starting with file_name_prefix,
             "job_titles": a list including unique "job_title"s
                           from all the files starting with file_name_prefix,
             "company_dict": a dictionary including all "company_dict"s
                            from all the files starting with file_name_prefix
            }
    """
    credentials = service_account.Credentials.from_service_account_file(
        service_account_key)
    client = storage.Client(project=project_id,
                            credentials=credentials)
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs()

    content = []
    job_titles = []
    company_dict = dict()
    for blob in blobs:
        if blob.name.startswith(file_name_prefix):
            blob_data = json.loads(blob.download_as_bytes())
            content += blob_data["results"]
            job_titles.append(blob_data["job_title"])
            company_dict = company_dict | blob_data["company_dict"]
    job_titles = list(set(job_titles))
    job_titles.sort()
    return {"results": content,
            "job_titles": job_titles,
            "company_dict": company_dict}


if __name__ == '__main__':
    # Title should be comma separated strings of job titles in ascending order.
    # Company list on the side bar should include unique names
    # in ascending order.
    # The dataframe should be filtered based on the selection on the sidebar.
    # The dataframe should only include unique values.
    # The dataframe should have date, title, and link columns where link
    # should be a hyperlink.
    gcs_data = retrieve_data_from_gcs(service_account_file_path,
                                      project_id,
                                      bucket_name,
                                      file_name_prefix)
    role_name = ", ".join(gcs_data["job_titles"])
    company_dictionary = gcs_data["company_dict"]
    gcs_data_result = gcs_data["results"]
    st.title(f"{role_name} Job Listings")
    with st.sidebar:
        st.write("Filter by Company")
        unique_categories = list(company_dictionary.keys())
        unique_categories.sort()
        selected_categories = []

        for category in unique_categories:
            if st.checkbox(f"{category}",
                           value=True,
                           key=f"checkbox_{category}"):
                selected_categories.append(company_dictionary[category])
        data = pd.DataFrame(gcs_data_result)
        filtered_df = data[data['link']
                           .str.startswith(tuple(selected_categories))]

        # Return date, title, skills, and link from the filtered_df.
        filtered_df = filtered_df[["date", "title", "skills", "link"]]
        filtered_df = filtered_df.drop_duplicates(subset=["link"])
    st.dataframe(filtered_df,
                 hide_index=True,
                 column_config={
                     "link": st.column_config.LinkColumn()})
