# kaddumapp/management/commands/seed_day_tracking.py
from django.core.management.base import BaseCommand
from dashboard.models import DayTrackingResourceDetails
from datetime import date

class Command(BaseCommand):
    help = 'Seeds the database with Project'

    def handle(self, *args, **options):
        self.stdout.write('Seeding Project data...')

        records = [
        {
            'day_tracking_no': 1,
            'item_type': 'car',
            'item_name': 'Toyata Hilux Dual Cab',
            'item_rate': 15.00,
            'start_time': '06:00',
            'end_time': '18:00',
            'total_hours': 12,
            'work_description': 'Toyata Hilux Dual Cab',
        },
        {
            'day_tracking_no': 1,
            'item_type': 'truck',
            'item_name': 'Isuzu 10m Body Tipper',
            'item_rate': 45.00,
            'start_time': '06:00',
            'end_time': '18:00',
            'total_hours': 12,
            'work_description': 'Isuzu 10m Body Tipper',
        },
        ]

        for record_data in records:
            DayTrackingResourceDetails.objects.create(**record_data)

        self.stdout.write(self.style.SUCCESS('Successfully seeded Day Tracking Resource Details data!'))
