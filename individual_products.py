from bs4 import BeautifulSoup as bs
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import requests
from requests_html import HTMLSession
import time
import globalValues

#importing the amazon scrape code to main file
from amazon_link_scrape import * 
from flipcart_link_scrape import *

session = HTMLSession()
headers = globalValues.get_headers()

#we got all links for the particular product
amazon_products_links = scrape_amazon_product("Samsung Galaxy")
#we got all links for flipcart products
flipkart_products_links = scrape_flipkart_product("headset")

#accessing individual product links and scraping data
for amazon_url in amazon_products_links:
    #accessing individual page
    amazon_response = requests.get(amazon_url, headers=headers)
    amazon_page = bs(amazon_response.content,"html.parser")

    #getting details original price, discount price, product title, comments
    amazon_prod_title = amazon_page.find("span", attrs={"id":"productTitle"}).text.strip()
    print("product : ",amazon_prod_title)

    amazon_original_price = amazon_page.find("span", attrs={"class":"a-text-price"}).text.strip()
    print("original price : ",amazon_original_price.split("$")[1])

    amazon_discount_price = amazon_page.find("span", attrs={"class":"priceToPay"})
    if amazon_discount_price is None:
        print("No discount")
    else:
        amazon_discount_price = amazon_discount_price.get_text().split("$")[1]   
        print("discount price : ",amazon_discount_price)

    amazon_rating = amazon_page.find("span", attrs={"id":"acrCustomerReviewText"}).text.strip()
    print("product rating : ",amazon_rating)

    comment_list = amazon_page.find_all(class_ = "a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold")
    prod_comment = []
    for comment in comment_list:
        prod_comment.append(comment.get_text().strip("\n"))
    print("AMAZON : ",prod_comment)

#accessing individual product links and scraping data
for flipkart_url in flipkart_products_links:
    #accessing individual page    
    flipkart_response = requests.get(flipkart_url, headers=headers)
    flipkart_page = bs(flipkart_response.content,"html.parser")

    #getting details original price, discount price, product title, comments
    flipkart_prod_title = flipkart_page.find("span", attrs={"class":"B_NuCI"}).text.strip()
    print("product : ",flipkart_prod_title)

    flipkart_original_price = flipkart_page.find("div", attrs={"class":"_3I9_wc _2p6lqe"}).text.strip()
    print("original price : ",flipkart_original_price)

    flipkart_discount_price = flipkart_page.find("div", attrs={"class":"_30jeq3 _16Jk6d"}).text.strip()
    print("discount price : ",flipkart_discount_price)


    comment_list = flipkart_page.find_all(class_ = "t-ZTKy")
    prod_comment = []
    for comment in comment_list:
        prod_comment.append(comment.get_text().strip("\n"))
    print("FLIPKART : ",prod_comment)