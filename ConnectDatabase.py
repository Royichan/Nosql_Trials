import pprint
from pymongo import MongoClient
import GlobalValues
from datetime import datetime

#establish database connection
def get_database_connection():
    connection_string = GlobalValues.get_connection_password()
    try:
        client = MongoClient(connection_string)
        client.admin.command('ping')
        print("MongoDB connected")
        database = client.ProductDatabase
        try:
            print("Database Connected")
            return database
        except Exception as e:
            print(f"####Database connection error####")
            return None
    except Exception as e:
        print(f"####MongoDB connection error####")
        return None
    
def upload_flipkart_products(flipkart_products):
    db = get_database_connection()
    if db is not None:
        try:
            flipkart_db = db.FlipkartProducts
            print("Flipkart collection connected")
            flag = flipkart_db.insert_many(flipkart_products)
            print(f"Flipkart Produts Uploaded to DB: {flag.acknowledged}")
            return flag.inserted_ids
        except Exception as e:
            print(f"####Flipkart collection connection error####")
            return None
    else:
        return None
        

def upload_amazon_products(amazon_products):
    db = get_database_connection()
    if db is not None:
        try:
            amazon_db = db.AmazonProducts
            print("Amazon collection connected")
            flag = amazon_db.insert_many(amazon_products)
            print(f"Amazon Produts Uploaded to DB: {flag.acknowledged}")
            return flag.inserted_ids
        except Exception as e:
            print(f"####Amazon collection connection error####")
            return None
    else:
        return None

def insert_history(history):
    db = get_database_connection()
    if db is not None:
        try:
            history_db = db.History
            print("History collection connected")
            flag = history_db.insert_one(history)
            print(f"Uploaded history data to DB: {flag.acknowledged}")
        except Exception as e:
            print(f"####History collection connection error while insertion####")
    else:
        return None

def get_history(search_string):
    db = get_database_connection()
    if db is not None:
        try:
            history_db = db.History
            print("History collection connected")
            count = history_db.count_documents({"keyword":search_string,"date":str(datetime.today().date())})
            if count > 0 and count == 2:
                history = history_db.find({"keyword":search_string,"date":str(datetime.today().date())})
                return True,history
            else:
                return False,"None"
        except Exception as e:
            print(f"####History collection connection error while retrival####")
            return False,"None"
    else:
        return False,"None"
        
def get_flipkart(Ids):
    db = get_database_connection()
    if db is not None:
        flipkart = []
        try:
            flipkart_db = db.FlipkartProducts
            print("Flipkart collection connected")
            for id in Ids:
                try:
                    prod = flipkart_db.find_one(id)
                    flipkart.append(prod)
                except Exception:
                    print("####One flipkart product not retrieved from DB####")
                    continue
            return flipkart
        except Exception as e:
            print(f"####Flipkart collection connection error####")
            return None
    else:
        return None

def get_amazon(Ids):
    db = get_database_connection()
    if db is not None:
        amazon = []
        try:
            amazon_db = db.AmazonProducts
            print("Amazon collection connected")
            for id in Ids:
                try:
                    prod = amazon_db.find_one(id)
                    amazon.append(prod)
                except Exception:
                    print("####One amazon product not retrieved from DB####")
                    continue
            return amazon
        except Exception as e:
            print(f"####Amazon collection connection error####")
            return None
    else:
        return None