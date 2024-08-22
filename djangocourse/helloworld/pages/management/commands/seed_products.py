from django.core.management.base import BaseCommand
from pages.factories import ProductFactory

class Command(BaseCommand):
    help = 'Seeds the database with products'

    def handle(self, *args, **kwargs):
        ProductFactory.create_batch(8)
        self.stdout.write(self.style.SUCCESS('Products seeded products!'))
