import GlobalValues
import ConnectDatabase as db
import SentimentAnalyzer as snt
from datetime import datetime

#importing the amazon scrape code to main file
import ScrapeAmazon as amzn
import ScrapeFlipkart as flpkt

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

def search_products_in_web(search_string):
    #we got all links for the particular product
    results = {}
    amazon_products_links = amzn.scrape_amazon_product(search_string)
    flipkart_products_links = flpkt.scrape_flipkart_product(search_string)

    #equalize product numbers
    if amazon_products_links is not None and flipkart_products_links is not None:
        amazon_products_links, flipkart_products_links = equalize_product_links(amazon_products_links, flipkart_products_links)
        
    if flipkart_products_links is not None:
        flipkart_details = flpkt.get_individual_flipkart_product_details(flipkart_products_links)
        print("Analyzing Comments For Flipkart")
        for product in flipkart_details:
            product["comments"] = snt.analyze_reviews(product["comments"])
            #print("com : ", product["comments"])
        print("Uploading Flipkart Deatils to DB")           
        flipkart_db_ids = db.upload_flipkart_products(flipkart_details)
        if flipkart_db_ids is not None:
            print("Uploading documents to History DB")
            flipkart_history = {}
            flipkart_history["keyword"] = search_string
            flipkart_history["date"] = str(datetime.today().date())
            flipkart_history["flipkartIds"] = flipkart_db_ids
            history_db_flag = db.insert_history(flipkart_history)
        else:
            print("Not able to upload Flipkart to history")
        results["flipkart"] = flipkart_details 
    else:
        print("No flipkart products found")
        results["flipkart"] = None
        
    if amazon_products_links is not None:
        amazon_details = amzn.get_idividual_amazon_product_details(amazon_products_links)
        print("Analyzing Comments For Amazon")
        for product in amazon_details:
            product["comments"] = snt.analyze_reviews(product["comments"])
            #print("com : ", product["comments"])
        print("Uploading Amazon Deatils to DB")
        amazon_db_ids = db.upload_amazon_products(amazon_details)
        if amazon_db_ids is not None:
            print("Uploading documents to History DB")
            amazon_history = {}
            amazon_history["keyword"] = search_string
            amazon_history["date"] = str(datetime.today().date())
            amazon_history["amazonIds"] = amazon_db_ids
            history_db_flag = db.insert_history(amazon_history)
        else:
            print("Not able to upload Amazon to history")
        results["amazon"] = amazon_details 
    else:
        print("No amazon products found")
        results["amazon"] = None
    return results

#function to search product and upload details
def search_products(search_string):
    print(f"Search Keyword : {search_string}")    
    search_flag,Ids = db.get_history(search_string.lower())
    if search_flag:
        print("Previously Searched Product")
        results = {}
        if Ids[0]["flipkartIds"] != "None":
            #print("yes",Ids[0]["flipkartIds"])
            results["flipkart"] = db.get_flipkart(Ids[0]["flipkartIds"])
        else:
            results["flipkart"] = None
            print("no flip")

        if Ids[1]["amazonIds"] != "None":
            #print("yes",Ids[1]["amazonIds"])
            results["amazon"] = db.get_amazon(Ids[1]["amazonIds"])
        else:
            results["amazon"] = None
            print("no ama")
        #print(results)
        print("Completed Data Retrival from DB")
        return results
    else:
        results = search_products_in_web(search_string.lower())
        #print(results)
        print("Completed Data Retrival from Web")
        return results
        #print(results["flipkart"],"\n\n\n\n\n",results["amazon"])