#!/usr/bin/env python3
from io import StringIO
from typing import Optional
from article import RSSArticle, RSSFeed
from convert_and_print_rss import convert_and_print_rss
from get_url_soup import get_url_soup
from bs4 import Tag
from datetime import datetime as dt
from xml.etree.ElementTree import Element, SubElement, ElementTree


def retrieve_es_rss(url):
    main_page = get_url_soup(url)
    title_tag = main_page.find("h1")
    if title_tag:
        title = "NYT Es: " + title_tag.getText()
    else:
        title = "New York Times en Español"
    rss_props = {
        "title": title,
        "link": url,
        "description": "New York Times in Spanish",
        "language": "es",
        "webMaster": "https://github.com/evanbubniak"
        }

    root = Element("rss", {"xmlns:atom": "http://www.w3.org/2005/Atom", "xmlns:media": "http://search.yahoo.com/mrss/", "version": "2.0"})
    channel = SubElement(root, "channel")
    for rss_prop_tagname in rss_props.keys():
        e = SubElement(channel, rss_prop_tagname)
        e.text = rss_props[rss_prop_tagname]

    output_str = StringIO("")

    sections = ["stream-panel", "collection-highlights-container"]

    for section in sections:
        section_elem = main_page.find("section", attrs={"id": section})

        if section_elem:
            article_lists = section_elem.find_all("ol")
            for article_list in article_lists:
                articles = article_list.find_all("li")
                for article in articles:
                    article_item = SubElement(channel, "item")
                    link_tag: Optional[Tag] = article.find("a")
                    if link_tag:
                        title_tag = article.find("h2")
                        title = title_tag.getText() if title_tag else "title missing"
                        link = "https://www.nytimes.com" + link_tag.attrs["href"]
                        split = link.split("/")
                        for i in range(len(split)-3):
                            try:
                                date_text = "/".join(split[i:i+3])
                                date = dt.strptime(date_text, '%Y/%m/%d')
                                break
                            except:
                                pass
                        pubDate = date.strftime("%a, %d %b %Y %H:%M:%S %z")
                        description = article.find("p").getText()

                    else:
                        title = "title missing"
                        link = "link missing"
                        pubDate = "pubDate missing"
                        description = "description missing"
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

    ElementTree(root).write(output_str, encoding="unicode", xml_declaration=True)
    return output_str.getvalue()

def retrieve_zh_rss(url):
    main_page = get_url_soup(url)
    # title_tag = main_page.find("h1")
    # if title_tag:
    #     title = "NYT Es: " + title_tag.getText()
    # else:
    #     title = "New York Times en Español"
    title = "紐約時報中文網"
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

    for layout in layouts:

        layout_tag = main_page.find("div", class_ = layout)


        if layout_tag:
            article_groups = layout_tag.find_all("div", recursive=False)
            for article_group in article_groups:
                article_subgroups = article_group.find_all("div", recursive = False)
                for article_subgroup in article_subgroups:
                    subdivs = article_subgroup.find_all("div", recursive = False)
                    if not subdivs:
                        subdivs = article_subgroup.find("ul", recursive = False).find_all("li")

            # article_lists = section_elem.find_all("ol")
            # for article_list in article_lists:
            #     articles = article_list.find_all("li")
            #     for article in articles:
            #         article_item = SubElement(channel, "item")
            #         link_tag: Optional[Tag] = article.find("a")
            #         if link_tag:
            #             title_tag = article.find("h2")
            #             title = title_tag.getText() if title_tag else "title missing"
            #             link = "https://www.nytimes.com" + link_tag.attrs["href"]
            #             date_text = "/".join(link.split("/")[4:7])
            #             date = dt.strptime(date_text, '%Y/%m/%d')
            #             pubDate = date.strftime("%a, %d %b %Y %H:%M:%S %z")
            #             description = article.find("p").getText()

            #         else:
            #             title = "title missing"
            #             link = "link missing"
            #             pubDate = "pubDate missing"
            #             description = "description missing"
            #         e = SubElement(article_item, "title")
            #         e.text = title
            #         e = SubElement(article_item, "link")
            #         e.text = link
            #         e = SubElement(article_item, "description")
            #         e.text = description
            #         e = SubElement(article_item, "pubDate")
            #         e.text = pubDate
            #         e = SubElement(article_item, "guid", {"isPermalink": "true"})
            #         e.text = link

    ElementTree(root).write(output_str, encoding="unicode", xml_declaration=True)
    return output_str.getvalue()

class NYTESRSSFeed(RSSFeed):

    def __init__(self, url):
        self.url = url

    def retrieve_rss(self):
        if "/es/" in self.url:
            return retrieve_es_rss(self.url)
        else:
            return retrieve_zh_rss(self.url)

class NYTESArticle(RSSArticle):
    def retrieve_content(self):
        soup = get_url_soup(self.url)
        body_tag = soup.find("section", attrs={"name": "articleBody"})
        if body_tag:
            main_texts = [text_tag.getText() for text_tag in body_tag.find_all("p")]
            text = "<p>" + "</p><p>".join(main_texts) + "</p>"
        else:
            text = "(Article text missing, please visit the article URL.)"
        self.content = text.replace("\n", "")

convert_and_print_rss("https://www.nytimes.com/es/", "", NYTESArticle, NYTESRSSFeed)
