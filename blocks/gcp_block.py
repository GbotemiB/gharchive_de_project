from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket

# alternative to creating GCP blocks in the UI
# copy your own service_account_info dictionary from the json file you downloaded from google
# IMPORTANT - do not store credentials in a publicly available repository!

def gcp_bucket(service_account_json: str) -> None:
    credentials_block = GcpCredentials(
        service_account_info=service_account_json)
    credentials_block.save("gcp-creds", overwrite=True)

    bucket_block = GcsBucket(
        gcp_credentials=GcpCredentials.load("gcp-creds"),
        bucket="gharchive_dataset_gcs",  # insert your  GCS bucket name
    )
    bucket_block.save("gharchive", overwrite=True)
    return None

if __name__=="__main__":
    service_account_json={
                "type": "service_account",
                "project_id": ******************,
                "private_key_id": ******************,
                "private_key": ******************,
                "client_email": ******************,
                "client_id": ******************,
                "auth_uri": ******************,
                "token_uri": ******************,
                "auth_provider_x509_cert_url": ******************,
                "client_x509_cert_url": ******************
            }  # replace the details of your credentials here
    
    
    gcp_bucket(service_account_json=service_account_json)