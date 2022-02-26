#!/usr/bin/env python3
from typing import Optional
from article import Article, RSSArticle
from sys import argv
from convert_and_print_rss import convert_and_print_rss
from get_url_soup import get_url_soup
from bs4 import Tag


def is_article_text(tag: Tag) -> bool:
    return "artstyle__intro" in tag.get_attribute_list("class") or "artstyle__paragraph" in tag.get_attribute_list("class") or "artstyle__title" in tag.get_attribute_list("class")

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
feed_name: str = argv[1] if len(argv) >= 2 else "voorpagina/rss.xml"
article_limit: Optional[int] = int(argv[2]) if len(argv) >= 3 else None
target_url = base_url + feed_name

def get_item_link(item) -> str:
    link = item.find("link")
    return "" if link is None else link.text

def get_item_title(item) -> str:
    title = item.find("title")
    return "" if title is None else title.text

def item_to_article(item) -> Article:
    return VolkskrantArticle(url = get_item_link(item), title = get_item_title(item), use_threads=True)

convert_and_print_rss(target_url, article_limit, item_to_article)