import requests
from bs4 import BeautifulSoup
import csv

# Function to get data from each product
def get_product_data(product):
    product_url = 'https://www.amazon.in' + product.find('a', class_='a-link-normal')['href']
    product_name = product.find('span', class_='a-size-medium a-color-base a-text-normal').text.strip()
    product_price = product.find('span', class_='a-price-whole').text.strip()
    product_rating = product.find('span', class_='a-icon-alt').text.strip()
    product_reviews = product.find('span', class_='a-size-base').text.strip()

    product_response = requests.get(product_url, headers=headers)
    product_soup = BeautifulSoup(product_response.text, 'html.parser')

    # Scrape additional data from product page
    product_description = product_soup.find('div', {'id': 'detailBullets_feature_div'})
    if product_description:
        product_description = product_description.get_text(strip=True)
    else:
        product_description = 'Not available'

    asin = product_soup.find(text='ASIN')
    if asin:
        asin = asin.find_next('span').get_text(strip=True)
    else:
        asin = 'Not available'

    manufacturer = product_soup.find(text='Manufacturer')
    if manufacturer:
        manufacturer = manufacturer.find_next('span').get_text(strip=True)
    else:
        manufacturer = 'Not available'

    return [product_url, product_name, product_price, product_rating, product_reviews, asin, product_description, manufacturer]


# Scrape data from multiple pages
base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"
data_list = []

with open('output.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews', 'ASIN', 'Product Description', 'Manufacturer'])

    for page_num in range(1, 85):  
        url = f"{base_url}{page_num}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.find_all('div', {'data-component-type': 's-search-result'})

        for product in products:
            data = get_product_data(product)
            writer.writerow(data)
            print(f"Data for {data[1]} written to file.")
