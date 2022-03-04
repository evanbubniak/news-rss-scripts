from typing import Type, Optional
import requests
from xml.etree.ElementTree import ElementTree, fromstring, Element
from article import RSSArticle
from io import StringIO
from tqdm import tqdm
from sys import argv

def parse_inputs(base_url, default_feed_name):
    feed_name: str = argv[1] if len(argv) >= 2 else default_feed_name
    article_limit: Optional[int] = int(argv[2]) if len(argv) >= 3 else 25
    target_url = base_url + feed_name
    return target_url, article_limit

def convert_and_print_rss(base_url: str, default_feed_name: str, article_class: Type[RSSArticle], **kwargs):
    target_url, article_limit = parse_inputs(base_url, default_feed_name)
    response = requests.get(target_url)
    root = fromstring(response.content)
    channel = root.find("channel")
    if channel:
        items = channel.findall("item")
        if article_limit is not None:
            for item in items[article_limit:]:
                channel.remove(item)
            items = items[:article_limit]
        articles = [article_class.from_item(item, **kwargs) for item in items]
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