from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Seed roles (groups) for Smart E-Commerce Platform'

    def handle(self, *args, **kwargs):
        # Create Admin group
        admin_group, created = Group.objects.get_or_create(name='Admin')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Admin group'))
        
        # Create Customer group
        customer_group, created = Group.objects.get_or_create(name='Customer')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Customer group'))
        
        self.stdout.write(self.style.SUCCESS('Roles seeded successfully'))
