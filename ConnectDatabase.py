import pprint
from pymongo import MongoClient
import GlobalValues

#establish database connection
def get_database_connection():
    connection_string = GlobalValues.get_connection_password()
    client = MongoClient(connection_string)
    if client is not None:
        print("MongoDB connected")
        database = client.ProductDatabase
        if database is not None:
            print("Database Connected")
            return database
        else:
            print("Database connection error")
    else:
        print("MongoDB connection error")
        return None
    
def upload_flipkart_products(flipkart_products):
    db = get_database_connection()
    flipkart_db = db.FlipkartProducts
    if flipkart_db is not None:
        print("Flipkart collection connected")
        flag = flipkart_db.insert_many(flipkart_products)
        print(f"Flipkart Produts Uploaded to DB: {flag.acknowledged}")
    else:
        print("Flipkart collection connection error")

def upload_amazon_products(amazon_products):
    db = get_database_connection()
    amazon_db = db.AmazonProducts
    if amazon_db is not None:
        print("Amazon collection connected")
        flag = amazon_db.insert_many(amazon_products)
        print(f"Amazon Produts Uploaded to DB: {flag.acknowledged}")
    else:
        print("Amazon collection connection error")
