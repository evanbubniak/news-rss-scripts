from typing import Type, Optional
from xml.etree.ElementTree import ElementTree, fromstring, Element
from article import RSSArticle, RSSFeed
from io import StringIO
from tqdm import tqdm
from sys import argv

DEFAULT_ARTICLE_LIMIT = 25

def convert_and_print_rss(base_url: str, default_feed_name: str, article_class: Type[RSSArticle] = RSSArticle, feed_class: Type[RSSFeed] = RSSFeed, **kwargs):
    feed_name: str = argv[1] if len(argv) >= 2 else default_feed_name
    target_url = base_url + feed_name
    feed = feed_class(target_url)

    article_limit: Optional[int] = int(argv[2]) if len(argv) >= 3 else DEFAULT_ARTICLE_LIMIT

    assert feed is not None, "Unable to create feed or no feed passed in."

    pref = ""
    root = fromstring(feed.retrieve_rss())
    channel = root.find("channel")
    if not channel:
        # Special case to handle RDF feeds, where items are children of root and which have a namespace prefix.
        pref = "{http://purl.org/rss/1.0/}"
        channel = root

    if channel:        
        items = channel.findall(pref + "item")

        if article_limit is not None:
            for item in items[article_limit:]:
                channel.remove(item)
            items = items[:article_limit]
        articles = [article_class.from_item(item, pref=pref, **kwargs) for item in items]
        for item, article in tqdm(zip(items, articles), total = len(items)):
            link = item.find(pref + "link")
            description = item.find(pref + "description")
            if link is not None:
                link.text = article.get_url()

            if description is None:
                description = Element(pref + "description")
                item.append(description)

            description.text = article.get_content()

        etree = ElementTree(element=root)
        output_str = StringIO("")
        etree.write(output_str, encoding="unicode", xml_declaration=True)
        print(output_str.getvalue())