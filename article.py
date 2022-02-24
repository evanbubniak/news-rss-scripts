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