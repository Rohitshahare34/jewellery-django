"""
Management command to fetch and store metal prices from API
Usage: python manage.py fetch_metal_prices
"""
from django.core.management.base import BaseCommand
from shop.price_api import update_metal_prices


class Command(BaseCommand):
    help = 'Fetch and update gold and silver prices from API'

    def handle(self, *args, **options):
        self.stdout.write('Fetching latest metal prices from API...')
        
        try:
            result = update_metal_prices()
            
            if result['success']:
                self.stdout.write(self.style.SUCCESS('✓ Prices updated successfully!'))
                self.stdout.write(f"  Gold: ₹{result['gold']['price_per_gram']}/g")
                self.stdout.write(f"  Silver: ₹{result['silver']['price_per_gram']}/g")
                self.stdout.write(f"  Gold Change: {result['gold']['change_percent']}% {'↑' if result['gold']['is_up'] else '↓'}")
                self.stdout.write(f"  Silver Change: {result['silver']['change_percent']}% {'↑' if result['silver']['is_up'] else '↓'}")
            else:
                self.stdout.write(self.style.ERROR(f'✗ Failed to update prices: {result["message"]}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error: {str(e)}'))
