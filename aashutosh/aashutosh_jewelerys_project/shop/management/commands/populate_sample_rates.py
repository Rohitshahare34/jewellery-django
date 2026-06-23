from django.core.management.base import BaseCommand
from shop.models import MetalRate, PopupMessage

class Command(BaseCommand):
    help = 'Populates sample data for Gold & Silver Rate System'

    def handle(self, *args, **kwargs):
        # Clear existing data
        MetalRate.objects.all().delete()
        PopupMessage.objects.all().delete()
        
        # Create Metal Rates
        rates_data = [
            {
                'metal_type': '24K Gold',
                'purity': 99.5,
                'rate_per_gram': 14840.00,
                'making_charge': 200.00,
                'making_type': 'FIXED',
                'gst_percentage': 3.0,
                'status': True
            },
            {
                'metal_type': '22K Gold',
                'purity': 91.6,
                'rate_per_gram': 13660.00,
                'making_charge': 12.0,
                'making_type': 'PERCENTAGE',
                'gst_percentage': 3.0,
                'status': True
            },
            {
                'metal_type': '18K Gold',
                'purity': 75.0,
                'rate_per_gram': 11140.00,
                'making_charge': 17.0,
                'making_type': 'PERCENTAGE',
                'gst_percentage': 3.0,
                'status': True
            },
            {
                'metal_type': 'Silver',
                'purity': 99.5,
                'rate_per_gram': 245.00,
                'making_charge': 0.0,
                'making_type': 'FIXED',
                'gst_percentage': 3.0,
                'status': True
            }
        ]
        
        for data in rates_data:
            MetalRate.objects.create(**data)
        self.stdout.write(self.style.SUCCESS('Successfully populated Metal Rates!'))
        
        # Create Popup Message
        PopupMessage.objects.create(
            title="Today's Gold Rate",
            message="Check out today's live gold and silver prices!",
            status=True,
            show_on_refresh=True
        )
        self.stdout.write(self.style.SUCCESS('Successfully created sample Popup!'))
        
        self.stdout.write(self.style.SUCCESS('\nSample data populated successfully!'))
