import requests
from bs4 import BeautifulSoup
import re
import codecs
import pandas as pd
import time
import datetime

def get_soup(link):
    html = requests.get(link)
    soup = BeautifulSoup(html.text, "lxml")
    return soup

source = "https://www.rottentomatoes.com/m/{}/reviews/"
n_movies = 10 # number of movies to go through
i = 0

# load all ids from movies.dat
df = pd.read_csv('movies.dat', sep='\t', encoding = "ISO-8859-1")
df.dropna(inplace=True)
ids = df.rtID.unique()

# load old ids
with codecs.open('parsed.txt', 'r', 'utf-8') as myfile:
    old_ids = myfile.read().splitlines()

# create headers for reviews.tsv
# with codecs.open('reviews.tsv', 'w', 'utf-8') as myfile:
#         myfile.write(u'{}\t{}\t{}\n'.format('title', 'review_text', 'rating'))

# write to log file
ts = time.time()
sttime = datetime.datetime.fromtimestamp(ts).strftime(' - %H:%M:%S')
with codecs.open('logs.txt', 'a+', 'utf-8') as myfile:
    myfile.write('-------------------\n')
    myfile.write('New process started'+sttime+'\n')


for rt_id in ids:

    if rt_id in old_ids:
        continue

    new_ids = []
    soup = get_soup(source.format(rt_id))
    movie_title_subling = soup.find('div', {'class':'bottom_divider'})

    if not movie_title_subling:
        with codecs.open('errors.txt', 'a+', 'utf-8') as myfile:
            myfile.write(source.format(rt_id)+'\n')
        with codecs.open('parsed.txt', 'a+', 'utf-8') as myfile:
            myfile.write(rt_id+'\n')
        continue

    movie_title = movie_title_subling.parent.find('h2').a.string

    for review_container in soup.findAll("div", {"class":"col-xs-16 review_container"}):
        classes = review_container.findAll('div', recursive=False)[0]['class']
        is_rotten = 'rotten' in classes
        is_fresh = 'fresh' in classes

        if not is_rotten and not is_fresh:
            print('that\'s weird! can\'t understand the rating. RT ID is :' + rt_id)
            continue

        the_review = review_container.find('div', {"class":"the_review"})
        text = the_review.string

        if text is None or not text.strip():
            continue

        # append to the end of file
        with codecs.open('reviews.tsv', 'a+', 'utf-8') as myfile:
            myfile.write(u'{}\t{}\t{}\n'.format(movie_title, text, 1 if is_fresh else 0))

        i += 1

        if not i % 100:
            # write to log file
            ts = time.time()
            sttime = datetime.datetime.fromtimestamp(ts).strftime(' - %H:%M:%S')
            with codecs.open('logs.txt', 'a+', 'utf-8') as myfile:
                myfile.write('done with 100 more reviews :)'+sttime+'\n')

    with codecs.open('parsed.txt', 'a+', 'utf-8') as myfile:
        myfile.write(rt_id+'\n')

    n_movies -= 1
    if n_movies == 0: break

# write to log file
with codecs.open('logs.txt', 'a+', 'utf-8') as myfile:
    myfile.write(str(i)+' reviews added\n')
