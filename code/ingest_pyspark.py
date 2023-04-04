import os

os.environ['PYSPARK_SUBMIT_ARGS'] = '--master local[2] pyspark-shell'

from pathlib import Path

from prefect import flow, task
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from pyspark.sql import SparkSession


def config():
    credentials_location = "credentials/credentials.json"

    conf = (
        SparkConf()
        .setMaster("local[*]")
        .setAppName("test")
        .set(
            "spark.jars",
            "lib/gcs-connector-hadoop3-2.2.5.jar, \
            lib/spark-3.2-bigquery-0.29.0-preview.jar",
        )
        .set("spark.hadoop.google.cloud.auth.service.account.enable", "true")
        .set(
            "spark.hadoop.google.cloud.auth.service.account.json.keyfile",
            credentials_location,
        )
        .set("spark.executor.memory", "8g")
        .set("spark.driver.memory", "8g")
    )

    # hadoop configurations
    sc = SparkContext(conf=conf)
    hadoop_conf = sc._jsc.hadoopConfiguration()

    hadoop_conf.set(
        "fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS"
    )
    hadoop_conf.set(
        "fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem"
    )
    hadoop_conf.set("fs.gs.auth.service.account.json.keyfile", credentials_location)
    hadoop_conf.set("fs.gs.auth.service.account.enable", "true")

    # creating spark session
    spark = SparkSession.builder.config(conf=sc.getConf()).getOrCreate()

    return spark


@task(log_prints=True)
def download_to_local(path: Path, year: int, month: int, day: int) -> Path:
    for chunk in range(1, 24):
        name = f"{year}-{month:02}-{day:02}"
        url = f"https://data.gharchive.org/{name}-{chunk}.json.gz"

        os.system(f"wget -P {path} {url}")
    print("data download successful")
    return path


@task(log_prints=True)
def convert_and_save_parquet(path, year: int, month: int, day: int):
    df = spark.read.json(f"{path}/*")
    # print(df.count())

    df.write.parquet(
        f"gs://gharchive_dataset_gcs/pq/{year}/{month:02}/{day:02}", mode="overwrite"
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
    global spark
    spark = config()
    dir = download_to_local(path, year, month, day)
    dir = convert_and_save_parquet(dir, year, month, day)
    dir = remove_files(path)
    spark.stop()


@flow()
def parent_flow(year: int, months: list, days: list):
    for month in months:
        for day in days:
            main(year, month, day)


if __name__ == "__main__":
    year = 2020
    month = [1, 2]
    day = [1, 2]
    parent_flow(year, month, day)
