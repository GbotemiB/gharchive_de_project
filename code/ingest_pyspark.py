import os
from pathlib import Path

from prefect import flow, task
from prefect_gcp import GcpCredentials

from spark_config import config


@task(log_prints=True)
def download_to_local(path: Path, year: int, month: int, day: int) -> Path:
    for chunk in range(1, 24):
        name = f"{year}-{month:02}-{day:02}"
        url = f"https://data.gharchive.org/{name}-{chunk}.json.gz"

        os.system(f"wget -P {path} {url}")
    print("data download successful")
    return path


@task(log_prints=True)
def convert_and_save_parquet(path, year: int, month: int, day: int, gcs_bucket):
    df = spark.read.json(f"{path}/*")
    # print(df.count())

    df.write.parquet(
        f"gs://{gcs_bucket}/pq/{year}/{month:02}/{day:02}", mode="overwrite"
    )
    print("write to parquet successful")

    return path


@task(log_prints=True)
def remove_files(path: Path):
    os.system(f"rm -r {path}")
    print(f"successfully removed content in {path}")
    return None


@flow()
def main(year: int, month: int, day: int):
    path = Path(f"data/{year}/{month:02}/{day:02}")
    bucket = "gharchive_dataset_gcs"
    global spark
    spark = config()
    dir = download_to_local(path, year, month, day)
    dir = convert_and_save_parquet(dir, year, month, day, bucket)
    dir = remove_files(path)
    spark.stop()


@flow()
def parent_flow(year: int, months: list, days: list):
    for month in months:
        for day in days:
            main(year, month, day)


if __name__ == "__main__":
    year = 2020
    month = [1]
    day = [1]
    parent_flow(year, month, day)
