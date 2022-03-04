#!/usr/bin/env python3
from article import RSSArticle
from convert_and_print_rss import convert_and_print_rss
from get_url_soup import get_url_soup
from bs4 import Tag

def tag_contains_article_body(tag: Tag) -> bool:
    return tag.attrs.get("id") == "content-to-read" or "gallery__content" in tag.get_attribute_list("class") or "body-article" in tag.get_attribute_list("class")

class CorriereDellaSeraArticle(RSSArticle):
    def retrieve_content(self):
        soup = get_url_soup(self.url)
        body_tag = soup.find(tag_contains_article_body)
        if body_tag:
            text = "<p>" + "</p><p>".join([text_tag.decode_contents() for text_tag in body_tag.find_all("div", class_ = "content")]) + "</p>"
        else:
            text = "(Article text missing, please visit the article URL.)"
        self.content = text

base_url: str = ""
default_feed_name: str = "http://xml2.corriereobjects.it/rss/homepage.xml"

convert_and_print_rss(base_url, default_feed_name, CorriereDellaSeraArticle)