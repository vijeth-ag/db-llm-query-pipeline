import json
import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr

# Initialize Spark session
spark = SparkSession.builder \
    .appName("db-llm-query-spark") \
    .config("spark.driver.memory", "10g") \
    .config("spark.executor.pyspark.memory", "2g") \
    .config("spark.driver.maxResultSize", "2g") \
    .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0') \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

print("spark:", spark)

# Read raw data from Kafka
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe", "mongo-topic-.people_db.people_coll") \
    .option("startingOffsets", "earliest") \
    .load()

# Function to send data to the API
def send_to_api(documents):
    print(len(documents))
    url = "http://db-service:5123/store"  # Replace with your API endpoint
    headers = {"Content-Type": "application/json"}
    
    for doc in documents:
        # Convert the document to JSON string
        payload = json.dumps({
            "data": str(doc)
        })
        
        # Send the document to the API
        response = requests.post(url, data=payload, headers=headers)
        
        if response.status_code == 200:
            print(f"Successfully stored document: {doc}")
        else:
            print(f"Failed to store document: {doc}, Status Code: {response.status_code}, Error: {response.text}")

# Process function to extract and send documents to the API
def process_row(df_spark, epoch_id):

    df_spark.show()

    # Parse Kafka message value as string and extract relevant fields
    df_spark = df_spark.selectExpr("CAST(value AS STRING) as json_str")
    df_spark.show(truncate=False)

    # Parse JSON and extract payloads
    df_spark = df_spark.withColumn("parsed_json", expr("from_json(json_str, 'payload STRING')"))
    df_spark = df_spark.withColumn("payload", col("parsed_json.payload"))


    # Extract and collect the MongoDB documents
    df_spark = df_spark.withColumn("mongo_doc", expr("from_json(payload, 'fullDocument MAP<STRING,STRING>')"))
    documents = df_spark.select("mongo_doc").collect()

    # Convert Row objects to dictionaries for sending to the API
    documents_dicts = [row.mongo_doc.asDict() for row in documents]

    # Send the documents to the API
    send_to_api(documents_dicts)

# Apply process_row to each micro-batch using foreachBatch
query = kafka_df.writeStream.foreachBatch(process_row).start()

query.awaitTermination()
