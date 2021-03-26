import requests

HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0',
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
test_url = 'https://cs13.pikabu.ru/post_img/2021/03/26/6/1616747916134821752.webp'


def save_image(url='', blog_id=''):
    response = requests.get(url=test_url, headers=HEADERS, stream=True)
    response.raw.decode_content = True
    all_bytes = b''
    if response.status_code == 200:
        for i, j in enumerate(response):
            all_bytes += j

    return all_bytes


if __name__ == '__main__':
    print(save_image())