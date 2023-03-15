from prefect import task, flow

from prefect_dbt.cloud import DbtCloudCredentials, DbtCloudJob
from prefect_dbt.cloud.jobs import run_dbt_cloud_job

@flow() 
def run_dbt_job():
    dbt_cloud_credential = DbtCloudCredentials.load("dbt-gharchive")
    dbt_cloud_job = DbtCloudJob(
        dbt_cloud_credentials=dbt_cloud_credential,
        job_id="234267")

    run = run_dbt_cloud_job(
        dbt_cloud_job, 
        targeted_retries = 1,
    )

    return run

if __name__=="__main__":
    run_dbt_job()
