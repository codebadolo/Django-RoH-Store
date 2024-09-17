from currencies.models import Currency
from user.models import UserProfile
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create a user with a profile'

    def handle(self, *args, **kwargs):
        # Ensure there's a currency to assign
        currency, created = Currency.objects.get_or_create(code="USD", defaults={"name": "US Dollar", "symbol": "$", "factor": 1.00})

        # Create the user
        user, created = User.objects.get_or_create(
            username='Hien',
            defaults={
                'first_name': 'Hien',
                'last_name': 'Nguyen',
                'email': 'hien@example.com',
            }
        )
        
        if created:
            user.set_password('Hien12345!')  # Set a random password or hardcoded
            user.save()

            # Create user profile and assign the currency
            profile = UserProfile.objects.create(
                user=user,
                phone='+1234567890',
                address='123 Random St',
                city='Random City',
                country='Random Country',
                image='images/users/default.png',
                currency=currency  # Assigning the currency created or retrieved
            )

            self.stdout.write(self.style.SUCCESS(f"User 'Hien' created with password: Hien12345!"))
        else:
            self.stdout.write(self.style.WARNING(f"User 'Hien' already exists!"))
