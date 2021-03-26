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

    def get_title(self, main_container):
        title_container = main_container.find('h2', class_='story__title')
        if title_container:
            title = title_container.find('a').get_text(strip=True)
            return title
        else:
            return None

    def get_tags(self, main_container):
        tags_container = main_container.find('div', class_='story__tags tags')
        if tags_container:
            tags = tags_container.find_all('a')
            tags_list = []
            for tag in tags:
                tags_list.append(tag.get_text(strip=True))
            return tags_list
        else:
            return None

    def get_text(self, main_container):
        text_containers = main_container.find_all('div', class_='story-block story-block_type_text')
        full_text = []
        if text_containers:
            for text_container in text_containers:
                texts = text_container.find_all('p')
                for text in texts:
                    full_text.append(text.get_text(strip=True))
        return full_text

    def get_images(self, main_container):
        image_containers = main_container.find_all('div', class_='story-block story-block_type_image')
        images_urls = []
        if image_containers:
            for image in image_containers:
                images_urls.append(image.find('img').get('src'))
        return images_urls

    def get_published_time(self, main_container):
        time = main_container.find('time')
        if time:
            return time.get_text(strip=True)
        else:
            return None

    def get_order_of_data(self, main_container):
        body_container = main_container.find('div', class_='story__content-inner')
        inners = body_container.find_all('div')
        for inner in inners:
            pass

    def parse(self):
        soup = BeautifulSoup(self.response.text, 'html.parser')
        main_containers = soup.find_all('article', class_='story')
        articles = []
        for main_container in main_containers:
            articles.append({
                'title': self.get_title(main_container),
                'text': self.get_text(main_container),
                'image': self.get_images(main_container),
                'published_time': self.get_published_time(main_container),
                'tags': self.get_tags(main_container),
            })
        return articles


if __name__ == '__main__':
    picabu_obj = PicabuParser()
    print(picabu_obj.parse())