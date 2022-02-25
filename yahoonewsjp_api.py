from typing import Tuple
import threading
from article import Article
from get_url_soup import get_url_soup

class YahooNewsArticle(Article):

    def __init__(self, digest_url = None, incl_date_in_content = True, *args, **kwargs):
        self.digest_url = digest_url
        self.incl_date_in_content = incl_date_in_content
        super().__init__(*args, **kwargs)
        self.thread = threading.Thread(target=self.set_url_and_get_content)
        self.thread.start()

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

    def set_url_and_get_content(self):
        self.set_url()
        title, content = self.load_content()
        if title:
            self.title = title
        self.content = content


    def set_url(self) -> None:
        digest_soup = get_url_soup(self.digest_url)
        self.url = digest_soup.find(attrs={"data-ual-gotocontent": "true"}).attrs["href"]

    def load_content(self) -> Tuple[str, str]:
        soup = get_url_soup(self.url)
        article_tag = soup.find("article")
        full_title = article_tag.find("header").find("h1").getText() if article_tag else None
        self.date_repr = f"{article_tag.find('time').getText()}\n\n" if article_tag else None
        text_tag = soup.find("div", class_="article_body")
        if text_tag:
            a_tags = text_tag.find_all("a")
            if a_tags:
                for a_tag in a_tags:
                    a_tag.extract()
            text = text_tag.getText()
        else:
            text = "(Article text missing, please visit the article URL.)"
        return full_title, text.replace("\n\n", "\n")

base_url = "https://news.yahoo.co.jp/"

def get_n_yahoonews_jp_top_articles(n=8):
    assert n > 0 and n <= 8, "the number of articles requested must be between 1 and 8"
    home_soup = get_url_soup(base_url)
    topics = home_soup.find(class_="topics")
    top_articles_items = topics.find_all(attrs={"data-ual-view-type":"list"})[:n]
    articles = [YahooNewsArticle(short_title = article_item.getText(), digest_url = article_item.next_element.attrs["href"]) for article_item in top_articles_items]
    return articles
    
if __name__ == "__main__":
    for article in get_n_yahoonews_jp_top_articles():
        print(article)