#!/usr/bin/env python3
from article import RSSArticle
from convert_and_print_rss import convert_and_print_rss
from get_url_soup import get_url_soup
from bs4 import Tag

def is_article_text(tag: Tag) -> bool:
    return "css-136yie6" in tag.get_attribute_list("class") or "css-13wylk3" in tag.get_attribute_list("class") \
                or "sz-article-body__paragraph--reduced" in tag.get_attribute_list("class") \
                or (tag.name == "h3" and not tag.attrs.get("class")) \
                or (tag.name == "li" and tag.parent.parent.parent.parent.name == "article") \
                or ("tik3-event-item-content-text" in tag.parent.get_attribute_list("class"))

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
default_feed_name = "https://rss.sueddeutsche.de/rss/Topthemen"

convert_and_print_rss(base_url, default_feed_name, SueddeutscheZeitungArticle)