# populate_sample_data.py
from django.core.management.base import BaseCommand
from shop.models import Category, Jewellery

class Command(BaseCommand):
    help = 'Populate database with sample jewellery data'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {'name': 'Necklaces', 'slug': 'necklaces'},
            {'name': 'Bracelets', 'slug': 'bracelets'},
            {'name': 'Earrings', 'slug': 'earrings'},
            {'name': 'Rings', 'slug': 'rings'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
        
        # Create sample jewellery items
        jewellery_data = [
            {
                'name': 'Diamond Elegance Necklace',
                'category': Category.objects.get(slug='necklaces'),
                'price': 25000,
                'description': 'Exquisite diamond necklace with premium craftsmanship.',
                'is_featured': True,
                'badge': 'BEST',
                'stone_type': 'DIAMOND',
                'color': 'GOLD'
            },
            {
                'name': 'Ruby Royal Bracelet',
                'category': Category.objects.get(slug='bracelets'),
                'price': 18000,
                'description': 'Beautiful ruby bracelet with intricate design.',
                'is_featured': True,
                'badge': 'NEW',
                'stone_type': 'RUBY',
                'color': 'SILVER'
            },
            # Add more sample items as needed
        ]
        
        for jewellery_item in jewellery_data:
            jewellery, created = Jewellery.objects.get_or_create(
                name=jewellery_item['name'],
                defaults=jewellery_item
            )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated sample data')
        )