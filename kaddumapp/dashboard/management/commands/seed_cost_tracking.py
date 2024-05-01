# kaddumapp/management/commands/seed_dairy_records.py
from django.core.management.base import BaseCommand
from dashboard.models import CostTracking
from datetime import date

class Command(BaseCommand):
    help = 'Seeds the database with CostTracking data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding CostTracking data...')

        records =  [
            {
                'project_no': '2425',
                'record_date': date(2024, 4, 22),
                'record_day': 'Monday',
                'year_week': '202417',
                'total_hours': 36,
                'local_hours': 12,
                'indigenous_hours': 12,
                'total_amount': 362.4,
                'local_amount': 144,
                'indigenous_amount': 114,
                'record_created_date': date(2024, 4, 22),
                'record_submitted_date': date(2024, 4, 22),
                'is_draft': False,               
            },
        ]

        for record_data in records:
            CostTracking.objects.create(**record_data)

        self.stdout.write(self.style.SUCCESS('Successfully seeded CostTracking data!'))
