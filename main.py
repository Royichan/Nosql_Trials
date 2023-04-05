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
amazon_products_links = scrape_amazon_product("Samsung Galaxy")
#we got all links for flipcart products
flipkart_products_links = scrape_flipkart_product("headset")

#print(amazon_products_links)
#print(flipkart_products_links)

#scraping Amazon Product details using Beautiful soup


session = HTMLSession()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.31",
    "Accept-Encoding":"gzip, deflate",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
    "DNT":"1",
    "Connection":"close",
    "Upgrade-Insecure-Requests":"1"
}

'''
for amazon_url in amazon_products_links:
    amazon_response = requests.get(amazon_url, headers=headers)
    amazon_page = bs(amazon_response.content,"html.parser")

    amazon_prod_title = amazon_page.find("span", attrs={"id":"productTitle"}).text.strip()
    print(amazon_prod_title)

    amazon_original_price = amazon_page.find("span", attrs={"class":"a-text-price"}).text.strip()
    print(amazon_original_price.split("$")[1])

    amazon_discount_price = amazon_page.find("span", attrs={"class":"priceToPay"})
    if amazon_discount_price is None:
        print("No discount")
    else:
        amazon_discount_price = amazon_discount_price.get_text().split("$")[1]   
        print(amazon_discount_price)

    amazon_rating = amazon_page.find("span", attrs={"id":"acrCustomerReviewText"}).text.strip()

    comment_list = amazon_page.find_all(class_ = "a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold")
    prod_comment = []
    for comment in comment_list:
        prod_comment.append(comment.get_text().strip("\n"))
    #print("AMAZON : ",prod_comment)
'''
 
for flipkart_url in flipkart_products_links:    
    flipkart_response = requests.get(flipkart_url, headers=headers)
    flipkart_page = bs(flipkart_response.content,"html.parser")

    flipkart_prod_title = flipkart_page.find("span", attrs={"class":"B_NuCI"}).text.strip()
    print(flipkart_prod_title)

    flipkart_original_price = flipkart_page.find("div", attrs={"class":"_3I9_wc _2p6lqe"}).text.strip()
    print(flipkart_original_price)

    flipkart_discount_price = flipkart_page.find("div", attrs={"class":"_30jeq3 _16Jk6d"}).text.strip()
    print(flipkart_discount_price)


    comment_list = flipkart_page.find_all(class_ = "t-ZTKy")
    prod_comment = []
    for comment in comment_list:
        prod_comment.append(comment.get_text().strip("\n"))
    print("FLIPKART : ",prod_comment)   
    
    #print(f"Flipkart : {flipkart_prod_title}\nAmazon : {amazon_prod_title}\n")
