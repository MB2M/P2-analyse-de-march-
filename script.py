import requests
import nums_from_string
from bs4 import BeautifulSoup
import urllib.request
from slugify import slugify


def get_soup(url):
    response = requests.get(url, 'html_parser')
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def get_categories(url):
    soup = get_soup(url)
    categories = soup.find('ul', class_="nav-list").li.ul
    categoriesList = []
    for category in categories.find_all("li"):
        categoriesList.append({'name': category.text.strip(), 'link': urlRoot + category.a['href']})
    return categoriesList


def get_book_informations(url):
    soup = get_soup(url)
    books = [url]
    product_info = {}
    for row in soup.find(class_="table table-striped").find_all('tr'):
        product_info[row.th.text] = row.td.text
    books.append(product_info['UPC'])
    books.append(soup.find(class_="product_main").h1.text)
    books.append(product_info['Price (incl. tax)'].strip('Â'))
    books.append(product_info['Price (excl. tax)'].strip('Â'))
    books.append(nums_from_string.get_nums(product_info['Availability'])[0])
    if soup.find("div", id={'product_description'}):
        books.append(soup.find("div", id={'product_description'}).find_next_sibling("p").text)
    books.append(soup.find('li', class_='active').find_previous_sibling('li').a.text)
    books.append(soup.find('p', class_='star-rating')['class'][1])
    books.append(urlRoot + soup.find('div', class_="item active").img['src'].replace('../', ""))
    return books


def get_total_pages(url):
    soup = get_soup(url)
    pagination = soup.find('ul', class_='pager')
    if pagination is not None:
        total_pages = int(pagination.li.text.strip().replace('Page 1 of ', ''))
    else:
        total_pages = 1
    return total_pages


def add_list_to_csv(file, book_list, separator=","):
    row = ""
    for element in book_list:
        row += str(element) + separator
    row = row.strip(separator) + "\n"
    file.write(row)


def extract_book_to_csv(url, count=1):
    book_information = get_book_informations(url)
    add_list_to_csv(csvfile, book_information, "|")
    save_img(book_information[-1], 'img/' + slugify(book_information[2] + "_" + str(count), separator='_') + '.jpg')


def extract_category_to_csv(url_category):
        count = 1
        total_pages = get_total_pages(url_category)
        for i in range(total_pages):
            url = url_category
            if i != 0:
                url = url.replace('index.html', 'page-' + str(i + 1) + '.html')
            soup = get_soup(url)
            for article in soup.ol.find_all('article'):
                url_book = urlRoot + 'catalogue/' + article.div.a['href'].replace('../', '')
                extract_book_to_csv(url_book, count)
                count += 1


def save_img(url, filename):
    urllib.request.urlretrieve(url, filename)


urlRoot = 'http://books.toscrape.com/'
categories = get_categories(urlRoot)

for category in categories:
    with open('csv/' + category['name'] + '.csv', 'w', newline='', encoding="utf-8") as csvfile:
        csvfile.write('product_page_url|universal_product_code|title|price_including_tax|price_excluding_tax|'
                      'number_available|product_description|category|review_rating|image_url\n')
        extract_category_to_csv(category['link'])

