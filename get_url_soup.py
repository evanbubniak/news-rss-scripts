from requests import get
from bs4 import BeautifulSoup
from requests_html import HTMLSession

def soup(html):
    return BeautifulSoup(html, 'html.parser')

def get_url_soup(url):
    return soup(get(url).content)

def get_requests_html_soup(url):
    session = HTMLSession()
    resp = session.get(url)
    resp.html.render(timeout=8000)
    return soup(resp.content)