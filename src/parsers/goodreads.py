from bs4 import BeautifulSoup
from langdetect import detect
import csv, time
import concurrent.futures
import requests, codecs

base_url = "https://www.goodreads.com"
headers = { 'User-Agent'  :  'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}

mark = {
    "did not like it": 1,
    "it was ok": 2,
    "liked it": 3,
    "really liked it": 4,
    "it was amazing": 5
}

def get_worksheet_list(url,headers):
    worksheet_list = []
    soup = BeautifulSoup(requests.get(url,headers=headers).text,'html.parser')
    for a in soup.find_all('a', {'class':'bookTitle'}, href=True):
        worksheet_list.append(a['href'])
    return (worksheet_list)

def get_reviews_from_worksheet(url,base_url):
    for i in range(1,11):
        url_to_go = ''
        mass = []
        url_to_go = base_url + url+"?hide_last_page=true&amp;page="+str(i)+"&authenticity_token=yBdCFPbuC7wLkbMmWq1YHHU9rsh4lGrhlDIWZspx41t3Vf3VXAWDPjKYsPxvceCRnikBwAyPewJNLoaS24LTEg%3D%3D"
        resp = requests.get(url_to_go,headers=headers).text
        resp = resp[27:]
        resp = resp[:len(resp)-3]
        try:
            soup = codecs.decode(resp, 'unicode-escape')

            soup = BeautifulSoup(soup,'html.parser')

            for div in soup.find_all('div', {'class':'review'}):
                string=(div.find('div', {'class':'reviewHeader uitext stacked'}).text)

                if string.find("rated it")>0:
                    review=(div.find('span', {'class':'readable'}).text)
                    try:
                        if detect(review)=="en":
                            review = review.replace("\n","")
                            review = review.replace("...more","")
                            review = review.replace("(view spoiler)[","")
                            review = review.replace("(hide spoiler)]","")

                            marks=mark.get(div.find('span', {'size':'15x15'}).text)

                            mass.append ([marks,review,"Goodreads"])
                    except Exception:
                        print ("Strange text")
            with open("goodreads.csv", "a") as f:
                writer = csv.DictWriter(f, ['rating','review','source'])
                for j in range(len(mass)):
                    writer.writerow({
                        'rating': mass[j][0],
                        'review': mass[j][1],
                        'source': str(mass[j][2])
                    })
        except Exception:
            print ("Can't decode")


if __name__ == "__main__":
    max_page = 108
    page_num = 1
    start_time = time.time()
    parse_url = "/list/show/1938.What_To_Read_Next?page="
    for page_number in range(31,35):
        print(page_number)
        worksheet_list=get_worksheet_list(base_url+parse_url+str(page_number),headers)
        for worksheet in worksheet_list:
            print(page_number,worksheet)
            get_reviews_from_worksheet(worksheet,base_url)
    print (time.time()-start_time)
