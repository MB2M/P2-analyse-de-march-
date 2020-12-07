import csv
import requests
import nums_from_string
from bs4 import BeautifulSoup

urlRoot = 'http://books.toscrape.com/'
response = requests.get(urlRoot, 'html_parser')
soup = BeautifulSoup(response.text, 'html.parser')

categories = soup.find('ul', class_="nav-list").li.ul
categoriesList = []
for category in categories.find_all("li"):
    categoriesList.append({'name': category.text.strip(), 'link': urlRoot + category.a['href']})

for category in categoriesList:
    urlCategory = category['link']
    response = requests.get(urlCategory)
    soup = BeautifulSoup(response.text, 'html.parser')

    pagination = soup.find('ul', class_='pager')
    TotalPages = "1"
    if pagination != None:
        TotalPages = pagination.li.text.strip().replace('Page 1 of ', '')

    with open(category['name'] + '.csv', 'w', newline='', encoding="utf-8") as csvfile:
        csvfile.write('product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,'
                      'number_available,product_description,category,review_rating,image_url\n')

        for i in range(int(TotalPages)):
            if i != 0:
                urlCategory = urlCategory.replace('index.html', 'page-' + str(i+1) + '.html')
            response = requests.get(urlCategory)
            soup = BeautifulSoup(response.text, 'html.parser')

            for article in soup.ol.find_all('article'):
                # Récupération des éléments sur la page d'un produit

                url = urlRoot + 'catalogue/' + article.div.a['href'].replace('../', '')
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')

                bookTitle = soup.find(class_="product_main").h1.text

                productInformations = {}
                for row in soup.find(class_="table table-striped").find_all('tr'):
                    productInformations[row.th.text] = row.td.text

                bookUPC = productInformations['UPC']
                bookTTC = productInformations['Price (incl. tax)'].strip('Â')
                bookHT = productInformations['Price (excl. tax)'].strip('Â')
                bookStock = nums_from_string.get_nums(productInformations['Availability'])[0]
                if soup.find("div", id={'product_description'}):
                    bookDescription = soup.find("div", id={'product_description'}).find_next_sibling("p").text

                bookTitle = soup.find(class_="product_main").h1.text
                bookCategory = soup.find('li', class_='active').find_previous_sibling('li').a.text
                bookRating = soup.find('p', class_='star-rating')['class'][1]
                bookImageUrl = urlRoot + soup.find('div', class_="item active").img['src'].replace('../', "")
                #print(url + "," + bookUPC + "," + bookTitle + "," + bookTTC + "," + bookHT + "," + str(bookStock) + "," + bookDescription + "," + bookCategory + "," + bookRating + "," + bookImageUrl)
                csvfile.write(url + "," + bookUPC + "," + bookTitle + "," + bookTTC + "," + bookHT + "," + str(bookStock) + "," + bookDescription + "," + bookCategory + "," + bookRating + "," + bookImageUrl + '\n')
