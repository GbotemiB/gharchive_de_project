from prefect import flow, task

from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, when

from spark_config import config

@task(log_prints=True)
def read_data_from_gcs(path: str):
    """
    This will read dataset from gcs
    it will create new columns and drop some columns
    finally return a spark dataframe
    """

    df = spark.read.parquet(path)
    # print(df.count())

    df_merge = (
        df.withColumn("users", col("actor.login"))
        .withColumn("repo_id", col("repo.id"))
        .withColumn("repo_name", split(col("repo.name"), "/")[1])
        .withColumn("org_exists", col("org").isNotNull())
        .withColumn(
            "count_commits",
            when(col("payload.size") >= 1, col("payload.size")).otherwise(0),
        )
    )

    df_merge = (
        df_merge.drop(col("actor"))
        .drop(col("repo"))
        .drop(col("payload"))
        .drop(col("org"))
    )
    print("repartitioning data")
    df_merge = df_merge.repartition("created_at")

    print(df_merge.columns)
    print("operations completed on dataset")
    return df_merge


@task(log_prints=True)
def write_to_bq(df, project_ID: str, project_dataset: str, table: str) -> None:
    """
    this will write the dataframe to bigquery
    """
    df.write.format("bigquery").mode("append").option("writeMethod", "direct").option(
        "partitionBy", "created_at"
    ).option("partitionField", "created_at").save(
        f"{project_ID}.{project_dataset}.{table}"
    )

    print("data write to bigquery successful")


@flow()
def execute(year: int, month: int):
    """
    this is the execution function on all the operations
    """
    bucket = "gharchive_dataset_gcs"
    path = f"gs://{bucket}/pq/{year}/{month:02}/*/*"
    project_ID = "onyx-nexus-382423"
    project_dataset = "gharchive_dataset"
    table = "github_data"

    global spark
    spark = config()
    data = read_data_from_gcs(path)
    write_to_bq(
        df=data, project_ID=project_ID, project_dataset=project_dataset, table=table
    )
    spark.stop()

@flow()
def parent_flow(year: int, months: list) -> None:
    
    for month in months:
        execute(year=year, month=month)

if __name__=="__main__":
    year=2020
    month=[1]
    parent_flow(year, month)
