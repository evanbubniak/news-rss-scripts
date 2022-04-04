#!/usr/bin/env python3
from convert_and_print_rss import convert_and_print_rss
from article import RSSArticle
from get_url_soup import get_url_soup

class YahooNewsArticle(RSSArticle):

    def __init__(self, url = None, incl_date_in_content = True, *args, **kwargs):
        if "pickup" in url:
            self.digest_url = url
            url = None
        else:
            self.digest_url = None
        self.incl_date_in_content = incl_date_in_content
        super().__init__(*args, **kwargs)

    def get_url(self):
        if not self.url:
            self.thread.join()
        return self.url

    def get_title(self):
        if not self.title:
            self.thread.join()
        return self.title

    def get_content(self):
        if not self.content:
            self.thread.join()
        return self.date_repr + self.content if self.incl_date_in_content else self.content

    def get_digest_text(self) -> str:
        digest_soup = get_url_soup(self.digest_url)
        return digest_soup.find("div", attrs={"data-ual-view-type": "digest"}).find("p", recursive=False).text

    def retrieve_content(self):
        if self.digest_url and not self.url:
            self.set_url()
        soup = get_url_soup(self.url)
        article_tag = soup.find("article")
        title = article_tag.find("header").find("h1").getText() if article_tag else None
        self.date_repr = f"{article_tag.find('time').getText()}\n\n" if article_tag else None
        text_tag = soup.find("div", class_="article_body")
        if text_tag:
            a_tags = text_tag.find_all("a")
            if a_tags:
                for a_tag in a_tags:
                    a_tag.extract()
            
            self.content = "<p>" + "</p><p>".join(text_tag.getText().split("\n\n")) + "</p>"
        else:
            self.content = "(Article text missing, please visit the article URL.)"
        if title:
            self.title = title

    def set_url(self) -> None:
        digest_soup = get_url_soup(self.digest_url)
        self.url = digest_soup.find(attrs={"data-ual-gotocontent": "true"}).attrs["href"]

URL_SUFFIX = "?source=rss"
base_url = "https://news.yahoo.co.jp/rss/"
default_feed_name = "topics/top-picks.xml"

def get_item_link(item, pref):
    link = item.find("link")
    return "" if link is None else link.text[:-1*len(URL_SUFFIX)]

convert_and_print_rss(base_url, default_feed_name, YahooNewsArticle, incl_date_in_content = False, get_item_link = get_item_link)