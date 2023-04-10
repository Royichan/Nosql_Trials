import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def get_headers():
    headers = {} 
    headers["User-Agent"] = os.environ.get("User-Agent")
    headers["Accept-Encoding"] = os.environ.get("Accept-Encoding")
    headers["Accept"] = os.environ.get("Accept")
    headers["DNT"] = os.environ.get("DNT")
    headers["Connection"] = os.environ.get("Connection")
    headers["Upgrade-Insecure-Requests"] = os.environ.get("Upgrade-Insecure-Requests")
    return headers

def get_connection_password():
    password = os.environ.get("MONGODB_PWD")
    connection_string = f"mongodb+srv://mymongo:{password}@mycluster.kclzuiw.mongodb.net/?retryWrites=true&w=majority"
    return connection_string