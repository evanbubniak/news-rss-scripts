#!/usr/bin/env python3
from article import RSSArticle
from convert_and_print_rss import convert_and_print_rss
from get_url_soup import get_url_soup

class UDNArticle(RSSArticle):
    def retrieve_content(self):
        soup = get_url_soup(self.url)
        body_tag = soup.find("article")
        if body_tag:
            main_texts = [text_tag.decode_contents() for text_tag in body_tag.find_all("p")]
            text = "<p>" + "</p><p>".join(main_texts) + "</p>"
        else:
            text = "(Article text missing, please visit the article URL.)"
        self.content = text.replace("\n", "")

base_url = ""
default_feed_name = "https://global.udn.com/rss/news/1020/8662"

convert_and_print_rss(base_url, default_feed_name, UDNArticle)