# kaddumapp/management/commands/seed_day_tracking.py
from django.core.management.base import BaseCommand
from dashboard.models import DayTrackingEquipmentDetails,ResourceCost,DayTracking
from datetime import date

class Command(BaseCommand):
    help = 'Seeds the database with Project'

    def handle(self, *args, **options):
        self.stdout.write('Seeding Project data...')

        # Fetch all DayTracking instances and create a dictionary with day_tracking_no as key
        day_trackings = {str(day_tracking.day_tracking_id): day_tracking for day_tracking in DayTracking.objects.all()}

        # Fetch all ResourceCost instances and create a dictionary with position_id as key
        resources = {str(resource.resource_id): resource for resource in ResourceCost.objects.all()}

        records = [
        {
            'id':'1',
            'day_tracking_id': day_trackings['DS00001'],
            'resource_id': resources['21'],
            'start_time': '06:00',
            'end_time': '18:00',
            'total_hours': 12,
            'work_description': 'Toyata Hilux Dual Cab',
        },
        {
            'id':'2',
            'day_tracking_id': day_trackings['DS00001'],
            'resource_id': resources['25'],
            'start_time': '06:00',
            'end_time': '18:00',
            'total_hours': 12,
            'work_description': 'Isuzu 10m Body Tipper',
        },
        ]

        for record_data in records:
            DayTrackingEquipmentDetails.objects.create(**record_data)

        self.stdout.write(self.style.SUCCESS('Successfully seeded Day Tracking Resource Details data!'))
