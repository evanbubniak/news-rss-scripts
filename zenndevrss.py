#!/usr/bin/env python3
from article import RSSArticle
from convert_and_print_rss import convert_and_print_rss
from get_url_soup import get_url_soup
from bs4 import NavigableString, Tag

def convert_tag_to_text(text_tag: Tag) -> str:
    if isinstance(text_tag, NavigableString):
        return text_tag
    else:
        return text_tag.decode_contents()
    # elif text_tag.name in ["ul", "ol"]:
    #     return "</p><p>".join("- " + listitem_tag.getText() for listitem_tag in text_tag.find_all("li"))
    # elif text_tag.name in ["h2", "h3"]:
    #     return "[ " + text_tag.getText() + " ]"
    # else:
    #     p_tags = text_tag.find_all("p")
    #     if p_tags:
    #         return "</p><p>".join(p_tag.getText() for p_tag in p_tags)
    #     else:
    #         return text_tag.getText()

class ZennDevArticle(RSSArticle):
    def retrieve_content(self):
        soup = get_url_soup(self.url)
        body_tag = soup.find(id="toc-target-content").find(class_="BodyContent_anchorToHeadings__Vl0_u")
        if body_tag:
            main_texts = [convert_tag_to_text(tag) for tag in body_tag.children]
            text = "<p>" + "</p><p>".join(main_texts) + "</p>"
        else:
            text = "(Article text missing, please visit the article URL.)"
        self.content = text.replace("\n", "")

base_url = ""
default_feed_name: str = "https://zenn.dev/topics/%E5%80%8B%E4%BA%BA%E9%96%8B%E7%99%BA/feed"

convert_and_print_rss(base_url, default_feed_name, ZennDevArticle, use_threads=False)
