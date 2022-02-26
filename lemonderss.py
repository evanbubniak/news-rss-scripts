#!/usr/bin/env python3
from typing import Optional
from article import Article, RSSArticle
from sys import argv
from convert_and_print_rss import convert_and_print_rss
from get_url_soup import get_url_soup

class LeMondeArticle(RSSArticle):
    def retrieve_content(self):
        soup = get_url_soup(self.url)
        text_classname = "article__paragraph"
        body_tag = soup.find("article")
        if body_tag:
            text = "<p>" + "</p><p>".join([text_tag.getText() for text_tag in body_tag.find_all(class_ =text_classname)]) + "</p>"
        else:
            text = "(Article text missing, please visit the article URL.)"
        self.content = text

base_url = "https://www.lemonde.fr/"
feed_name: str = argv[1] if len(argv) >= 2 else "rss/une.xml"
article_limit: Optional[int] = int(argv[2]) if len(argv) >= 3 else None
target_url = base_url + feed_name

def get_item_link(item) -> str:
    link = item.find("link")
    return "" if link is None else link.text

def get_item_title(item) -> str:
    title = item.find("title")
    return "" if title is None else title.text

def item_to_article(item) -> Article:
    return LeMondeArticle(url = get_item_link(item), title = get_item_title(item))

convert_and_print_rss(target_url, article_limit, item_to_article)