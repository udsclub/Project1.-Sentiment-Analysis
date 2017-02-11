import requests
from bs4 import BeautifulSoup
import csv
import concurrent.futures
import datetime
import queue

root = "http://www.lovehoney.co.uk"
start_link = "http://www.lovehoney.co.uk/community/reviews/"


def get_page_content(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')


class Review:
    def __init__(self, rate, text, source=root, category="sex-goods"):
        self.rate = rate
        self.text = text
        self.source = source
        self.category = category


def parse_reviews(url, q, page_num, max_page):
    if page_num == (max_page - 1):
        q.put('STOP')
    else:
        page = get_page_content(url)
        trs = page.select('table tbody tr')
        for tr in trs:
            review_link = tr.find_all('a')[2].get('href')
            review_page = get_page_content(root+review_link)
            text = review_page.find('div', {'class': 'review-content'}).getText()
            rate = round(int((tr.find_all('td')[4].find('span').getText()[:2])) / 2)
            review = Review(rate, text)
            q.put(review)


def write_reviews(q):
    review_count = 0
    with open("lovehoney.csv", "a") as f:
        writer = csv.DictWriter(f, ['rating', 'review', 'source', 'category'])
        while True:
            review = q.get()
            if review == 'STOP':
                log('Done')
                return
            writer.writerow({
                'rating': review.rate,
                'review': review.text,
                'source': review.source,
                'category': review.category
            })
            review_count += 1
            if review_count % 100 == 0:
                log('Total reviews: ' + str(review_count))
            q.task_done()
    log('Finished')


def current_time():
    return datetime.datetime.now()


def log(msg):
    print(str(current_time()) + ' : ' + msg)


link = start_link
page_num = 1
q = queue.Queue(-1)
max_page = 18137
with concurrent.futures.ThreadPoolExecutor(10) as executor:
    executor.submit(write_reviews, q)
    while page_num < max_page:
        url = start_link + 'page-' + str(page_num)
        executor.submit(parse_reviews, url, q, page_num, max_page)
        page_num += 1
executor.shutdown()
