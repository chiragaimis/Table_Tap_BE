from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = 'Seed superuser only for Smart E-Commerce Platform'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='superadmin').exists():
            User.objects.create(
                username='superadmin',
                email='superadmin@ecommerce.com',
                password=make_password('Admin@123'),
                is_superuser=True,
                is_staff=True,
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS('Created superadmin'))
        else:
            self.stdout.write(self.style.WARNING('Superadmin already exists'))

        self.stdout.write(self.style.SUCCESS('Seeding complete'))
