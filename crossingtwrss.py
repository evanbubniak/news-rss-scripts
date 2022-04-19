#!/usr/bin/env python3
from article import RSSArticle
from convert_and_print_rss import convert_and_print_rss
from get_url_soup import get_requests_html_soup

class CrossingTWArticle(RSSArticle):
    def retrieve_content(self):
        soup = get_requests_html_soup(self.url)
        body_tag = soup.find("article").find("div", class_="trackSection")
        if body_tag:
            text = "<p>" + "</p><p>".join([text_tag.getText() for text_tag in body_tag.find_all(["p", "blockquote"])]) + "</p>"
        else:
            text = "(Article text missing, please visit the article URL.)"
        self.content = text

base_url = "https://crossing.cw.com.tw/rss"
default_feed_name: str =  ""

convert_and_print_rss(base_url, default_feed_name, CrossingTWArticle, use_threads=False)