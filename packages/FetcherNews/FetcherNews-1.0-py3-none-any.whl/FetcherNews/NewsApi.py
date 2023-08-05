from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

URL = "https://news.google.com/rss"




class News:
    CLIENT = urlopen(URL)
    XML_PAGE = CLIENT.read()
    soup_page= soup(XML_PAGE,"xml")
    news_list = soup_page.findAll("item")
    for news in news_list:
        print(news.title.text)
        print(news.pubDate.text)
        print('-'*60)