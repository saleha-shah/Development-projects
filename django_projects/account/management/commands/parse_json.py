import json
from django.core.management.base import BaseCommand
from account.models import Listing


class Command(BaseCommand):
    help = 'Populate listings from JSON data'

    def handle(self, *args, **options):
        with open('output.json') as f:
            data = json.load(f)
        
        for item in data:
            listing = Listing(
                brand=item['brand'],
                care=item['care'],
                category=item['category'],
                currency=item['currency'],
                description=item['description'],
                image_urls=item['image_urls'],
                lang=item['lang'],
                market=item['market'],
                name=item['name'],
                price=item['price'],
                retailer_sku=item['retailer_sku'],
                skus=item['skus'],
                trail=item['trail'],
                url=item['url']
            )
            listing.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated listings.'))
