# Databricks notebook source
from enum import StrEnum

class InputJobParameters(StrEnum):
    INPUT_DATA_PATH = "input_data_path"
    API_URL = "api_url"
    PARALLELISM = "parallelism"
    RATE_PER_EXECUTOR_PER_SECOND = "rate_per_executor_per_second"

INPUT_DATA_SCHEMA = """
    login STRING, 
    sales_channel STRING, 
    number_of_orders_month INT
"""

API_RESPONSE_SCHEMA = """
    response_status_code INT, 
    exception STRING, 
    response_body STRING, 
    login STRING, 
    first_name STRING, 
    last_name STRING, 
    email STRING, 
    username STRING, 
    address STRING, 
    phone STRING
"""

API_COLUMNS = [
    'response_status_code',
    'exception',
    'response_body',
    'login',
    'first_name',
    'last_name',
    'email',
    'username',
    'address',
    'phone'
]
