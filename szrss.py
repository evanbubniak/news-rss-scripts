#!/usr/bin/env python3
from typing import Optional
from article import Article, RSSArticle
from sys import argv
from convert_and_print_rss import convert_and_print_rss
from get_url_soup import get_url_soup
from bs4 import Tag


def is_article_text(tag: Tag) -> bool:
    return "css-136yie6" in tag.get_attribute_list("class") or "css-13wylk3" in tag.get_attribute_list("class") or "sz-article-body__paragraph--reduced" in tag.get_attribute_list("class") or (tag.name == "h3" and not tag.attrs.get("class"))

class SueddeutscheZeitungArticle(RSSArticle):
    def retrieve_content(self):
        soup = get_url_soup(self.url)
        body_tag = soup.find("article")
        if body_tag:
            text = "<p>" + "</p><p>".join([text_tag.getText() for text_tag in body_tag.find_all(is_article_text)]) + "</p>"
        else:
            text = "(Article text missing, please visit the article URL.)"
        self.content = text

base_url = ""
feed_name: str = argv[1] if len(argv) >= 2 else "https://rss.sueddeutsche.de/rss/Topthemen"
article_limit: Optional[int] = int(argv[2]) if len(argv) >= 3 else None
target_url = base_url + feed_name

def get_item_link(item) -> str:
    link = item.find("link")
    return "" if link is None else link.text

def get_item_title(item) -> str:
    title = item.find("title")
    return "" if title is None else title.text

def item_to_article(item) -> Article:
    return SueddeutscheZeitungArticle(url = get_item_link(item), title = get_item_title(item), use_threads=False)

convert_and_print_rss(target_url, article_limit, item_to_article)