import requests
from bs4 import BeautifulSoup
import GlobalValues

headers = GlobalValues.get_headers()

#function to scrape the first page
def scrape_flipkart_product(product_name):
    url = f"https://www.flipkart.com/search?q={product_name}"
    try:
        response = requests.get(url, headers=headers)
    except Exception:
        print("Could not search in Flipkart")
        return None
    if response.ok:
        print("Flipkart Success")
        products = []
        #getting individual product links
        product_search_result = BeautifulSoup(response.content, 'html.parser')
        if product_search_result.select('._4ddWXP') != []:
            for item in product_search_result.select('._4ddWXP'):
                product = "https://www.flipkart.com" + item.select_one('.s1Q9rs')['href']
                products.append(product)
        elif product_search_result.select('._2kHMtA') != []:
            for item in product_search_result.select('._2kHMtA'):
                product = "https://www.flipkart.com" + item.select_one('._1fQZEK')['href']
                products.append(product)
        else:
            return None
        return products
    else:
        print("Flipkart Response Not OK")
        return None
    
#function to get individual product details
def get_individual_flipkart_product_details(flipkart_products_links):
    #accessing individual product links and scraping data
    print("Getting Flipkart Product Details")
    flipkart_products = []
    for flipkart_url in flipkart_products_links:
        flipkart_product = {}
        #accessing individual page
        flipkart_product["productUrl"] = flipkart_url
        #print(flipkart_url)

        try:
            flipkart_response = requests.get(flipkart_url, headers=headers)
        except Exception:
            print("One product not loaded from Flipkart")
            continue

        flipkart_page = BeautifulSoup(flipkart_response.content,"html.parser")

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
            flipkart_product["rating"] = None

        #product comments
        comment_list = flipkart_page.find_all(class_ = "t-ZTKy")
        if comment_list is None:
            flipkart_product["comments"] = None
        else:
            prod_comment = []
            for comment in comment_list:
                prod_comment.append(comment.get_text().strip("\n").replace("READ MORE",""))
            #print("FLIPKART : ",prod_comment)
            if prod_comment != []:
                flipkart_product["comments"] = prod_comment
            else:
                flipkart_product["comments"] = None
        flipkart_products.append(flipkart_product)
    #print(flipkart_products)
    return flipkart_products