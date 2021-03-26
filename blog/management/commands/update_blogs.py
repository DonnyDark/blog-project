import requests

from PIL import Image

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files.images import ImageFile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from blog.models import BlogModel
from blog.parsers import pikabu_parser
from texts_and_images.models import TextOrImage


class Command(BaseCommand):
    help = 'update blogs'

    def add_arguments(self, parser):
        parser.add_argument('pages', type=int, help='total pages for parsing')

    def additional_logic_method_for_handle(self, all_data):
        user = get_user_model().objects.first()
        for data in all_data:
            if data['order_of_main_data']:
                blog = BlogModel(title=data['title'], author=user, tags=' '.join(data['tags']))
                for i, main_data in enumerate(data['order_of_main_data']):
                    if type(main_data) is list:
                        for text in main_data:
                            new_text = TextOrImage(blog=blog, text=text)
                            new_text.save()
                    else:
                        r = requests.get(url=main_data, stream=True)
                        r.raw.decode_content = True
                        all_bytes = b''
                        for content in r:
                            all_bytes += content
                        if main_data[-3:] == 'jpg':
                            pass
                        image_path = str(int(blog.id) + i) + '.png'
                        path = default_storage.save(image_path, ContentFile(all_bytes))

                        image = TextOrImage(blog=blog)
                        image.image = ImageFile(open('media/'+path, 'rb'))
                        image.save()

    def handle(self, *args, **kwargs):
        pages = kwargs['pages']
        all_data = pikabu_parser.parse_pages(pages)
        self.additional_logic_method_for_handle(all_data)


