from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
import globalValues

#establish database connection
def mongo_connection():
    connection_string = globalValues.get_connection_password()
    client = MongoClient(connection_string)

    dbs = client.list_database_names()
    test_db = client.MongoProject
    collections = test_db.list_collection_names()
    print(dbs)
    print(collections)

mongo_connection()

