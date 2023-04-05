from prefect_dbt.cloud import DbtCloudCredentials
from prefect_gcp.cloud_storage import GcsBucket


def dbt_block(api_key: str, account_id:int) -> None:
    credentials_block = DbtCloudCredentials(
        api_key=api_key,
        account_id=account_id
    )
    credentials_block.save("dbt-gharchive", overwrite=True)
    return None


if __name__=="__main__":
    
    api_key = "" #enter dbt api key
    account_id =  #enter dbt account id
    dbt_block(api_key, account_id)