import json

from django.core.management.base import BaseCommand

from ecommerce.models import Product, ImageURL, Category, Description, SKU, Care


class Command(BaseCommand):
    help = 'Populate listings from JSON data'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='JSON filename to populate data')

    def handle(self, *args, **options):
        filename = options['filename']
        with open(filename) as f:
            data = json.load(f)

        for item in data:
            product = Product(
                brand=item['brand'],
                currency=item['currency'],
                lang=item['lang'],
                market=item['market'],
                name=item['name'],
                price=item['price'],
                gender=item['gender'],
                retailer_sku=item['retailer_sku'],
                trail=item['trail'],
                url=item['url']
            )
            product.save()

            image_urls = [
                ImageURL(product=product, color=color, url=url)
                for color, urls in item['image_urls'].items()
                for url in urls
            ]
            ImageURL.objects.bulk_create(image_urls)

            categories = [
                Category(product=product, category=category)
                for category in item['category']
            ]
            Category.objects.bulk_create(categories)

            description = [
                Description(product=product, content=content)
                for content in item['description']
            ]
            Description.objects.bulk_create(description)

            care = [
                Care(product=product, content=care)
                for care in item['care']
            ]
            Care.objects.bulk_create(care)

            skus = [
                SKU(
                    product=product,
                    sku=sku,
                    color=details['colour'],
                    size=details['size'],
                    currency=details['currency'],
                    price=details['price'],
                    out_of_stock=details['out_of_stock']
                )
                for sku, details in item['skus'].items()
            ]
            SKU.objects.bulk_create(skus)

        self.stdout.write(self.style.SUCCESS('Successfully populated listings.'))
