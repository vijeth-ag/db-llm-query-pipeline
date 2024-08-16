from pymilvus import connections, utility, db, MilvusClient, FieldSchema, CollectionSchema, Collection, DataType

DB_NAME = "mongo_vec_db"
COLLECTION_NAME = "mongo_vec_coll"

def init_db():
    connections.connect(host="milvus-standalone", port=19530)

    databases = db.list_database()

    if DB_NAME not in databases:
        print("db created")
        database = db.create_database(DB_NAME)
        

    client = MilvusClient(
        uri="http://milvus-standalone:19530",
        db_name=DB_NAME
    )

    collections = client.list_collections()
    print("existing collec",collections)

    if COLLECTION_NAME not in collections:
        id_field = FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, description="primary id")
        embedding_field = FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384, description="vector")
        text_field = FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=2000, description="text")
        
        schema = CollectionSchema(fields=[id_field, embedding_field,text_field], auto_id=True, enable_dynamic_field=True, description="desc of a collection")

        client.create_collection(
            collection_name=COLLECTION_NAME,
            schema = schema,
            dimension=5
        )
        print("collection created")
        


    index_params = MilvusClient.prepare_index_params()

    index_params.add_index(
        field_name="embedding",
        metric_type="COSINE",
        index_type="IVF_FLAT",
        index_name="vector_index",
        params={ "nlist": 128 }
    )

    client.create_index(
        collection_name=COLLECTION_NAME,
        index_params=index_params
    )

    client.load_collection(
        collection_name=COLLECTION_NAME,
    )



def store_embeddings(vec, text):
    client = MilvusClient(
    uri="http://milvus-standalone:19530",
    db_name=DB_NAME
    )

    data=[{"embedding": vec, "text": text}]
    
    res = client.insert(
        collection_name=COLLECTION_NAME,
        data=data
    )

    

