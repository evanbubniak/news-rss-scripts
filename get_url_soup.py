from requests import get
from bs4 import BeautifulSoup
from requests_html import HTMLSession

ua_headers = { "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1" }

def soup(html):
    return BeautifulSoup(html, 'html.parser')

def get_url_soup(url, headers = ua_headers):
    return soup(get(url, headers).content)

def get_requests_html_soup(url):
    session = HTMLSession()
    resp = session.get(url)
    resp.html.render(timeout=8000)
    return soup(resp.content)