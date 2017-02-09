import requests
from bs4 import BeautifulSoup
import re
import time
import csv


def get_soup(link):
    html = requests.get(link)
    soup = BeautifulSoup(html.text, "lxml")
    return soup


def parse(soup):
    r = []
    for review in soup.findAll("div", {"class": "col-sm-24 col-md-15 col-lg-16 review-content"}):
        r.append([str(review.find("a", {"class": "stars"}).i)[21], review.bdi.p.text])
    return r


def preproccess(text):
    return text.replace("|", ";").replace("\r", '').replace("\n", '')


def save(reviews):
    with open("reviews_iherb_all.csv", "a") as f:
        for review in reviews:
            f.write(review[0] + "|" + preproccess(review[1]) + "\n")


def save_products(products):
    with open("reviews_iherb_products.csv", "a") as f:
        for i in products:
            f.write(i + ",")

n_pages = 296
source = "http://www.iherb.com/c/Categories?p={}&disc=true&sr=1&noi=192"

t = time.time()
products_list = []
stop = False

for i in range(1, n_pages+1):
    soup = get_soup(source.format(i))
    for item in soup.findAll("div", {"class":"product ga-product col-xs-12 col-sm-12 col-md-8 col-lg-6"}):
        if item.find("a", {"class": "rating-count"}):
            products_list.append(item.a["href"].replace("/pr/","/r/"))
        else:
            stop = True
            break
    if stop:
        print("Page {} is the last".format(i))
        break
    if i % 20 == 0:
        elapsed_time = time.time() - t
        print("{}: {:.2f}".format(i, elapsed_time))

elapsed_time = time.time() - t
print("Products have been collected: {:.2f}".format(elapsed_time))

product_source = "{}/?p={}&revl=en"

r = []
products = []
t = time.time()
sum_reviews = 0

with open("reviews_iherb_products.csv", "r") as f:
    reader = csv.reader(f)
    for i in reader:
        already_parsed = [item.strip() for item in i]

products_list = [i for i in products_list if i not in already_parsed]
print(len(products_list))
print(len(already_parsed))

for num, s in enumerate(products_list):
    products.append(s)
    soup = get_soup(product_source.format(s, 1))
    try:
        total = int(re.search(r"(\d+) total", str(soup.find("p", {"class": "display-items-L"}))).group(1))
    except:
        continue

    r.extend(parse(soup))
    for p in range(2, total // 10 + (total % 10 > 0) + 1):
        soup = get_soup(product_source.format(s, p))
        r.extend(parse(soup))
    if len(r) > 10000:
        sum_reviews += len(r)
        elapsed_time = time.time() - t
        print("{}: {:.2f}".format(sum_reviews, elapsed_time))
        save(r)
        save_products(products)
        products = []
        r = []
