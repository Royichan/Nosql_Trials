import requests
from bs4 import BeautifulSoup
import GlobalValues

headers = GlobalValues.get_headers()

#function to scrape the first page
def scrape_amazon_product(product_name):
    url = f"https://www.amazon.com/s?k={product_name}"
    try:
        response = requests.get(url, headers=headers)
    except Exception:
        print("Could not search in Amazon")
        return None
    
    if response.ok:
        print("Amazon Success")
        products = []
        #getting individual product links
        product_search_result = BeautifulSoup(response.content, 'html.parser')
        for item in product_search_result.select('div[data-component-type="s-search-result"]'):
            product = "https://www.amazon.com" + item.select_one('.a-link-normal')['href']
            products.append(product)
        if products != []:
            return products
        else:
            return None
    else:
        print("Amazon Response Not OK")
        return None

#function to get individual product details    
def get_idividual_amazon_product_details(amazon_products_links):
    #accessing individual product links and scraping data
    print("Getting Amazon Product Details")
    amazon_products = []
    for amazon_url in amazon_products_links:
        amazon_product = {}
        #accessing individual page
        amazon_product["productUrl"] = amazon_url
        #print(amazon_url)
        
        try:
            amazon_response = requests.get(amazon_url, headers=headers)
        except Exception:
            print("One product not loaded from Amazon")
            continue
        amazon_page = BeautifulSoup(amazon_response.content,"html.parser")

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
                amazon_product["originalPrice"] = "No price found"

        amazon_discount_price = amazon_page.find("span", attrs={"class":"priceToPay"})
        if amazon_discount_price is None:
            amazon_product["discountPrice"] = "No discount price"
            #print("No discount")
        else:
            amazon_discount_price = amazon_discount_price.get_text().split("$")[1]
            amazon_product["discountPrice"] = float(amazon_discount_price.replace(",",""))   
            #print("discount price : ",amazon_discount_price)

        amazon_rating = amazon_page.find("span", attrs={"id":"acrCustomerReviewText"})
        if amazon_rating is None:
            amazon_product["rating"] = None
            #print("No Rating")
        else:
            amazon_product["rating"] = amazon_rating.text.strip()
            #print("product rating : ",amazon_rating.text.strip())

        #product comments
        comment_list = amazon_page.find_all(class_ = "a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold")
        if comment_list is None:
            amazon_product["comments"] = None
            #print("No Comment")
        else:
            prod_comment = []
            for comment in comment_list:
                prod_comment.append(comment.get_text().strip("\n"))
            if prod_comment != []:
                amazon_product["comments"] = prod_comment
            else:
                amazon_product["comments"] = None
            #print("AMAZON : ",prod_comment)
        amazon_products.append(amazon_product)
    #print(amazon_products)
    return amazon_products