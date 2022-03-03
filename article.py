import threading
from abc import ABCMeta, abstractmethod

class Article:

    def __init__(self, title: str = "", short_title = None, content = None, url = None):
        self.title = title
        self.short_title = short_title
        self.content = content
        self.url = url

    def __repr__(self) -> str:
        return f"Title: {self.get_title()}\nContent: {self.get_content()}\nURL: {self.get_url()}"

    def get_content(self) -> str:
        return self.content

    def get_title(self) -> str:
        return self.title if self.title else self.short_title

    def get_short_title(self) -> str :
        return self.short_title if self.short_title else self.title

    def get_url(self) -> str:
        return self.url


def get_item_link(item) -> str:
    link = item.find("link")
    return "" if link is None else link.text

def get_item_title(item) -> str:
    title = item.find("title")
    return "" if title is None else title.text

class RSSArticle(Article, metaclass=ABCMeta):
    def __init__(self, *args, use_threads = True, **kwargs):
        super().__init__(*args, **kwargs)
        if use_threads:
            self.thread = threading.Thread(target=self.retrieve_content)
            self.thread.start()
        else:
            self.thread = None

    def get_content(self):
        if not self.content:
            if self.thread:
                self.thread.join()
            else:
                self.retrieve_content()
        return self.content

    @abstractmethod
    def retrieve_content(self):
        pass

    @classmethod
    def from_item(cls, item, get_item_link = get_item_link, get_item_title = get_item_title, **kwargs) -> Article:
        return cls(url = get_item_link(item), title = get_item_title(item), **kwargs)