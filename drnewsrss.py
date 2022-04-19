#!/usr/bin/env python3
from article import RSSArticle
from convert_and_print_rss import convert_and_print_rss
from get_url_soup import get_url_soup
from bs4 import Tag

def convert_tag_to_text(tag: Tag) -> str:
    if "dre-list" in tag.get_attribute_list("class"):
        return "</p><p>".join(listitem_tag.getText() for listitem_tag in tag.find_all("li"))
    else:
        text_classname="dre-speech"
        if text_classname in tag.get_attribute_list("class"):
            return tag.getText()
        return "</p><p>".join([text_tag.getText() for text_tag in tag.find_all(class_=text_classname)])

class DRNewsArticle(RSSArticle):
    def retrieve_content(self):
        soup = get_url_soup(self.url)
        
        if "/seneste/" in self.url or "/seneste-sport/" in self.url:
            body_classname = "hydra-latest-news-page-short-news__body"
        else:
            body_classname = "dre-article-body"
        body_tag = soup.find("div", class_=body_classname)

        if body_tag:
            text = "<p>" + "</p><p>".join([convert_tag_to_text(text_tag) for text_tag in body_tag.findChildren(recursive=False)]) + "</p>"
        else:
            text = "(Article text missing, please visit the article URL.)"
        self.content = text

base_url = "https://www.dr.dk/nyheder/service/feeds/"
default_feed_name: str = "senestenyt"

convert_and_print_rss(base_url, default_feed_name, DRNewsArticle)
