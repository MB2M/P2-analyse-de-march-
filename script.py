import csv
import requests
import nums_from_string
from bs4 import BeautifulSoup


url = 'http://books.toscrape.com/catalogue/the-past-never-ends_942/index.html'

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

bookTitle = soup.find(class_="product_main").h1.text

productInformations = {}
for row in soup.find(class_="table table-striped").find_all('tr'):
    productInformations[row.th.text] = row.td.text

bookUPC = productInformations['UPC']
bookTTC = productInformations['Price (incl. tax)'].strip('Â')
bookHT = productInformations['Price (excl. tax)'].strip('Â')
bookStock = productInformations['Availability']
bookStockNumber = nums_from_string.get_nums(bookStock)[0]
bookDesciption = soup.find(id={'product_description'}).next_sibling
print(bookUPC,",",bookTTC,",",bookHT,",",bookStock,',',bookStockNumber,',',bookDesciption)

# with open('books.csv', 'w', newline='') as csvfile:
#     csvfile.write('product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,'
#                   'number_available,product_description,category,review_rating,image_url')
#
#     csvfile.write(soup.title.text.strip())
