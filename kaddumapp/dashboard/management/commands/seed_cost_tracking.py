# kaddumapp/management/commands/seed_dairy_records.py
from django.core.management.base import BaseCommand
from dashboard.models import CostTracking, Project
from datetime import date, datetime

class Command(BaseCommand):
    help = 'Seeds the database with CostTracking data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding CostTracking data...')
        projects = {str(project.project_no): project for project in Project.objects.all()}

        records =  [
            {
                'cost_tracking_id':'CT00001',
                'project_no': projects['2425'],
                'record_date': date(2024, 5, 2),
                'year_week': '202417',
                'created_date':datetime(2024,5,2,10,20,30),
                'last_modification_date': datetime(2024,5,2,10,20,30),
                'is_draft': True,
                'total_hours_employee': 80,
                'total_hours_employee_local': 20,
                'total_hours_employee_local_percentage': 0.2,
                'total_hours_employee_indigenous': 10,
                'total_hours_employee_indigenous_percentage': 10,
                'total_amount_employee':0,
                'total_hours_equipment':0,
                'total_amount_equipment':0,     
            },
            {
                'cost_tracking_id':'CT00002',
                'project_no': projects['2425'],
                'record_date': date(2024, 5, 3),
                'year_week': '202417',
                'created_date':datetime(2024,5,3,10,20,30),
                'last_modification_date': datetime(2024,5,3,10,20,30),
                'is_draft': False,  
                'total_hours_employee': 80,
                'total_hours_employee_local': 20,
                'total_hours_employee_local_percentage': 0.2,
                'total_hours_employee_indigenous': 10,
                'total_hours_employee_indigenous_percentage': 10,
                'total_amount_employee':0,
                'total_hours_equipment':0,
                'total_amount_equipment':0,         
            },
        ]

        for record_data in records:
            CostTracking.objects.create(**record_data)

        self.stdout.write(self.style.SUCCESS('Successfully seeded CostTracking data!'))
