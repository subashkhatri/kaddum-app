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
                'purchase_order_no': 'Not Applicable',
                'project_name': 'Delta Electrical Generator Pad',
                'client': 'Delta Electrics',
                'project_start_date': None,
                'project_end_date': None,
                'project_budget': None,
                'project_total_cost': 0,
                'created_date':datetime(2024,7,1,00,00,00),
                'last_modification_date':datetime(2024,7,1,00,00,00),
                'is_active': True,
            },
             {
                'project_no': 2425,
                'purchase_order_no': '3105775901',
                'project_name': 'ERA General Civil Works',
                'client': 'Energy Resources Australia',
                'project_start_date': None,
                'project_end_date': None,
                'project_budget': None,
                'project_total_cost': 0,
                'created_date':datetime(2024,7,1,00,00,00),
                'last_modification_date':datetime(2024,7,1,00,00,00),
                'is_active': True,
            },
            {
                'project_no': 2448,
                'purchase_order_no': '3106122049',
                'project_name': 'ERA supply Civil works operator',
                'client': 'Energy Resources Australia',
                'project_start_date': None,
                'project_end_date': None,
                'project_budget': 228228,
                'project_total_cost': 0,
                'created_date':datetime(2024,7,1,00,00,00),
                'last_modification_date':datetime(2024,7,1,00,00,00),
                'is_active': True,
            },
            {
                'project_no': 2449,
                'purchase_order_no': '3106076780',
                'project_name': 'Tailings Dam Crest Repairs',
                'client': 'Energy Resources Australia',
                'project_start_date': None,
                'project_end_date': None,
                'project_budget': 114877.4,
                'project_total_cost': 0,
                'created_date':datetime(2024,7,1,00,00,00),
                'last_modification_date':datetime(2024,7,1,00,00,00),
                'is_active': True,
            },
            {
                'project_no': 2451 ,
                'purchase_order_no': '3105775901',
                'project_name': 'ERA Tip Head Works',
                'client': 'Energy Resources Australia',
                'project_start_date': None,
                'project_end_date': None,
                'project_budget': 123189,
                'project_total_cost': 0,
                'created_date':datetime(2024,7,1,00,00,00),
                'last_modification_date':datetime(2024,7,1,00,00,00),
                'is_active': True,
            },
            {
                'project_no': 2455 ,
                'purchase_order_no': '3106027588',
                'project_name': 'ERA 009 Spillway & Road Repairs',
                'client': 'Energy Resources Australia',
                'project_start_date': None,
                'project_end_date': None,
                'project_budget': 49434,
                'project_total_cost': 0,
                'created_date':datetime(2024,7,1,00,00,00),
                'last_modification_date':datetime(2024,7,1,00,00,00),
                'is_active': True,
            },
            {
                'project_no': 2456,
                'purchase_order_no': 'DNP-KNP-2324-066',
                'project_name': 'Patonga Road Works',
                'client': 'Parks Australia',
                'project_start_date': None,
                'project_end_date': None,
                'project_budget': 90000,
                'project_total_cost': 0,
                'created_date':datetime(2024,7,1,00,00,00),
                'last_modification_date':datetime(2024,7,1,00,00,00),
                'is_active': True,
            },
            {
                'project_no': 2457,
                'purchase_order_no': 'Not Applicable',
                'project_name': 'Whistle duck road repairs',
                'client': 'Gundjeihmi Association',
                'project_start_date': None,
                'project_end_date': None,
                'project_budget': None,
                'project_total_cost': 0,
                'created_date':datetime(2024,7,1,00,00,00),
                'last_modification_date':datetime(2024,7,1,00,00,00),
                'is_active': True,
            },
        ]

        for record_data in records:
            Project.objects.create(**record_data)

        self.stdout.write(self.style.SUCCESS('Successfully seeded Project data!'))
