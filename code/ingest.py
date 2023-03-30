import os
from pathlib import Path

import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket

# from calender import monthrange


@task()
def download_to_local(url: str, year: int, month: int, day: int) -> Path:
    path = Path(f"data/{year}/{month:02}/{day:02}")
    os.system(f"wget -P {path} {url}")
    return path


@task(log_prints=True)
def convert_to_parquet(
    path: Path, dataset_file: str, year: int, month: int, day: int
) -> Path:
    file = f"{path}/{dataset_file}.json.gz"
    print(file)
    df = pd.read_json(file, lines=True)
    path = f"{year}/{month:02}/{day:02}"

    try:
        df.to_parquet(f"pq/{path}/{dataset_file}.parquet")
    except OSError:
        os.system(f"mkdir -p pq/{path}")
        df.to_parquet(f"pq/{path}/{dataset_file}.parquet")

    print("saved successfully to parquet")

    return path


@task(retries=3)
def upload_to_gcs(path: Path, dataset_file: str):
    # prefect gcs block
    gcp_block = GcsBucket.load("gharchive")
    gcp_block.upload_from_path(
        from_path=(f"pq/{path}/{dataset_file}.parquet"),
        to_path=(f"pq/{path}/{dataset_file}.parquet"),
    )
    return path


@task(log_prints=True)
def remove_files(path: Path, dataset_file: str):
    os.system(f"rm data/{path}/{dataset_file}.json.gz")
    os.system(f"rm pq/{path}/{dataset_file}.parquet")
    print("successfully removed {dataset_file}")
    return


@flow()
def main(year: int, month: int, day: int):
    for chunk in range(1, 23):
        dataset_file = f"{year}-{month:02}-{day:02}-{chunk}"
        dataset_url = f"https://data.gharchive.org/{dataset_file}.json.gz"

        path = download_to_local(dataset_url, year, month, day)
        path = convert_to_parquet(path, dataset_file, year, month, day)
        path = upload_to_gcs(path, dataset_file)
        remove_files(path, dataset_file)


@flow()
def parent_flow(year: int, months: list, days: list):
    for month in months:
        try:
            for day in days:
                main(year, month, day)
        except FileNotFoundError:
            print("no more data")
            pass


if __name__ == "__main__":
    year = 2015
    month = [1, 2]  # [i for i in range(1,13)]
    """for i in month:
        ranGe = monthrange(year, i)[1]
        day = [i for i in range(1, ranGe+1)]"""

    day = [i for i in range(1, 32)]
    parent_flow(year, month, day)
