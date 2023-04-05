import requests
#import os
from bs4 import BeautifulSoup
import globalValues

def scrape_amazon_product(product_name):
    url = f"https://www.amazon.com/s?k={product_name}"
    headers = globalValues.get_headers()
    response = requests.get(url, headers=headers)
    print(response)
    product_search_result = BeautifulSoup(response.content, 'html.parser')
    products = []
    for item in product_search_result.select('[data-component-type="s-search-result"]'):
        product = "https://www.amazon.com" + item.select_one('.a-link-normal')['href']
        products.append(product)
    return products



def scrape_amazon_product_multiple_pages(product_name):
    url = f"https://www.amazon.com/s?k={product_name}"
    headers = globalValues.get_headers()
    response = requests.get(url, headers=headers)
    print(response)
    soup = BeautifulSoup(response.content, 'html.parser')
    page_numbers = soup.find_all('span', {'class': 's-pagination-item s-pagination-disabled'})
    total_pages = int(page_numbers[-1].text.strip())
    products = []
    #print(total_pages)
    if total_pages > 1:
        for pg_num in range(1,total_pages):
            #print(len(products))
            url = f"https://www.amazon.com/s?k={product_name}&page={pg_num}"
            next_page_response = requests.get(url, headers=headers)
            next_page = BeautifulSoup(response.content, 'html.parser')
            for item in next_page.select('[data-component-type="s-search-result"]'):
                product = "https://www.amazon.com" + item.select_one('.a-link-normal')['href']
                products.append(product)
    else:
        for item in soup.select('[data-component-type="s-search-result"]'):
            product = "https://www.amazon.com" + item.select_one('.a-link-normal')['href']
            products.append(product)

    final_products=[]
    for i in range(0,len(products)-1):
        query = product_name.replace(" ","-").lower()
        if query in products[i].lower():
            final_products.append(products[i])

    return final_products


'''x = scrape_amazon_product("iphone 13")
y=[]
for i in range(0,len(x)-1):
    query = "Iphone 13".replace(" ","-").lower()
    if query in x[i].lower():
        y.append(x[i])
print("true links : ",len(y))'''

#print(len(scrape_amazon_product("iphone 13")))
'''d={"yes":0, "no":0}
for i in scrape_amazon_product("iphone 13"):
    query = "iphone 13".replace(" ","-")
    print(query)
    if query.lower() not in i.lower():
        d["no"] += 1
    else:
        d["yes"] += 1
print(d)'''