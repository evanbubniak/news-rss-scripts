#!/usr/bin/env python3
import requests
from xml.etree.ElementTree import ElementTree, fromstring
from yahoonewsjp_api import YahooNewsArticle
from sys import argv
from io import StringIO

URL_SUFFIX = "?source=rss"
base_url = "https://news.yahoo.co.jp/rss/"
target_url = base_url + argv[1]

response = requests.get(target_url)
root = fromstring(response.content)

def get_item_link(item):
    link = item.find("link")
    return "" if link is None else link.text[:-1*len(URL_SUFFIX)]

def get_item_title(item):
    title = item.find("title")
    return "" if title is None else title.text

channel = root.find("channel")
if channel:
    items = channel.findall("item")
    articles = [YahooNewsArticle(digest_url = get_item_link(item), short_title = get_item_title(item)) for item in items]
    for item, article in zip(items, articles):
        link = item.find("link")
        description = item.find("description")
        if link is not None:
            link.text = article.get_url()
        if description is not None:
            description.text = article.get_content(incl_date = False)

    etree = ElementTree(element=root)
    output_str = StringIO("")
    etree.write(output_str, encoding="unicode", xml_declaration=True)
    print(output_str.getvalue())