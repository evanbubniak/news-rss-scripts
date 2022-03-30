#!/usr/bin/env python3
from article import RSSArticle
from convert_and_print_rss import convert_and_print_rss
from get_url_soup import get_url_soup

class DRNewsArticle(RSSArticle):
    def retrieve_content(self):
        soup = get_url_soup(self.url)
        for body_tag_classname in ["dre-article-body", "hydra-latest-news-page-short-news__body"]:
            body_tag = soup.find("div", class_=body_tag_classname)
            if body_tag:
                break

        if body_tag:
            text = "<p>" + "</p><p>".join([text_tag.getText() for text_tag in body_tag.find_all(class_ ="dre-speech")]) + "</p>"
        else:
            text = "(Article text missing, please visit the article URL.)"
        self.content = text

base_url = "https://www.dr.dk/nyheder/service/feeds/"
default_feed_name: str = "senestenyt"

convert_and_print_rss(base_url, default_feed_name, DRNewsArticle)