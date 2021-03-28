from django.core.management.base import BaseCommand

from blog.models import BlogModel


class Command(BaseCommand):
    help = 'delete all objects of BlogModel'

    def handle(self, *args, **options):
        BlogModel.objects.all().delete()