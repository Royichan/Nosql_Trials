import pprint
from pymongo import MongoClient
import GlobalValues

#establish database connection
def get_database_connection():
    connection_string = GlobalValues.get_connection_password()
    client = MongoClient(connection_string)
    try:
        client.admin.command('ping')
        print("MongoDB connected")
        database = client.ProductDatabase
        try:
            print("Database Connected")
            return database
        except Exception as e:
            print(f"Database connection error")
            return None
    except Exception as e:
        print(f"MongoDB connection error")
        return None
    
def upload_flipkart_products(flipkart_products):
    db = get_database_connection()
    if db is not None:
        try:
            flipkart_db = db.FlipkartProducts
            print("Flipkart collection connected")
            flag = flipkart_db.insert_many(flipkart_products)
            print(f"Flipkart Produts Uploaded to DB: {flag.acknowledged}")
            return True
        except Exception as e:
            print(f"Flipkart collection connection error")
            return False
        

def upload_amazon_products(amazon_products):
    db = get_database_connection()
    if db is not None:
        try:
            amazon_db = db.AmazonProducts
            print("Amazon collection connected")
            flag = amazon_db.insert_many(amazon_products)
            print(f"Amazon Produts Uploaded to DB: {flag.acknowledged}")
            return True
        except Exception as e:
            print(f"Amazon collection connection error")
            return False