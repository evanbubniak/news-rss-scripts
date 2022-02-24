#!/usr/bin/env python3
from typing import Optional
import requests
from xml.etree.ElementTree import ElementTree, fromstring, Element
from article import Article
from get_url_soup import get_url_soup
from sys import argv
from io import StringIO
import threading
from tqdm import tqdm

class DRNewsArticle(Article):
    def __init__(self, feed_name = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.feed_name = feed_name
        self.thread = threading.Thread(target=self.retrieve_content)
        self.thread.start()

    def get_content(self):
        if not self.content:
            self.thread.join()
        return self.content

    def retrieve_content(self):
        soup = get_url_soup(self.url)
        if self.feed_name == "senestenyt":
            body_classname = "hydra-latest-news-page-short-news__body"
        else:
            body_classname = "dre-article-body"
        body_tag = soup.find("div", class_=body_classname)

        if body_tag:
            text = "<p>" + "</p><p>".join([text_tag.getText() for text_tag in body_tag.find_all(class_ ="dre-speech")]) + "</p>"
        else:
            text = "(Article text missing, please visit the article URL.)"
        self.content = text



feed_name: str = argv[1] if len(argv) >= 2 else "senestenyt"
article_limit: Optional[int] = int(argv[2]) if len(argv) >= 3 else None
base_url = "https://www.dr.dk/nyheder/service/feeds/"
target_url = base_url + feed_name

response = requests.get(target_url)
root = fromstring(response.content)

def get_item_link(item):
    link = item.find("link")
    return "" if link is None else link.text

def get_item_title(item):
    title = item.find("title")
    return "" if title is None else title.text

channel = root.find("channel")
if channel:
    items = channel.findall("item")
    articles = [DRNewsArticle(feed_name = feed_name, url = get_item_link(item), short_title = get_item_title(item)) for item in items]
    if article_limit is not None:
        articles = articles[:article_limit]
    for item, article in tqdm(zip(items, articles), total = len(items)):
        link = item.find("link")
        description = item.find("description")
        if link is not None:
            link.text = article.get_url()

        if description is None:
            description = Element("description")
            item.append(description)

        description.text = article.get_content()

    etree = ElementTree(element=root)
    output_str = StringIO("")
    etree.write(output_str, encoding="unicode", xml_declaration=True)
    print(output_str.getvalue())