#!/usr/bin/env python3
from article import RSSArticle
from convert_and_print_rss import convert_and_print_rss
from get_url_soup import get_url_soup

def findOccurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]

class AsahiArticle(RSSArticle):
    def retrieve_content(self):
        question_mark_indices = findOccurrences(self.url, "?")
        if len(question_mark_indices) > 0:
            index_of_last_questionmark = question_mark_indices[-1]
            stripped_url = self.url[:index_of_last_questionmark]
        else:
            stripped_url = self.url

        text = ""
        soup = get_url_soup(stripped_url)
        if "www.asahi.com/" in self.url:
            main_tag = soup.find("main")
            
            if main_tag:
                body_tag = main_tag.find(class_ = "nfyQp")
                if body_tag:
                    text_tags = [tag for tag in body_tag.children if "notPrint" not in tag.get_attribute_list("class")]
                    text = "<p>" + "</p><p>".join([text_tag.getText() for text_tag in text_tags]) + "</p>"
        elif "japan.cnet.com/" in self.url:
            body_tag = soup.find(class_ = "article_body")
            if body_tag:
                text = "<p>" + "</p><p>".join([text_tag.getText() for text_tag in body_tag.find_all("p")]) + "</p>"
        elif "japan.zdnet.com" in self.url:
            body_tag = soup.find(class_ = "article-contents")
            if body_tag:
                text = "<p>" + "</p><p>".join([text_tag.getText() for text_tag in body_tag.find_all("p")]) + "</p>"
        
        if not text:
            text = "(Article text missing, please visit the article URL.)"
        self.content = text

base_url = "https://www.asahi.com/rss/"
default_feed_name: str =  "asahi/newsheadlines.rdf"

convert_and_print_rss(base_url, default_feed_name, AsahiArticle)