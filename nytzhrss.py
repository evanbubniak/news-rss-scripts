#!/usr/bin/env python3
from io import StringIO
from typing import List, Optional
from article import RSSArticle, RSSFeed
from convert_and_print_rss import convert_and_print_rss
from get_url_soup import get_requests_html_soup
from bs4 import Tag
from datetime import datetime as dt
from xml.etree.ElementTree import Element, SubElement, ElementTree

def make_element(channel, title, link, description, pubDate):
    article_item = SubElement(channel, "item")
    e = SubElement(article_item, "title")
    e.text = title
    e = SubElement(article_item, "link")
    e.text = link
    e = SubElement(article_item, "description")
    e.text = description
    e = SubElement(article_item, "pubDate")
    e.text = pubDate
    e = SubElement(article_item, "guid", {"isPermalink": "true"})
    e.text = link

def merge_title_headline(title, headline):
    if title and headline and headline != title:
        title = title + "（" + headline + "）"
    elif headline and not title:
        title = headline
    return title

def expand_link(link):
    if not link[:4] == "http":
        link = "https://cn.nytimes.com" + link
    return link

def extract_date(link):
    date_text = "".join([segment for segment in link.split("/") if segment.isnumeric()])
    date = dt.strptime(date_text, '%Y%m%d')
    return date.strftime("%a, %d %b %Y %H:%M:%S %z")

def process_article(channel, subdiv, headline_tag_name="h3"):
    headline_tag = subdiv.find(headline_tag_name)
    link_tag = headline_tag.find("a")
    link = expand_link(link_tag.attrs.get("href"))
    title = link_tag.attrs.get("title")
    headline = headline_tag.getText() if headline_tag else None
    title = merge_title_headline(title, headline)
    description_tag = subdiv.find("p", class_ = "summary")
    description = description_tag.getText() if description_tag else ""
    pubDate = extract_date(link)
    make_element(channel, title, link, description, pubDate)

def retrieve_zh_rss(url):
    main_page = get_requests_html_soup(url)
    if "zh-hant" in url:
        title = "紐約時報中文網"
    else:
        title = "纽约时报中文网"
    rss_props = {
        "title": title,
        "link": url,
        "description": title,
        "language": "zh",
        "webMaster": "https://github.com/evanbubniak"
        }

    root = Element("rss", {"xmlns:atom": "http://www.w3.org/2005/Atom", "xmlns:media": "http://search.yahoo.com/mrss/", "version": "2.0"})
    channel = SubElement(root, "channel")
    for rss_prop_tagname in rss_props.keys():
        e = SubElement(channel, rss_prop_tagname)
        e.text = rss_props[rss_prop_tagname]

    output_str = StringIO("")

    layouts = ["layoutA", "layoutB", "layoutC"]
    layout_tags = [main_page.find("div", class_ = layout) for layout in layouts]
    if any(layout_tags):
        for layout_tag in layout_tags:
            if layout_tag:
                article_groups = layout_tag.find_all("div", recursive=False)
                for article_group in article_groups:
                    article_subgroups = article_group.find_all("div", recursive = False)
                    for article_subgroup in article_subgroups:
                        subdivs: List[Tag] = article_subgroup.find_all("div", recursive = False)
                        if subdivs:
                            for subdiv in subdivs:
                                if "leadNewsContainer" in subdiv.get_attribute_list("class"):
                                    process_article(channel, subdiv, headline_tag_name="h2")
                                article_list = subdiv.find("ul", recursive=False)
                                if article_list:
                                    for article in article_list.find_all("li"):
                                        process_article(channel, subdiv)
                                else:
                                    process_article(channel, subdiv)

                        else:
                            subdivs: List[Tag] = article_subgroup.find("ul", recursive = False).find_all("li")
                            for subdiv in subdivs:
                                process_article(channel, subdiv)
    else:
        articles_tag = main_page.find("div", class_ = "articles")
        articles_list_tag = articles_tag.find("ol", class_ = "article-list")
        article_listitems = articles_list_tag.find_all("li")

        for article in article_listitems:
            if article.getText() in ["广告", "廣告"]:
                continue

            link_tag: Optional[Tag] = article.find("a")
            if link_tag:
                title = link_tag.attrs.get("title")
                headline_tag = article.find("h2")
                headline = headline_tag.getText() if headline_tag else None
                title = merge_title_headline(title, headline)
                link = link_tag.attrs["href"]
                pubDate = extract_date(link)
                description = article.find("p").getText()
                make_element(channel, title, link, description, pubDate)

    ElementTree(root).write(output_str, encoding="unicode", xml_declaration=True)
    return output_str.getvalue()


class NYTZHRSSFeed(RSSFeed):

    def __init__(self, url):
        self.url = url

    def retrieve_rss(self):
        return retrieve_zh_rss(self.url)

class NYTZHArticle(RSSArticle):
    def retrieve_content(self):
        soup = get_requests_html_soup(self.url)
        body_tag = soup.find("section", class_= "article-body")
        if body_tag:
            main_texts = [text_tag.decode_contents() for text_tag in body_tag.find_all("div", class_="article-paragraph")]
            text = "<p>" + "</p><p>".join(main_texts) + "</p>"
        else:
            text = "(Article text missing, please visit the article URL.)"
        self.content = text.replace("\n", "")

default_zh = "https://cn.nytimes.com/"
convert_and_print_rss(default_zh, "zh-hant/", NYTZHArticle, NYTZHRSSFeed, use_threads=False)