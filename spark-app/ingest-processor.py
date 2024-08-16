# spark job to observe kafka topic and process incoming data

import json
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr
from vector.embedding import encode
from vector.vec_db import init_db
from vector.vec_db import store_embeddings

# from functools import wraps
# from pymilvus import connections, utility, db, MilvusClient, FieldSchema, CollectionSchema, Collection, DataType
# from openai import OpenAI
# import time

model_id = "sentence-transformers/all-MiniLM-L6-v2"

init_db()

# Initialize Spark session
spark = SparkSession.builder \
    .appName("db-llm-query-spark") \
    .config("spark.driver.memory", "10g") \
    .config("spark.executor.pyspark.memory", "2g") \
    .config("spark.driver.maxResultSize", "2g") \
    .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0') \
    .getOrCreate()

# spark.sparkContext.setLogLevel("WARN")
# set spark log level to error onlu
spark.sparkContext.setLogLevel("ERROR")


print("spark:",spark)

# Read raw data from Kafka
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe", "mongo-topic-.people_db.people_coll") \
    .option("startingOffsets", "earliest") \
    .load()

# kafka_string_df = kafka_df.selectExpr("CAST(value AS STRING)")

# # Process data
def process(data):
    # print("processing data", type(data))
    process_row(data)


def process_row(row):
    row_values = row.asDict().values()
    byte_arrays = [item for item in row_values if isinstance(item, bytearray)]

    documents = []
    for byte_array in byte_arrays:
        json_str = byte_array.decode('utf-8')
        parsed_json = json.loads(json_str)
        payload_str = parsed_json.get('payload', None)
        
        # If payload is present, parse it to get the actual MongoDB document
        if payload_str:
            mongo_doc = json.loads(payload_str)
            documents.append(mongo_doc)


    # Output the extracted MongoDB documents
    for i, doc in enumerate(documents, start=1):
        full_document = doc.get('fullDocument')
        if full_document:            
            embedded_doc = encode(str(full_document))
            # print(f"embedded_doc: {embedded_doc}")
            print("...............storing.....")
            store_embeddings(embedded_doc, str(full_document))
            
           


query = kafka_df.writeStream.foreach(process).start()

query.awaitTermination()