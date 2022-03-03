#!/usr/bin/env python3
from article import RSSArticle
from convert_and_print_rss import convert_and_print_rss
from get_url_soup import get_url_soup
from bs4 import Tag


def is_article_text(tag: Tag) -> bool:
    article_text_classes = ["artstyle__intro", "artstyle__paragraph", "artstyle__title", "block-text", "block-lead", "block-chapter"]
    return any(article_text_class in tag.get_attribute_list("class") for article_text_class in article_text_classes)

def convert_tag_to_text(text_tag: Tag) -> str:
    if text_tag.name in ["ul", "ol"]:
        return "</p><p>".join("- " + listitem_tag.getText() for listitem_tag in text_tag.find_all("li"))
    elif text_tag.name == "h3" and "artstyle__title" in text_tag.get_attribute_list("class"):
        return "[ " + text_tag.getText() + " ]"
    else:
        return text_tag.getText()

class VolkskrantArticle(RSSArticle):
    def retrieve_content(self):
        soup = get_url_soup(self.url)
        body_tag = soup.find("article")
        if body_tag:
            main_texts = [convert_tag_to_text(text_tag) for text_tag in body_tag.find_all(is_article_text)]
            text = "<p>" + "</p><p>".join(main_texts) + "</p>"
        else:
            text = "(Article text missing, please visit the article URL.)"
        self.content = text.replace("\n", "")

base_url = "https://www.volkskrant.nl/"
default_feed_name: str = "voorpagina/rss.xml"

convert_and_print_rss(base_url, default_feed_name, VolkskrantArticle)