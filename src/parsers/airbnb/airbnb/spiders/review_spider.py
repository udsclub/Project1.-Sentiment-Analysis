import scrapy
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
import json
import csv, time



headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}


class ReviewSpider(scrapy.Spider):
    name = "review"
    
    
    def start_requests(self):

        start_url = "https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population"
        yield scrapy.Request(start_url, self.extract_cities)


    def extract_cities(self, response):

        cities = response.css('td:nth-child(2)').extract()
        try:
            for city in cities:
                soup = BeautifulSoup(city, 'html.parser')
                city = soup.find('a')
                try:
                    city_name = city['title'].split(',')[0]
                    url = 'http://www.airbnb.com/s/{0}'.format(city_name)
                    tag = getattr(self, 'tag', None)
                    if tag is not None:
                        url = url + 'tag/' + tag
                    yield scrapy.Request(url, self.parse_city_page)
                except TypeError:
                    pass
        except ValueError:
            pass

    
    def parse_city_page(self, response):

        next_page = response.css('li.next a::attr(href)').extract_first()        
        room_urls = response.css('.listingCardWrapper_1804ev2 a::attr(href)').extract()
        
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, self.parse_city_page)
        
        if len(room_urls)>0:
            for room_url in room_urls:
                room_url = response.urljoin(room_url)
                yield scrapy.Request(room_url, self.parse_room_page)


    def parse_room_page(self, response):

        room_id = response.url.strip('https://www.airbnb.com/rooms/')
        review_selector = ".review-wrapper > div  h4 span"
        next_page = response.css(review_selector).extract_first()  

        
        soup = BeautifulSoup(next_page, 'html.parser')
        try:
            number_of_review = int(soup.get_text().split(" Reviews")[0])
            url_reviewes = "https://ru.airbnb.com/api/v2/reviews?key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=UAH&locale=ru&listing_id={0}&role=guest&_format=for_p3&_limit={1}&_offset=0&_order=language".format(room_id, number_of_review)
            yield scrapy.Request(url_reviewes, self.parse_review)
        except ValueError:
            number_of_review = None

    def parse_review(self, response):

        reviewes = json.loads(response.body)['reviews']
        for review in reviewes:
            yield {'review': review['comments'],
                    'listing_id': review['review_vote']['listing_id'],
                    'review_id': review['review_vote']['review_id'],
                    'date': review['localized_date'],
                    'up_vote':review['review_vote']['upvote_count'],
                    'down_vote':review['review_vote']['downvote_count']
                    }




            