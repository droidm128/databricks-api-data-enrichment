# Databricks notebook source
# COMMAND ----------
# MAGIC %run ./constants

# COMMAND ----------
# MAGIC %md 
# MAGIC # Parameters Initialization

# COMMAND ----------
dbutils.widgets.text(InputJobParameters.INPUT_DATA_PATH, "/Workspace/Shared/test-data/sample_data.csv", "")
dbutils.widgets.text(InputJobParameters.API_URL, "droidm128-databricks-api-data-enrichment.westus.azurecontainer.io:5000/test", "")
dbutils.widgets.text(InputJobParameters.PARALLELISM, "3", "")
dbutils.widgets.text(InputJobParameters.RATE_PER_EXECUTOR_PER_SECOND, "10", "")

input_data_path = dbutils.widgets.get(InputJobParameters.INPUT_DATA_PATH)
api_url = dbutils.widgets.get(InputJobParameters.API_URL)
rate_per_executor_per_second = int(dbutils.widgets.get(InputJobParameters.RATE_PER_EXECUTOR_PER_SECOND))
parallelism = int(dbutils.widgets.get(InputJobParameters.PARALLELISM))

print(f"{input_data_path=}")
print(f"{api_url=}")
print(f"{parallelism=}")
print(f"{rate_per_executor_per_second=}")

# COMMAND ----------
# MAGIC %md 
# MAGIC # Read input data

# COMMAND ----------

original_df = spark.read.option("header", True).schema(INPUT_DATA_SCHEMA).format("csv").load(f"file://{input_data_path}")

# COMMAND ----------
# MAGIC %md 
# MAGIC # Define API Enrichment function

# COMMAND ----------
import requests
import traceback
import pandas as pd
from typing import Iterator
from pyspark.sql.functions import pandas_udf
from pyrate_limiter import Duration, Limiter, Rate, BucketFullException

def get_person_information(login: str, limiter: Limiter) -> pd.DataFrame:
    """Query the API with the given login and return user info as a Pandas Data Frame. Handles errors and returns details."""
    response = None
    try:
        limiter.try_acquire("endpoint")
        response = requests.get(f"http://{api_url}", params={"login": login})
        response.raise_for_status() 
        response_body = response.json() 
        return pd.DataFrame([{
            "response_status_code": str(response.status_code),
            "exception": None,
            "response_body": str(response_body),
            "login": login,
            "first_name": response_body.get("first_name"),
            "last_name": response_body.get("last_name"),
            "email": response_body.get("email"),
            "username": response_body.get("username"),
            "address": response_body.get("address"),
            "phone": response_body.get("phone")
        }])
    except:
        exception = traceback.format_exc()
        return pd.DataFrame([{
            "response_status_code": str(response.status_code) if response is not None else None,
            "exception": exception,
            "response_body": str(response.content) if response is not None else None,
            "login": login,
            "first_name": None,
            "last_name": None,
            "email": None,
            "username": None,
            "address": None,
            "phone": None
        }])

# COMMAND ----------
# MAGIC %md 
# MAGIC # Enrich data using the API

# COMMAND ----------
#This function is instantiated multiple times across the cluster (one per Spark executor), so we first instantiate our rate limiter. This function will execute on each worker core.
def enrich_person_information(itr: Iterator[pd.DataFrame]) -> Iterator[pd.DataFrame]:
    rate = Rate(rate_per_executor_per_second, Duration.SECOND)
    limiter = Limiter(rate,raise_when_fail=False,max_delay=10000)
    for pdf in itr:
        df = pd.DataFrame(columns=API_COLUMNS)
        for _, row in pdf.iterrows():
            df = pd.concat([df,get_person_information(row["login"], limiter)], ignore_index=True)
        yield df

enriched_df = (
    original_df.repartition(parallelism)
    .mapInPandas(enrich_person_information, schema=API_RESPONSE_SCHEMA)
)

result_df=original_df.join(enriched_df, on="login", how="left")
result_df.write.mode("overwrite").format("delta").saveAsTable("hive_metastore.default.test_enriched_data") #replace with your desired catalog.schema.table
