import requests
from bs4 import BeautifulSoup

# Function to get data from each product
def get_product_data(product):
    product_url_element = product.find('a', class_='a-link-normal')
    product_url = 'https://www.amazon.in' + product_url_element['href'] if product_url_element else 'Not available'
    
    product_name_element = product.find('span', class_='a-size-medium a-color-base a-text-normal')
    product_name = product_name_element.text.strip() if product_name_element else 'Not available'
    
    product_price_element = product.find('span', class_='a-price-whole')
    product_price = product_price_element.text.strip() if product_price_element else 'Not available'
    
    product_rating_element = product.find('span', class_='a-icon-alt')
    product_rating = product_rating_element.text.strip() if product_rating_element else 'Not available'
    
    product_reviews_element = product.find('span', class_='a-size-base')
    product_reviews = product_reviews_element.text.strip() if product_reviews_element else 'Not available'
    
    return [product_url, product_name, product_price, product_rating, product_reviews]

# Scrape data from multiple pages
base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2"
data_list = []

for page_num in range(1, 21):  # scrape at least 20 pages
    url = f"{base_url}{page_num}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.find_all('div', {'data-component-type': 's-search-result'})

    for product in products:
        data = get_product_data(product)
        data_list.append(data)

# Print the data
for data in data_list:
    print("Product URL:", data[0])
    print("Product Name:", data[1])
    print("Product Price:", data[2])
    print("Rating:", data[3])
    print("Number of Reviews:", data[4])
    print("-----------------------------------------------------")
