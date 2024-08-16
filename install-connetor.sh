curl -X POST -H "Content-Type: application/json" \
  --data '{
    "name": "mongo-source-connector6",
    "config": {
      "connector.class": "com.mongodb.kafka.connect.MongoSourceConnector",
      "tasks.max": "1",
      "connection.uri": "mongodb://root:password@mongo:27017/people_db?authSource=admin",
      "database": "people_db",
      "collection": "people_coll",
      "topic.prefix": "mongo-topic-",
      "poll.max.batch.size": "1000",
      "poll.await.time.ms": "5000",
      "errors.tolerance": "all",
      "offset.partition.name": "new_partition_name",
      "startup.mode": "copy_existing",
       "change.stream.full.document": "updateLookup"
    }
  }' \
  http://localhost:8083/connectors