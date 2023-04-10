import requests
from bs4 import BeautifulSoup
import GlobalValues

#function to scrape the first page
def scrape_flipkart_product(product_name):
    url = f"https://www.flipkart.com/search?q={product_name}"
    headers = GlobalValues.get_headers()
    response = requests.get(url, headers=headers)
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