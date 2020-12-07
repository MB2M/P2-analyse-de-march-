import requests
import nums_from_string
from bs4 import BeautifulSoup


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


def add_list_to_csv(file, book_list, separator=","):
    row = ""
    for element in book_list:
        row += str(element) + separator
    row = row.strip(separator) + "\n"
    file.write(row)


def extract_category_to_csv(url_category, name="default"):
    soup = get_soup(url_category)
    total_pages = "1"
    pagination = soup.find('ul', class_='pager')
    if pagination is not None:
        total_pages = pagination.li.text.strip().replace('Page 1 of ', '')

    with open('csv/' + name + '.csv', 'w', newline='', encoding="utf-8") as csvfile:
        csvfile.write('product_page_url|universal_product_code|title|price_including_tax|price_excluding_tax|'
                      'number_available|product_description|category|review_rating|image_url\n')
        for i in range(int(total_pages)):
            url = url_category
            if i != 0:
                url = url.replace('index.html', 'page-' + str(i + 1) + '.html')
            soup = get_soup(url)

            for article in soup.ol.find_all('article'):
                url_book = urlRoot + 'catalogue/' + article.div.a['href'].replace('../', '')
                book_information = get_book_informations(url_book)
                add_list_to_csv(csvfile, book_information, "|")


urlRoot = 'http://books.toscrape.com/'
categories = get_categories(urlRoot)
for category in categories:
    extract_category_to_csv(category['link'], name=category["name"])
