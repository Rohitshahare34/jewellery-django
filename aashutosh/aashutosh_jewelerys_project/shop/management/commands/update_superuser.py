from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Updates the superuser credentials'

    def handle(self, *args, **kwargs):
        # Try to get or create the superuser
        try:
            # First try to delete existing superusers if needed, or update
            user, created = User.objects.update_or_create(
                username='aashutosh',
                defaults={
                    'is_superuser': True,
                    'is_staff': True,
                    'is_active': True,
                }
            )
            user.set_password('aashutosh@1829')
            user.save()
            
            if created:
                self.stdout.write(self.style.SUCCESS('Successfully created superuser "aashutosh"!'))
            else:
                self.stdout.write(self.style.SUCCESS('Successfully updated superuser "aashutosh"!'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
