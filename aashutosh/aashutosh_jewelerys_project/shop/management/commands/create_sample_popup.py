from django.core.management.base import BaseCommand
from shop.models import PopupMessage

class Command(BaseCommand):
    help = 'Creates a sample popup message'

    def handle(self, *args, **kwargs):
        # Create a sample popup
        popup, created = PopupMessage.objects.update_or_create(
            title="Today's Gold Rate",
            defaults={
                'message': 'Check out today\'s live gold and silver prices!',
                'status': True,
                'show_on_refresh': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created sample popup!'))
        else:
            self.stdout.write(self.style.SUCCESS('Successfully updated sample popup!'))
