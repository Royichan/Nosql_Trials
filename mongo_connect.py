from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
load_dotenv(find_dotenv())

#establish database connection
def mongo_connection():
    password = os.environ.get("MONGODB_PWD")

    connection_string = f"mongodb+srv://athish:{password}@cluster0.ouwq2sk.mongodb.net/MongoProject"
    client = MongoClient(connection_string)

    dbs = client.list_database_names()
    test_db = client.MongoProject
    collections = test_db.list_collection_names()
    print(dbs)
    print(collections)

mongo_connection()

