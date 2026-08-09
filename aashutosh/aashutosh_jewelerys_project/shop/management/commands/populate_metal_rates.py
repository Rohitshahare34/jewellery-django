from django.core.management.base import BaseCommand
from shop.models import MetalRate

class Command(BaseCommand):
    help = 'Populates the database with sample metal rates'

    def handle(self, *args, **kwargs):
        # Clear existing rates
        MetalRate.objects.all().delete()
        
        # Create sample rates
        rates = [
            {
                'metal_type': 'GOLD_24K',
                'purity': 99.5,
                'rate_per_gram': 14840.00,
                'making_charge': 200.00,
                'making_type': 'FIXED',
                'gst_percentage': 3.0,
                'status': True
            },
            {
                'metal_type': 'GOLD_22K',
                'purity': 91.6,
                'rate_per_gram': 13660.00,
                'making_charge': 12.0,
                'making_type': 'PERCENTAGE',
                'gst_percentage': 3.0,
                'status': True
            },
            {
                'metal_type': 'GOLD_18K',
                'purity': 75.0,
                'rate_per_gram': 11140.00,
                'making_charge': 17.0,
                'making_type': 'PERCENTAGE',
                'gst_percentage': 3.0,
                'status': True
            },
            {
                'metal_type': 'GOLD_14K',
                'purity': 58.3,
                'rate_per_gram': 9200.00,
                'making_charge': 15.0,
                'making_type': 'PERCENTAGE',
                'gst_percentage': 3.0,
                'status': True
            },
            {
                'metal_type': 'SILVER',
                'purity': 92.5,
                'rate_per_gram': 245.00,
                'making_charge': 0.0,
                'making_type': 'FIXED',
                'gst_percentage': 3.0,
                'status': True
            }
        ]

        for rate_data in rates:
            MetalRate.objects.create(**rate_data)
        
        self.stdout.write(self.style.SUCCESS('Successfully populated sample metal rates!'))
