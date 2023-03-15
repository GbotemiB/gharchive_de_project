from prefect import task, flow

from prefect_dbt.cloud import DbtCloudCredentials, DbtCloudJob
from prefect_dbt.cloud.jobs import run_dbt_cloud_job


def run_dbt_job():
    dbt_cloud_credentials = DbtCloudCredentials.load("dbt-gharchive")
    dbt_cloud_job = DbtCloudJob.load(
        dbt_cloud_credentials=dbt_cloud_credentials,
        job_id="234267"
    )

    run = run_dbt_cloud_job(
        dbt_cloud_job, 
        targeted_retries = 1,
    )

    return run
