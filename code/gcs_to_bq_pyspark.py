import pyspark
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.context import SparkContext

from pyspark.sql import types
from pyspark.sql.types import *
from pyspark.sql import functions as F
from pyspark.sql.functions import col, split, when

from prefect import task, flow

def config():
    credentials_location = '/home/gbotemi/credentials/credentials.json'

    conf = SparkConf() \
        .setMaster('local[*]') \
        .setAppName('test') \
        .set("spark.jars", "/home/gbotemi/lib/gcs-connector-hadoop3-2.2.5.jar, /home/gbotemi/lib/spark-3.2-bigquery-0.29.0-preview.jar") \
        .set("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
        .set("spark.hadoop.google.cloud.auth.service.account.json.keyfile", credentials_location)

    #hadoop configurations
    sc = SparkContext(conf=conf)
    hadoop_conf = sc._jsc.hadoopConfiguration()

    hadoop_conf.set("fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
    hadoop_conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
    hadoop_conf.set("fs.gs.auth.service.account.json.keyfile", credentials_location)
    hadoop_conf.set("fs.gs.auth.service.account.enable", "true")

    #creating spark session
    spark = SparkSession.builder \
        .master("local[*]") \
        .appName('test') \
        .config(conf=sc.getConf()) \
        .getOrCreate()

    return spark

@task(log_prints=True)
def read_data_from_gcs(path: str):
    """ 
        This will read dataset from gcs
        it will create new columns and drop some columns
        finally return a spark dataframe
    """

    df = spark.read.parquet(path)
    #print(df.count())

    df_merge = df.withColumn("users" ,col("actor.login")) \
        .withColumn("repo_id", col("repo.id")) \
        .withColumn("repo_name", split(col("repo.name"), "/")[1]) \
        .withColumn("org_exists", col("org").isNotNull()) \
        .withColumn("count_commits", when(col("payload.size") >= 1, col("payload.size")).otherwise(0))
    
    df_merge = df_merge.drop(col('actor')) \
        .drop(col('repo')) \
        .drop(col('payload')) \
        .drop(col('org'))
    print("repartitioning data")
    df_merge = df_merge.repartition('created_at')

    print(df_merge.columns)
    print("operations completed on dataset")
    return df_merge

@task(log_prints=True)
def write_to_bq(df, project_ID: str, project_dataset: str, table: str) -> None:
    """
        this will write the dataframe to bigquery
    """
    df.write \
        .format("bigquery") \
        .mode("append") \
        .option("writeMethod", "direct") \
        .option("partitionBy", "created_at") \
        .option("partitionField", "created_at") \
        .save(f"{project_ID}.{project_dataset}.{table}")

    print("data write to bigquery successful")


@flow()
def execute(year: int, month: int):
    """
        this is the execution function on all the operations
    """
   
    path = f"gs://gharchive-data/pq/{year}/{month:02}/*/*"
    project_ID = "gharchive-379414"
    project_dataset = "gharchive_data"
    table = f"{year}"

    global spark
    spark = config()
    data = read_data_from_gcs(path)
    write_to_bq(df=data, project_ID=project_ID, project_dataset=project_dataset, table=table)
    spark.stop()


if __name__=="__main__":
    year=2015
    month=2
    execute(year=year, month=month)
