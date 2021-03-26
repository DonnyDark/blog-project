import requests
from multiprocessing import Process, Queue
from bs4 import BeautifulSoup

COOKIES = {'pcid': 'MaClH3Acnv2',
            'la': '1616748234_4348_4593_4640__4349',
            'ulfs': '1616748234',
            'is_scrollmode': '0',}

class PicabuParser:
    def __init__(self, url='https://pikabu.ru/'):
        self.url = url
        self.headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0',
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',}

    def get_response(self, page=1):
        response = requests.get(url=self.url+f'?page={page}', headers=self.headers, cookies=COOKIES)
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

    def get_published_time(self, main_container):
        time = main_container.find('time')
        if time:
            return time.get_text(strip=True)
        else:
            return None

    def get_order_of_data(self, main_container):
        order_list_of_data = []
        body_container = main_container.find('div', class_='story__content-inner')
        if body_container:
            inners = body_container.find_all('div')
        else:
            return None
        for inner in inners:
            if inner.find('p'):
                text_list = []
                text_containers = inner.find_all('p')
                for text in text_containers:
                    text_list.append(text.get_text(strip=True))
                order_list_of_data.append(text_list)
            elif inner.find('figure'):
                image = inner.find('img').get('data-src')
                order_list_of_data.append(image)

        return order_list_of_data

    def parse(self, page=1):
        soup = BeautifulSoup(self.get_response(page).text, 'html.parser')
        main_containers = soup.find_all('article', class_='story')
        articles = []
        for main_container in main_containers:
            articles.append({
                'title': self.get_title(main_container),
                'order_of_main_data': self.get_order_of_data(main_container),
                'published_time': self.get_published_time(main_container),
                'tags': self.get_tags(main_container),
            })
        return articles


def parse_one_page(queue_for_data, queue_for_num, page=1):
    parse_obj = PicabuParser()
    all_data = parse_obj.parse(page)
    queue_for_data.put(all_data)
    queue_for_num.put(1)


def parse_pages(total_pages=10, test=False):
    processes = []
    queue_for_data = Queue()
    queue_for_num = Queue()
    for i in range(1, total_pages+1):
        processes.append(Process(target=parse_one_page, args=(queue_for_data, queue_for_num, i)))
        processes[i-1].start()
        if test:
            print(f'process {i} is started...')

    all_data = []
    list_of_nums = []
    while sum(list_of_nums) != total_pages:
        if not queue_for_num.empty():
            list_of_nums.append(queue_for_num.get())
            all_data.extend(queue_for_data.get())
            if test:
                print(f'process {sum(list_of_nums)} is finished...')

    for process in processes:
        process.join()

    return all_data


if __name__ == '__main__':
    print(parse_pages(4, test=True))