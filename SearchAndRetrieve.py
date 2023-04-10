from bs4 import BeautifulSoup as bs
import requests
from requests_html import HTMLSession
import time
import GlobalValues
import ConnectDatabase as db

#importing the amazon scrape code to main file
from ScrapeAmazon import * 
from ScrapeFlipkart import *

session = HTMLSession()
headers = GlobalValues.get_headers()

def equalize_product_links(amazon_products_links,flipkart_products_links):
    #taking same amount of links from both webpages
    print(f"Amazon Links Before: {len(amazon_products_links)}, Flipkart Links Before: {len(flipkart_products_links)}")
    if amazon_products_links is not None and flipkart_products_links is not None:
        if len(amazon_products_links) < len(flipkart_products_links):
            flipkart_products_links = flipkart_products_links[:len(amazon_products_links)]
        elif len(amazon_products_links) > len(flipkart_products_links):
            amazon_products_links = amazon_products_links[:len(flipkart_products_links)]
    print(f"Amazon Links After: {len(amazon_products_links)}, Flipkart Links After: {len(flipkart_products_links)}")
    return amazon_products_links,flipkart_products_links

def get_idividual_amazon_product_details(amazon_products_links):
    #accessing individual product links and scraping data
    print("Getting Amazon Product Details")
    amazon_products = []
    for amazon_url in amazon_products_links:
        amazon_product = {}
        #accessing individual page
        amazon_product["productUrl"] = amazon_url
        #print(amazon_url)
        amazon_response = requests.get(amazon_url, headers=headers)
        amazon_page = bs(amazon_response.content,"html.parser")

        #getting details original price, discount price, product title, comments
        amazon_prod_title = amazon_page.find("span", attrs={"id":"productTitle"})
        if amazon_prod_title is not None:    
            amazon_product["title"] = amazon_prod_title.text.strip()
        else:
            amazon_prod_title = amazon_page.find("span", attrs={"id":"prologueProductTitle"})
            if amazon_prod_title is not None:
                amazon_product["title"] = amazon_prod_title.text.strip()
            else:
                amazon_product["title"] = "No product title in two tags"
        #print("product : ",amazon_prod_title)

        amazon_original_price = amazon_page.find("span", attrs={"class":"a-text-price"})
        if amazon_original_price is not None:
            amazon_original_price = amazon_original_price.text.strip()
            amazon_product["originalPrice"] = amazon_original_price.split("$")[1].replace(",","")
            amazon_product["originalPrice"] = float(amazon_product["originalPrice"])
        else:
            amazon_original_price_2 = amazon_page.find("span", attrs={"class":"a-price-whole"})
            if amazon_original_price_2 is not None:
                amazon_original_price_2 = amazon_original_price_2.text.strip()
                amazon_product["originalPrice"] = amazon_original_price_2.replace(",","")
                amazon_product["originalPrice"] = float(amazon_product["originalPrice"])
            else:
                amazon_product["originalPrice"] = "no original price found in tag"

        amazon_discount_price = amazon_page.find("span", attrs={"class":"priceToPay"})
        if amazon_discount_price is None:
            amazon_product["discountPrice"] = "None"
            #print("No discount")
        else:
            amazon_discount_price = amazon_discount_price.get_text().split("$")[1]
            amazon_product["discountPrice"] = amazon_discount_price.replace(",","")   
            #print("discount price : ",amazon_discount_price)

        amazon_rating = amazon_page.find("span", attrs={"id":"acrCustomerReviewText"})
        if amazon_rating is None:
            amazon_product["rating"] = "None"
            #print("No Rating")
        else:
            amazon_product["rating"] = amazon_rating.text.strip()
            #print("product rating : ",amazon_rating.text.strip())

        #product comments
        comment_list = amazon_page.find_all(class_ = "a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold")
        if comment_list is None:
            amazon_product["comments"] = "None"
            #print("No Comment")
        else:
            prod_comment = []
            for comment in comment_list:
                prod_comment.append(comment.get_text().strip("\n"))
            if prod_comment != []:
                amazon_product["comments"] = prod_comment
            else:
                amazon_product["comments"] = "None"
            #print("AMAZON : ",prod_comment)
        amazon_products.append(amazon_product)
    #print(amazon_products)
    return amazon_products

