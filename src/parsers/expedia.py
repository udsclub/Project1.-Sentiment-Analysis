from bs4 import BeautifulSoup
from requests import get as r_get
from string import punctuation, digits
from selenium import webdriver
from json import loads as j_loads
from time import time, sleep
from datetime import datetime

import pandas as pd
import codecs

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

def get_soup(link, headers):
    html = r_get(link, headers)
    soup = BeautifulSoup(html.text, "lxml")
    return soup

# obtaining the list of the largest cities in the USA
wiki = get_soup('https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population', headers)
tables = wiki.findAll('table', {"class":"wikitable sortable"})

cities = []
for row in tables[0].findAll('tr'):
    cells = row.findAll('td')
    if len(cells) > 0:
        city = cells[1].text.encode('utf8').translate(None, punctuation + digits).strip()
        state = cells[2].text.encode('utf8').translate(None, punctuation + digits).strip()
        cities.append(city + (city != state) * (' ' + state))

with codecs.open('parsed_cities.txt', 'rb', 'utf-8') as f:
    parsed_cities = f.read().splitlines()
event_time = datetime.fromtimestamp(time()).strftime(' - %Y-%m-%d %H:%M:%S')
with codecs.open('logs.txt', 'a+', 'utf-8') as f:
    f.write('--------------------------------------------\n')
    f.write('started' + event_time + '\n')

# obtaining lists of hotels and its Ids by cities
hotels = []
new_cities = 0
exp_search = 'https://www.expedia.com/Hotel-Search?#&destination='

for city in cities:
    if city in parsed_cities:
        continue
    # geckodriver.exe can be downloaded here: https://github.com/mozilla/geckodriver/releases
    browser = webdriver.Firefox(executable_path=r'\your path here\geckodriver.exe')
    browser.get(exp_search + city)
    browser.implicitly_wait(5)
    for hotel in browser.find_elements_by_tag_name('article'):
        if hotel.get_attribute('data-hotelid') is None:
            continue
        hotels.append((hotel.get_attribute('data-hotelid'), hotel.find_element_by_xpath('h3').text, city))
    browser.quit()
    with codecs.open('parsed_cities.txt', 'a+', 'utf-8') as f:
        f.write(city.decode('utf8')+'\n')
    new_cities += 1
    if new_cities % 100 == 0:
        print '+100 cities'
    sleep(2)

if len(hotels) > 0:
    hotels_df = pd.DataFrame(hotels, columns = [u'hotelId', u'hotelName', u'cityName'])
    hotels_df.to_csv('hotels.csv', mode='a+', header=False, index=False, encoding='utf-8')
event_time = datetime.fromtimestamp(time()).strftime(' - %Y-%m-%d %H:%M:%S')
with codecs.open('logs.txt', 'a+', 'utf-8') as f:
    f.write('New cities:' + str(new_cities) + '; new hotels:' + str(len(hotels)) + '\n')
    f.write('ended' + event_time + '\n')

# obtaining hotels reviews by hotelId
source = 'https://www.expedia.com/ugc/urs/api/hotelreviews/hotel/{}/?_type=json&start={}&items={}&categoryFilter=&languageFilter=en&searchTerm=&sortBy=&languageSort=en&expweb.activityId=6115a5e6-a1b8-4666-9ed0-59ad63798bd2&pageName=page.Hotels.Infosite.Information&origin=Expedia&caller=Expedia&guid=a47aaa1445c94618bf3fc5bf12a43ff8&includeRatingsOnly=false&jsonpCallback=art&_=1486478852279'

hotel_ids = ['239659', '97974']
# hotel_ids = pd.read_csv('hotels.csv').drop_duplicates()
# hotel_ids = hotel_ids['hotelId'].unique()

with codecs.open('parsed_hotels.txt', 'rb', 'utf-8') as f:
    parsed_hotels = f.read().splitlines()
event_time = datetime.fromtimestamp(time()).strftime(' - %Y-%m-%d %H:%M:%S')
with codecs.open('logs.txt', 'a+', 'utf-8') as f:
    f.write('--------------------------------------------\n')
    f.write('started gathering of reviews' + event_time + '\n')

new_hotels = 0
new_reviews = 0
cols_to_remain = [u'hotelId', u'contentLocale', u'isRecommended', u'isUnverified', u'ratingOverall',
                  u'reviewSubmissionTime', u'title', u'reviewText', u'totalPositiveFeedbacks', u'totalThanks']

for h_id in hotel_ids[:100]:
    if str(h_id) in parsed_hotels:
        continue

    reviews = []
    reviews_raw = []
    start = 0
    items = 10

    while True:
        temp = r_get(source.format(h_id, start, items), headers)
        if temp.status_code != 200:
            with codecs.open('errors_hotels.txt', 'a+', 'utf-8') as f:
                f.write(str(h_id) + str(start) + '\n')
                break
        temp = j_loads(temp.content[4:-2])
        if not temp[u'reviewDetails'][u'numberOfReviewsInThisPage']:
            break
        reviews += temp[u'reviewDetails'][u'reviewCollection']['review']
        reviews_raw.append(temp)
        start += 10
        sleep(1)

    if len(reviews) > 0:
        reviews_df = pd.DataFrame(reviews)[cols_to_remain]
        reviews_df.to_csv('reviews.csv', mode='a+', header=False, index=False, encoding='utf-8')
        with codecs.open('reviews_rav.txt', 'a+', 'utf-8') as f:
            for review in reviews_raw:
                f.write('%s\n' % review)

    with codecs.open('parsed_hotels.txt', 'a+', 'utf-8') as f:
        f.write(str(h_id) + '\n')
    new_hotels += 1
    new_reviews += len(reviews)

    if new_hotels % 10 == 0:
        event_time = datetime.fromtimestamp(time()).strftime(' - %Y-%m-%d %H:%M:%S')
        with codecs.open('logs.txt', 'a+', 'utf-8') as f:
            f.write('+10 hotels' + event_time + '\n')
    sleep(2)

event_time = datetime.fromtimestamp(time()).strftime(' - %Y-%m-%d %H:%M:%S')
with codecs.open('logs.txt', 'a+', 'utf-8') as f:
    f.write('New hotels:' + str(new_hotels) + '; new reviews:' + str(new_reviews) + '\n')
    f.write('ended gathering of reviews' + event_time + '\n')
