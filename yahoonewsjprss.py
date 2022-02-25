#!/usr/bin/env python3
from typing import Optional
from yahoonewsjp_api import YahooNewsArticle
from sys import argv
from convert_and_print_rss import convert_and_print_rss


URL_SUFFIX = "?source=rss"
base_url = "https://news.yahoo.co.jp/rss/"
feed_name: str = argv[1] if len(argv) >= 2 else "topics/top-picks.xml"
article_limit: Optional[int] = int(argv[2]) if len(argv) >= 3 else None
target_url = base_url + feed_name

def get_item_link(item):
    link = item.find("link")
    return "" if link is None else link.text[:-1*len(URL_SUFFIX)]

def get_item_title(item):
    title = item.find("title")
    return "" if title is None else title.text

def item_to_article(item):
    return YahooNewsArticle(digest_url = get_item_link(item), short_title = get_item_title(item), incl_date_in_content = False)

convert_and_print_rss(target_url, article_limit, item_to_article)