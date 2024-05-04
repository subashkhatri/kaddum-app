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
                'total_hours': 84,
                'total_hours_local': 12,
                'total_hours_indigenous': 12,
                'total_amount': 696,
                'created_date':datetime(2024,5,2,10,20,30),
                'last_modification_date': datetime(2024,5,2,10,20,30),
                'is_draft': True,               
            },
            {
                'cost_tracking_id':'CT00002',
                'project_no': projects['2425'],
                'record_date': date(2024, 5, 3),
                'year_week': '202417',
                'total_hours': 48,
                'total_hours_local': 12,
                'total_hours_indigenous': 12,
                'total_amount': 362.4,
                'created_date':datetime(2024,5,3,10,20,30),
                'last_modification_date': datetime(2024,5,3,10,20,30),
                'is_draft': False,               
            },
        ]

        for record_data in records:
            CostTracking.objects.create(**record_data)

        self.stdout.write(self.style.SUCCESS('Successfully seeded CostTracking data!'))
