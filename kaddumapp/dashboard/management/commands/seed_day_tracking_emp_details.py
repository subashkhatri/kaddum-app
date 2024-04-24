# kaddumapp/management/commands/seed_day_tracking.py
from django.core.management.base import BaseCommand
from dashboard.models import DayTrackingEmployeeDetails
from datetime import date

class Command(BaseCommand):
    help = 'Seeds the database with Project'

    def handle(self, *args, **options):
        self.stdout.write('Seeding Project data...')

        records = [
        {
            'day_tracking_no': 1,
            'employee_name': 'Melissa Pettersson',
            'position': 'ERA Supervisor',
            'item_rate': 12.00,
            'start_time': '06:00',
            'end_time': '18:00',
            'total_hours': 12,
            'work_description': 'supervisor',
        },
        {
            'day_tracking_no': 1,
            'employee_name': 'Joseph Jeffries',
            'position': 'ERA Allrounder',
            'item_rate': 9.50,
            'start_time': '06:00',
            'end_time': '18:00',
            'total_hours': 12,
            'work_description': 'ERA Allrounder',
        },
        {
            'day_tracking_no': 1,
            'employee_name': 'Rik Erkelens',
            'position': 'ERA Moxy Operator',
            'item_rate': 8.70,
            'start_time': '06:00',
            'end_time': '18:00',
            'total_hours': 12,
            'work_description': 'ERA Moxy Operator',
        },
        ]

        for record_data in records:
            DayTrackingEmployeeDetails.objects.create(**record_data)

        self.stdout.write(self.style.SUCCESS('Successfully seeded Day Tracking Employee Details data!'))
