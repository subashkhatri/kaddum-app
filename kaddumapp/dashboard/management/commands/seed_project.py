# kaddumapp/management/commands/seed_day_tracking.py
from django.core.management.base import BaseCommand
from dashboard.models import Project
from datetime import date

class Command(BaseCommand):
    help = 'Seeds the database with Project'

    def handle(self, *args, **options):
        self.stdout.write('Seeding Project data...')

        records = [
            {
                'project_no': '2424',
                'purchase_order_no': None,
                'project_name': 'Delta Electrical Generator Pad',
                'client': 'Delta Electrics',
                'project_start_date': None,
                'project_end_date': None,
                'project_budget': '50',
                'project_total_cost': None,
                'is_active': 'True',
            },
             {
                'project_no': '2425',
                'purchase_order_no': '3105775901',
                'project_name': 'ERA General Civil Works',
                'client': 'Energy Resources Australia',
                'project_start_date': None,
                'project_end_date': None,
                'project_budget': '50',
                'project_total_cost': None,
                'is_active': 'True',
            },
            {
                'project_no': '2426',
                'purchase_order_no': '??',
                'project_name': 'ERA Tip Head Works',
                'client': 'Energy Resources Australia',
                'project_start_date': None,
                'project_end_date': None,
                'project_budget': '50',
                'project_total_cost': None,
                'is_active': 'True',
            },
            {
                'project_no': '2430',
                'purchase_order_no': '3106027588',
                'project_name': 'ERA 009 Spillway & Road Repairs',
                'client': 'Energy Resources Australia',
                'project_start_date': None,
                'project_end_date': None,
                'project_budget': '50',
                'project_total_cost': None,
                'is_active': 'True',
            },
            {
                'project_no': '2437',
                'purchase_order_no': 'Not Applicable',
                'project_name': 'Pit 3 Dewatering Filters',
                'client': 'Bell Environmental',
                'project_start_date': None,
                'project_end_date': None,
                'project_budget': '50',
                'project_total_cost': None,
                'is_active': 'True',
            },
            {
                'project_no': '2439',
                'purchase_order_no': 'Not Applicable',
                'project_name': 'ERA office Plans',
                'client': 'Energy Resources Australia',
                'project_start_date': None,
                'project_end_date': None,
                'project_budget': '50',
                'project_total_cost': None,
                'is_active': 'True',
            },
        ]

        for record_data in records:
            Project.objects.create(**record_data)

        self.stdout.write(self.style.SUCCESS('Successfully seeded Project data!'))
