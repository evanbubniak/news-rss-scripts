from typing import Callable, Optional
import requests
from xml.etree.ElementTree import ElementTree, fromstring, Element
from bs4 import Tag
from article import Article
from io import StringIO
from tqdm import tqdm

def convert_and_print_rss(target_url: str, article_limit: Optional[int], item_to_article: Callable[[Tag], Article]):
    response = requests.get(target_url)
    root = fromstring(response.content)
    channel = root.find("channel")
    if channel:
        items = channel.findall("item")
        articles = [item_to_article(item) for item in items]
        if article_limit is not None:
            articles = articles[:article_limit]

        for item, article in tqdm(zip(items, articles), total = len(items)):
            link = item.find("link")
            description = item.find("description")
            if link is not None:
                link.text = article.get_url()

            if description is None:
                description = Element("description")
                item.append(description)

            description.text = article.get_content()

        etree = ElementTree(element=root)
        output_str = StringIO("")
        etree.write(output_str, encoding="unicode", xml_declaration=True)
        print(output_str.getvalue())