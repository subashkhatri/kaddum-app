# kaddumapp/management/commands/seed_day_tracking.py
from django.core.management.base import BaseCommand
from dashboard.models import DayTracking
from datetime import date

class Command(BaseCommand):
    help = 'Seeds the database with DayTracking data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding DayTracking data...')

        records = [
            {
                'project_no': '2439',
                'record_date': date(2024, 2, 5),
                'record_day': 'dayshift',
                'record_shift': 'Dust Mitigation Pit 3',
                'work_area': 'Dust Mitigation Pit 3',
                'client_representative': 'Jsysen Roach',
                'weather': 'hot and humid',
                'comments': 'no',
                'kaddum_name': 'Kabi',
                'kaddum_sign': 'Kabi',
                'kaddum_sign_date': date(2024, 2, 5),
                'client_name': 'Jsysen Roach',
                'client_sign': 'Jsysen Roach',
                'client_sign_date': date(2024, 2, 5),
                'record_created_date': date(2024, 2, 5),
                'record_submitted_date': date(2024, 2, 5),
                'is_draft': False,
            },
            {
                'project_no': '2439',
                'record_date': date(2024, 2, 5),
                'record_day': 'nightshift',
                'record_shift': 'Dust Mitigation Pit 3',
                'work_area': 'Jsysen Roach',
                'client_representative': 'Jsysen Roach',
                'weather': 'hot and humid',
                'comments': 'no',
                'kaddum_name': 'chen',
                'kaddum_sign': 'chen',
                'kaddum_sign_date': date(2024, 2, 5),
                'client_name': 'Jsysen Roach',
                'client_sign': 'Jsysen Roach',
                'client_sign_date': date(2024, 2, 5),
                'record_created_date': date(2024, 2, 5),
                'record_submitted_date': date(2024, 2, 5),
                'is_draft': False,
            },
        ]

        for record_data in records:
            DayTracking.objects.create(**record_data)

        self.stdout.write(self.style.SUCCESS('Successfully seeded DayTracking data!'))
