import requests
from bs4 import BeautifulSoup


class PicabuParser:
    def __init__(self, url='https://pikabu.ru/'):
        self.url = url
        self.headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0',
                        'accept': '*/*',}
        self.response = self.get_response()
        self.response_status_code = self.response.status_code

    def get_response(self):
        response = requests.get(url=self.url, headers=self.headers)
        return response

    def parse_tags(self, tags_container):
        tags = tags_container.find_all('a')
        tags_list = []
        for tag in tags:
            tags_list.append(tag.get_text(strip=True))
        return tags_list

    def parse_text(self, text_container):
        pass

    def test_parse(self):
        soup = BeautifulSoup(self.response.text, 'html.parser')

        articles_container = soup.find('div', class_='stories-feed__container')
        all_articles = articles_container.find_all('article', class_='story')
        articles = []
        for article in all_articles:
            articles.append({
                'title': article.find('a', class_='story__title-link story__title-link_visited').get_text(strip=True),
                'text': self.parse_text(article.find('div', class_='story-block story-block_type_text')),
                'image': '',
                'published_time': '',
                'tags': self.parse_tags(article.find('div', class_='story__tags tags')),
            })
        return articles
