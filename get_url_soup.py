from requests import get
from bs4 import BeautifulSoup

def get_url_soup(url):
    return BeautifulSoup(get(url).content, 'html.parser')