# kaddumapp/management/commands/seed_day_tracking.py
from django.core.management.base import BaseCommand
from dashboard.models import CostingEmployeeDetails
from datetime import date

class Command(BaseCommand):
    help = 'Seeds the database with CostingEmployeeDetails'

    def handle(self, *args, **options):
        self.stdout.write('Seeding CostingEmployeeDetails data...')

        records = [
        {
            'cost_tracking_no': 1,
            'employee_name': 'Melissa Pettersson',
            'position': 'ERA Supervisor',
            'item_rate': 12.00,
            'total_hours': 12,
            'total_amount': 144,
        },
        {
            'cost_tracking_no': 1,
            'employee_name': 'Joseph Jeffries',
            'position': 'ERA Allrounder',
            'item_rate': 9.50,
            'total_hours': 12,
            'total_amount': 114,
        },
        {
            'cost_tracking_no': 1,
            'employee_name': 'Rik Erkelens',
            'position': 'ERA Moxy Operator',
            'item_rate': 8.70,
            'total_hours': 12,
            'total_amount': 104.4,
        },
        ]

        for record_data in records:
            CostingEmployeeDetails.objects.create(**record_data)

        self.stdout.write(self.style.SUCCESS('Successfully seeded Cost Tracking Employee Details data!'))
