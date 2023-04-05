import requests
from bs4 import BeautifulSoup

def scrape_flipkart_product(product_name):
    url = f"https://www.flipkart.com/search?q={product_name}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    print(response)
    products = []
    product_search_result = BeautifulSoup(response.content, 'html.parser')
    for item in product_search_result.select('._4ddWXP'):
        product = "https://www.flipkart.com" + item.select_one('.s1Q9rs')['href']
        products.append(product)
    return products


def scrape_flipkart_product_multiple_pages(product_name):
    url = f"https://www.flipkart.com/search?q={product_name}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "Accept-Encoding":"gzip, deflate",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
        "DNT":"1",
        "Connection":"close",
        "Upgrade-Insecure-Requests":"1"
    }
    response = requests.get(url, headers=headers)
    print(response)
    soup = BeautifulSoup(response.content, 'html.parser')
    page_numbers = soup.find_all('a', {'class': 'ge-49M'})
    total_pages = int(page_numbers[-1].text.strip())
    #print(total_pages)
    products = []
    if total_pages > 1:
        for pg_num in range(1,total_pages):
            #print(len(products))
            url = f"https://www.flipkart.com/search?q={product_name}&page={pg_num}"
            next_page_response = requests.get(url, headers=headers)
            next_page = BeautifulSoup(response.content, 'html.parser')
            for item in soup.select('._2kHMtA'):
                product = "https://www.flipkart.com" + item.select_one('._1fQZEK')['href']
                products.append(product)
    else:
        for item in soup.select('._2kHMtA'):
            product = "https://www.flipkart.com" + item.select_one('._1fQZEK')['href']
            products.append(product)

    final_products=[]
    for i in range(0,len(products)-1):
        query = product_name.replace(" ","-").lower()
        if query in products[i].lower():
            final_products.append(products[i])
    
    return final_products

'''x = scrape_flipkart_product("iphone 13")
x.append("")
y=[]
for i in range(0,len(x)-1):
    query = "Iphone 13".replace(" ","-").lower()
    if query in x[i].lower():
        y.append(x[i])
print("true links : ",len(y))'''

#for i in scrape_flipkart_product("iphone 13"):
#    print(i)

'''d={"yes":0, "no":0}
for i in scrape_flipkart_product("iphone 13"):
    query = "iphone 13".replace(" ","-")
    print(query)
    if query.lower() not in i.lower():
        d["no"] += 1
    else:
        d["yes"] += 1
print(d)'''