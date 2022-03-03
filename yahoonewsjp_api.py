from get_url_soup import get_url_soup
from yahoonewsjprss import YahooNewsArticle

base_url = "https://news.yahoo.co.jp/"
def get_n_yahoonews_jp_top_articles(n=8):
    assert n > 0 and n <= 8, "the number of articles requested must be between 1 and 8"
    home_soup = get_url_soup(base_url)
    topics = home_soup.find(class_="topics")
    top_articles_items = topics.find_all(attrs={"data-ual-view-type":"list"})[:n]
    articles = [YahooNewsArticle(short_title = article_item.getText(), url = article_item.next_element.attrs["href"]) for article_item in top_articles_items]
    return articles
    
if __name__ == "__main__":
    for article in get_n_yahoonews_jp_top_articles():
        print(article)