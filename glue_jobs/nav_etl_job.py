import sys
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions

# Initialize Glue context
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Input and output paths
RAW_S3_PATH = "s3://mf-nav-data/raw/"
PROCESSED_S3_PATH = "s3://mf-nav-data/processed/"

# Read raw NAV data
raw_df = (
    spark.read
    .option("header", "true")
    .csv(RAW_S3_PATH)
)

# Basic data cleansing and transformation
processed_df = (
    raw_df
    .dropDuplicates(["fund_id", "nav_date"])
    .withColumn("nav_value", col("nav_value").cast("double"))
    .withColumn("aum", col("aum").cast("double"))
)

# Write processed data in Parquet format, partitioned by nav_date
(
    processed_df
    .write
    .mode("overwrite")
    .partitionBy("nav_date")
    .parquet(PROCESSED_S3_PATH)
)

print("NAV ETL job completed successfully.")
