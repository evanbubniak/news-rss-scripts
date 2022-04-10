#!/usr/bin/env python3
from article import RSSArticle
from convert_and_print_rss import convert_and_print_rss
from get_url_soup import get_url_soup

class MSNArticle(RSSArticle):
    def retrieve_content(self):
        url_suffixes = ["&amp;srcref=rss", "?srcref=rss"]
        for url_suffix in url_suffixes:
            if url_suffix in self.url:
                self.url = self.url.replace(url_suffix, "")
        soup = get_url_soup(self.url)
        body_tag = soup.find("div", class_="articlecontent")
        if body_tag:
            text = "<p>" + "</p><p>".join([text_tag.getText() for text_tag in body_tag.find_all("p")]) + "</p>"
        else:
            text = "(Article text missing, please visit the article URL.)"
        self.content = text

base_url = "https://rss.msn.com/"
default_feed_name: str = "de-de/"

convert_and_print_rss(base_url, default_feed_name, MSNArticle)