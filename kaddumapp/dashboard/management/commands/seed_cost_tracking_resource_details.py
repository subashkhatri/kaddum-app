# kaddumapp/management/commands/seed_day_tracking.py
from django.core.management.base import BaseCommand
from dashboard.models import CostingResourceDetails
from datetime import date

class Command(BaseCommand):
    help = 'Seeds the database with Project'

    def handle(self, *args, **options):
        self.stdout.write('Seeding Project data...')

        records = [
        {
            'cost_tracking_no': 1,
            'item_type': 'car',
            'item_name': 'Toyata Hilux Dual Cab',
            'item_rate': 15.00,
            'total_hours': 12,
            'total_amount': 180,
        },
        {
            'cost_tracking_no': 1,
            'item_type': 'truck',
            'item_name': 'Isuzu 10m Body Tipper',
            'item_rate': 45.00,
            'total_hours': 12,
            'total_amount': 540,
        },
        ]

        for record_data in records:
            CostingResourceDetails.objects.create(**record_data)

        self.stdout.write(self.style.SUCCESS('Successfully seeded Day Tracking Resource Details data!'))