def get_individual_flipkart_product_details(flipkart_products_links):
    #accessing individual product links and scraping data
    print("Getting Flipkart Product Details")
    flipkart_products = []
    for flipkart_url in flipkart_products_links:
        flipkart_product = {}
        #accessing individual page
        flipkart_product["productUrl"] = flipkart_url
        #print(flipkart_url)    
        flipkart_response = requests.get(flipkart_url, headers=headers)
        flipkart_page = bs(flipkart_response.content,"html.parser")

        #getting details original price, discount price, product title, comments
        flipkart_prod_title = flipkart_page.find("span", attrs={"class":"B_NuCI"})
        if flipkart_prod_title is not None:
            flipkart_product["title"] = flipkart_prod_title.text.strip()
        else:
            flipkart_product["title"] = "No title"
        #print("product : ",flipkart_prod_title)

        flipkart_original_price = flipkart_page.find("div", attrs={"class":"_3I9_wc _2p6lqe"})
        if flipkart_original_price is not None:
            flipkart_product["originalPrice"] = flipkart_original_price.text.strip()[1::].replace(",","")
            flipkart_product["originalPrice"] = int(flipkart_product["originalPrice"])/60
        else:
             flipkart_product["originalPrice"] = "No price found"
        #print("original price : ",flipkart_original_price)


        flipkart_discount_price = flipkart_page.find("div", attrs={"class":"_30jeq3 _16Jk6d"})
        if flipkart_discount_price is not None:
            flipkart_product["discountPrice"] = flipkart_discount_price.text.strip()[1::].replace(",","")
            flipkart_product["discountPrice"] = int(flipkart_product["discountPrice"])/60
        else:
            flipkart_product["discountPrice"] = "No discount price"
        #print("discount price : ",flipkart_discount_price)

        flipkart_ratings = flipkart_page.find("span", attrs={"class":"_2_R_DZ"})
        if flipkart_ratings is not None:
            flipkart_product["rating"] = flipkart_ratings.get_text().split("&")[0].strip()
        else:
            flipkart_product["rating"] = "None"

        #product comments
        comment_list = flipkart_page.find_all(class_ = "t-ZTKy")
        if comment_list is None:
            flipkart_product["comments"] = "None"
        else:
            prod_comment = []
            for comment in comment_list:
                prod_comment.append(comment.get_text().strip("\n").replace("READ MORE",""))
            #print("FLIPKART : ",prod_comment)
            if prod_comment != []:
                flipkart_product["comments"] = prod_comment
            else:
                flipkart_product["comments"] = "None"
        flipkart_products.append(flipkart_product)
    #print(flipkart_products)
    return flipkart_products

def search_products(search_string):
    #we got all links for the particular product
    amazon_products_links = scrape_amazon_product(search_string)
    flipkart_products_links = scrape_flipkart_product(search_string)

    #equalize product numbers
    if amazon_products_links is not None and flipkart_products_links is not None:
        amazon_products_links, flipkart_products_links = equalize_product_links(amazon_products_links, flipkart_products_links)
        flipkart_details = get_individual_flipkart_product_details(flipkart_products_links)
        amazon_details = get_idividual_amazon_product_details(amazon_products_links)
#########################lets add sentiment analyzer here#########################
        #uploading values to DB        
        db.upload_flipkart_products(flipkart_details)
        db.upload_amazon_products(amazon_details)
    else:
        if flipkart_products_links is not None:
            flipkart_details = get_individual_flipkart_product_details(flipkart_products_links)
            print("Uploading Deatils to DB")
#########################lets add sentiment analyzer here#########################            
            db.upload_flipkart_products(flipkart_details)
        else:
            print("No flipkart products found")

        if amazon_products_links is not None:
            amazon_details = get_idividual_amazon_product_details(amazon_products_links)
#########################lets add sentiment analyzer here#########################
            db.upload_amazon_products(amazon_details)
        else:
            print("No amazon products found")

    #print(amazon_details,"\n\n\n\n\n\n\n\n")
    #print(flipkart_details)

search_products("naruto")