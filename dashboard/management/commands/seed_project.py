# kaddumapp/management/commands/seed_day_tracking.py
from django.core.management.base import BaseCommand
from dashboard.models import Project
from datetime import date, datetime

class Command(BaseCommand):
    help = 'Seeds the database with Project'

    def handle(self, *args, **options):
        self.stdout.write('Seeding Project data...')

        records = [
            {
                'project_no': 2424,
                'purchase_order_no': None,
                'project_name': 'Delta Electrical Generator Pad',
                'client': 'Delta Electrics',
                'project_start_date': date(2024, 4, 1),
                'project_end_date': date(2024, 5, 30),
                'project_budget': 250050,
                'project_total_cost': 0,
                'created_date':datetime(2024,4,1,10,20,30),
                'last_modification_date':datetime(2024,4,1,10,20,30),
                'is_active': False,
            },
             {
                'project_no': 2425,
                'purchase_order_no': '3105775901',
                'project_name': 'ERA General Civil Works',
                'client': 'Energy Resources Australia',
                'project_start_date': date(2024, 4, 1),
                'project_end_date': date(2024, 5, 30),
                'project_budget': 500000,
                'project_total_cost': 0,
                'created_date':datetime(2024,4,1,16,20,30),
                'last_modification_date':datetime(2024,4,1,16,20,30),
                'is_active': True,
            },
            {
                'project_no': 2426,
                'purchase_order_no': '??',
                'project_name': 'ERA Tip Head Works',
                'client': 'Energy Resources Australia',
                'project_start_date': date(2024, 5, 1),
                'project_end_date': date(2024, 6, 30),
                'project_budget': 100000,
                'project_total_cost': 0,
                'created_date':datetime(2024,4,1,10,20,30),
                'last_modification_date':datetime(2024,5,1,10,20,30),
                'is_active': True,
            },
            {
                'project_no': 2430,
                'purchase_order_no': '3106027588',
                'project_name': 'ERA 009 Spillway & Road Repairs',
                'client': 'Energy Resources Australia',
                'project_start_date': date(2024, 1, 1),
                'project_end_date': date(2024, 2, 18),
                'project_budget': 5000,
                'project_total_cost': 0,
                'created_date':datetime(2024,1,1,10,20,30),
                'last_modification_date':datetime(2024,1,20,20,20,30),
                'is_active': True,
            },
            {
                'project_no': 2437,
                'purchase_order_no': 'Not Applicable',
                'project_name': 'Pit 3 Dewatering Filters',
                'client': 'Bell Environmental',
                'project_start_date': date(2024, 6, 1),
                'project_end_date': date(2024, 9, 1),
                'project_budget': 250000,
                'project_total_cost': 0,
                'created_date':datetime(2024,5,1,12,20,30),
                'last_modification_date':datetime(2024,6,1,10,20,30),
                'is_active': True,
            },
            {
                'project_no': 2439,
                'purchase_order_no': 'Not Applicable',
                'project_name': 'ERA office Plans',
                'client': 'Energy Resources Australia',
                'project_start_date': date(2024, 8, 1),
                'project_end_date': date(2024, 9, 1),
                'project_budget': 350000,
                'project_total_cost': 0,
                'created_date':datetime(2024,8,1,10,20,30),
                'last_modification_date':datetime(2024,8,1,10,20,30),
                'is_active': True,
            },
        ]

        for record_data in records:
            Project.objects.create(**record_data)

        self.stdout.write(self.style.SUCCESS('Successfully seeded Project data!'))
