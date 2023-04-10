import requests
from bs4 import BeautifulSoup
import GlobalValues

#function to scrape the first page
def scrape_amazon_product(product_name):
    url = f"https://www.amazon.com/s?k={product_name}"
    headers = GlobalValues.get_headers()
    response = requests.get(url, headers=headers)
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