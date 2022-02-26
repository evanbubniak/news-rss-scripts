#!/usr/bin/env python3
from typing import Optional
from article import Article, RSSArticle
from sys import argv
from convert_and_print_rss import convert_and_print_rss
from get_url_soup import get_url_soup
from bs4 import Tag

def convert_tag_to_text(text_tag: Tag) -> str:
    if text_tag.name in ["ul", "ol"]:
        return "</p><p>".join("- " + listitem_tag.getText() for listitem_tag in text_tag.find_all("li"))
    elif text_tag.name == "h2":
        return "[ " + text_tag.getText() + " ]"
    else:
        return text_tag.getText()

class DeutscheWelleArticle(RSSArticle):
    def retrieve_content(self):
        soup = get_url_soup(self.url)
        body_tag = soup.find("div", class_="col3")
        if body_tag:
            intro_text_tag = body_tag.find("p", class_ = "intro")
            intro_text = intro_text_tag.getText() if intro_text_tag else ""
            main_text_tag = body_tag.find("div", class_ = "longText")
            main_texts = [convert_tag_to_text(text_tag) for text_tag in main_text_tag.findChildren(recursive=False)] if main_text_tag else []
            text = "<p>" + "</p><p>".join([intro_text] + main_texts) + "</p>"
        else:
            text = "(Article text missing, please visit the article URL.)"
        self.content = text.replace("\n", "")

base_url = "https://rss.dw.com/"
feed_name: str = argv[1] if len(argv) >= 2 else "xml/rss-de-all"
article_limit: Optional[int] = int(argv[2]) if len(argv) >= 3 else None
target_url = base_url + feed_name

def get_item_link(item) -> str:
    link = item.find("link")
    return "" if link is None else link.text

def get_item_title(item) -> str:
    title = item.find("title")
    return "" if title is None else title.text

def item_to_article(item) -> Article:
    return DeutscheWelleArticle(url = get_item_link(item), title = get_item_title(item), use_threads=True)

convert_and_print_rss(target_url, article_limit, item_to_article)