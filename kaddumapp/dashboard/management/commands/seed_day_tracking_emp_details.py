# kaddumapp/management/commands/seed_day_tracking.py
from django.core.management.base import BaseCommand
from dashboard.models import DayTrackingEmployeeDetails, UserAccount, DayTracking, ResourceCost
from datetime import date

class Command(BaseCommand):
    help = 'Seeds the database with Project'

    def handle(self, *args, **options):
        self.stdout.write('Seeding Project data...')

        # Fetch all DayTracking instances and create a dictionary with day_tracking_no as key
        day_trackings = {str(day_tracking.day_tracking_id): day_tracking for day_tracking in DayTracking.objects.all()}

        # Fetch all UserAccount instances and create a dictionary with employee_id as key
        employees = {str(employee.username): employee for employee in UserAccount.objects.all()}

        # Fetch all ResourceCost instances and create a dictionary with position_id as key
        positions = {str(position.resource_id): position for position in ResourceCost.objects.all()}

        
        records = [
        {
            'id': '1',
            'day_tracking_id': day_trackings['DS00001'],
            'employee_id': employees['KD0001'],
            'position_id': positions['1'],
            'start_time': '06:00',
            'end_time': '18:00',
            'total_hours': 12,
            'work_description': 'supervisor',
            'hour_rate': 10,
            'total_amount': 120,
            'confirmed_position_id': positions['1'],
        },
        {
            'id': '2',
            'day_tracking_id': day_trackings['DS00001'],
            'employee_id': employees['KD0002'],
            'position_id': positions['2'],
            'start_time': '06:00',
            'end_time': '18:00',
            'total_hours': 12,
            'work_description': 'ERA Allrounder',
            'hour_rate': 9,
            'total_amount': 108,
            'confirmed_position_id': positions['4'],
        },
        {
            'id': '3',
            'day_tracking_id': day_trackings['DS00002'],
            'employee_id': employees['KD0003'],
            'position_id': positions['3'],
            'start_time': '06:00',
            'end_time': '18:00',
            'total_hours': 12,
            'work_description': 'ERA Moxy Operator',
            'hour_rate': 5,
            'total_amount': 60,
            'confirmed_position_id': positions['6'],
        },
        {
            'id': '4',
            'day_tracking_id': day_trackings['DS00002'],
            'employee_id': employees['KD0001'],
            'position_id': positions['1'],
            'start_time': '06:00',
            'end_time': '18:00',
            'total_hours': 12,
            'work_description': 'supervisor',
            'hour_rate': 10,
            'total_amount': 120,
            'confirmed_position_id': positions['1'],
        },
        {
            'id': '5',
            'day_tracking_id': day_trackings['DS00002'],
            'employee_id': employees['KD0002'],
            'position_id': positions['2'],
            'start_time': '06:00',
            'end_time': '18:00',
            'total_hours': 12,
            'work_description': 'ERA Allrounder',
            'hour_rate': 9,
            'total_amount': 108,
            'confirmed_position_id': positions['4'],
        },
        {
            'id': '6',
            'day_tracking_id': day_trackings['DS00002'],
            'employee_id': employees['KD0003'],
            'position_id': positions['3'],
            'start_time': '06:00',
            'end_time': '18:00',
            'total_hours': 12,
            'work_description': 'ERA Moxy Operator',
            'hour_rate': 5,
            'total_amount': 60,
            'confirmed_position_id': positions['4'],
        },
        {
            'id': '7',
            'day_tracking_id': day_trackings['DS00002'],
            'employee_id': employees['KD0004'],
            'position_id': positions['4'],
            'start_time': '06:00',
            'end_time': '18:00',
            'total_hours': 12,
            'work_description': 'ERA Moxy Operator',
            'hour_rate': 5,
            'total_amount': 60,
            'confirmed_position_id': positions['5'],
        },
        {
            'id': '8',
            'day_tracking_id': day_trackings['DS00002'],
            'employee_id': employees['KD0005'],
            'position_id': positions['5'],
            'start_time': '06:00',
            'end_time': '18:00',
            'total_hours': 12,
            'work_description': 'ERA Moxy Operator',
            'hour_rate': 5,
            'total_amount': 60,
            'confirmed_position_id': positions['6'],
        },
        {
            'id': '9',
            'day_tracking_id': day_trackings['DS00003'],
            'employee_id': employees['KD0001'],
            'position_id': positions['1'],
            'start_time': '06:00',
            'end_time': '18:00',
            'total_hours': 12,
            'work_description': 'supervisor',
            'hour_rate': 10,
            'total_amount': 120,
            'confirmed_position_id': positions['1'],
        },
        {
            'id': '10',
            'day_tracking_id': day_trackings['DS00003'],
            'employee_id': employees['KD0002'],
            'position_id': positions['2'],
            'start_time': '06:00',
            'end_time': '18:00',
            'total_hours': 12,
            'work_description': 'ERA Allrounder',
            'hour_rate': 9,
            'total_amount': 108,
            'confirmed_position_id': positions['4'],
        },
        {
            'id': '11',
            'day_tracking_id': day_trackings['DS00003'],
            'employee_id': employees['KD0003'],
            'position_id': positions['3'],
            'start_time': '06:00',
            'end_time': '18:00',
            'total_hours': 12,
            'work_description': 'ERA Moxy Operator',
            'hour_rate': 5,
            'total_amount': 60,
            'confirmed_position_id': positions['6'],
        },
        {
            'id': '12',
            'day_tracking_id': day_trackings['DS00004'],
            'employee_id': employees['KD0003'],
            'position_id': positions['3'],
            'start_time': '06:00',
            'end_time': '18:00',
            'total_hours': 12,
            'work_description': 'ERA Moxy Operator',
            'hour_rate': 5,
            'total_amount': 60,
            'confirmed_position_id': positions['6'],
        },
        ]

        for record_data in records:
            DayTrackingEmployeeDetails.objects.create(**record_data)

        self.stdout.write(self.style.SUCCESS('Successfully seeded Day Tracking Employee Details data!'))
