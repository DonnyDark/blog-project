from django.core.management.base import BaseCommand

from blog.models import BlogModel
from blog.parsers import pikabu_parser

from texts_and_images.models import TextOrImage


class Command(BaseCommand):

    def additional_logic_method_for_handle(self, all_data):
        for data in all_data:
            pass

    def handle(self, *args, **kwargs):
        parser_obj = pikabu_parser.PicabuParser()
        all_data = parser_obj.parse()
        self.additional_logic_method_for_handle(all_data)

