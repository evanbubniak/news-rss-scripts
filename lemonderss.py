#!/usr/bin/env python3
from article import RSSArticle
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
default_feed_name: str =  "rss/une.xml"

convert_and_print_rss(base_url, default_feed_name, LeMondeArticle)