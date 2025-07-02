# Databricks notebook source

# COMMAND ----------
# MAGIC %md 
# MAGIC # Generate Sample Data

# COMMAND ----------
import csv
from faker import Faker
import random
import os

dbutils.widgets.text("test_data_folder", "2", "")
test_data_folder = dbutils.widgets.get("test_data_folder")
os.makedirs(test_data_folder, exist_ok=True)

fake = Faker()
sales_channels = ['Online', 'Retail', 'Wholesale', 'Direct', 'Partner']
with open(f"{test_data_folder}/sample_data.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['login', 'sales_channel', 'number_of_orders_month'])
    for _ in range(200):
        login = fake.user_name()
        sales_channel = random.choice(sales_channels)
        number_of_orders_month = random.randint(1, 100)
        writer.writerow([login, sales_channel, number_of_orders_month])