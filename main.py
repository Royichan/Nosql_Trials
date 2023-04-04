from bs4 import BeautifulSoup as bs
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import requests
from requests_html import HTMLSession
import time

#importing the amazon scrape code to main file
from amazon_link_scrape import * 
from flipcart_link_scrape import *

#we got all links for the particular product
amazon_products_links = scrape_amazon_product("iphone 13")
#we got all links for flipcart products
flipkart_products_links = scrape_flipkart_product("iphone 13")

#print(amazon_products_links)
#print(flipkart_products_links)

#scraping Amazon Product details using Beautiful soup


session = HTMLSession()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.37",
    "Accept-Encoding":"gzip, deflate",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
    "DNT":"1",
    "Connection":"close",
    "Upgrade-Insecure-Requests":"1"
}

for amazon_url, flipkart_url in zip(amazon_products_links, flipkart_products_links):
    amazon_response = requests.get(amazon_url, headers=headers)
    amazon_page = bs(amazon_response.content,"html.parser")
    amazon_prod_title = amazon_page.find("span", attrs={"id":"productTitle"}).text.strip()
    
    flipkart_response = requests.get(flipkart_url, headers=headers)
    flipkart_page = bs(flipkart_response.content,"html.parser")
    flipkart_prod_title = flipkart_page.find("span", attrs={"class":"B_NuCI"}).text.strip()   
    
    print(f"Flipkart : {flipkart_prod_title}\nAmazon : {amazon_prod_title}\n")