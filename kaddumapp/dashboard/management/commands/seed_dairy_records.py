from django.core.management.base import BaseCommand
from dashboard.models import DairyRecord, Project, UserAccount
from datetime import date, datetime

class Command(BaseCommand):
    help = 'Seeds the database with DairyRecord data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding DairyRecord data...')

        # Fetch all Project instances and create a dictionary with project_no as key
        projects = {str(project.project_no): project for project in Project.objects.all()}
        
        # Fetch all UserAccount instances and create a dictionary with username as key
        supervisors = {supervisor.username: supervisor for supervisor in UserAccount.objects.all()}

        records =  [
            {
                'dairy_record_id': 'DR00001',
                'project_no': projects['2425'],  # Fetch Project instance by project_no
                'record_date': date(2024, 5, 2),
                'record_shift': 'Day Shift',
                'supervisor_id': supervisors['KD0001'],  # Fetch UserAccount instance by username
                'activity_discussion': 'Activity discussion details here.',
                'safety_issue_discussion': 'Safety issue discussion details here.',
                'instruction_from_client': 'Instructions from client here.',
                'visitor_on_site': None,
                'daily_progress_description': 'Daily progress description here.',
                'record_comment': 'Record comment here.',
                'handover_note': 'Handover note here.',
                'created_date':datetime(2024,5,2,10,20,30),
                'last_modification_date': datetime(2024,5,2,10,20,30),
                'delay_access': True,
                'delay_lack_of_drawing': False,
                'delay_await_client_decision': False,
                'delay_poor_weather': False,
                'delay_industrial_matters': False,
                'delay_await_client_instruction': False,
                'delay_subcontractors': True,
                'delay_await_materials': False,
                'delay_rework': False,
                'delay_other': None,
                'delay_details': 'out of stock',
                'jha_qty': 3,
                'ccc_qty': 1,
                'take5_qty': 1,
                'stop_seek_qty': 0,
                'mobilised_qty': 2,
                'non_manual_qty': 1,
                'manual_qty': 1,
                'subcontractor_qty': 1,
                'incident_qty': 1,
                'near_miss_qty': 1,
                'first_aid_qty': 2,
                'medically_treated_injury_qty': 1,
                'loss_time_injury_qty': 0,
                'is_draft':False,
            },
            {
                'dairy_record_id': 'DR00002',
                'project_no': projects['2425'],  # Fetch Project instance by project_no
                'record_date': date(2024, 5, 2),
                'record_shift': 'Night Shift',
                'supervisor_id': supervisors['KD0001'],  # Fetch UserAccount instance by username
                'activity_discussion': 'Activity discussion details here.',
                'safety_issue_discussion': 'Safety issue discussion details here.',
                'instruction_from_client': 'Instructions from client here.',
                'visitor_on_site': None,
                'daily_progress_description': 'Daily progress description here.',
                'record_comment': 'Record comment here.',
                'handover_note': 'Handover note here.',
                'created_date':datetime(2024,5,3,18,20,30),
                'last_modification_date': datetime(2024,5,3,18,20,30),
                'delay_access': True,
                'delay_lack_of_drawing': False,
                'delay_await_client_decision': False,
                'delay_poor_weather': False,
                'delay_industrial_matters': False,
                'delay_await_client_instruction': False,
                'delay_subcontractors': True,
                'delay_await_materials': True,
                'delay_rework': True,
                'delay_other': None,
                'delay_details': 'out of stock',
                'jha_qty': 3,
                'ccc_qty': 1,
                'take5_qty': 1,
                'stop_seek_qty': 0,
                'mobilised_qty': 2,
                'non_manual_qty': 1,
                'manual_qty': 1,
                'subcontractor_qty': 1,
                'incident_qty': 1,
                'near_miss_qty': 1,
                'first_aid_qty': 2,
                'medically_treated_injury_qty': 1,
                'loss_time_injury_qty': 0,
                'is_draft':False,
            },
            {
                'dairy_record_id': 'DR00003',
                'project_no': projects['2425'],  # Fetch Project instance by project_no
                'record_date': date(2024, 5, 3),
                'record_shift': 'Day Shift',
                'supervisor_id': supervisors['KD0002'],  # Fetch UserAccount instance by username
                'activity_discussion': 'Activity discussion details here.',
                'safety_issue_discussion': 'Safety issue discussion details here.',
                'instruction_from_client': 'Instructions from client here.',
                'visitor_on_site': None,
                'daily_progress_description': 'Daily progress description here.',
                'record_comment': 'Record comment here.',
                'handover_note': 'Handover note here.',
                'created_date':datetime(2024,5,3,10,20,30),
                'last_modification_date': datetime(2024,5,3,10,20,30),
                'delay_access': True,
                'delay_lack_of_drawing': False,
                'delay_await_client_decision': False,
                'delay_poor_weather': False,
                'delay_industrial_matters': False,
                'delay_await_client_instruction': False,
                'delay_subcontractors': True,
                'delay_await_materials': True,
                'delay_rework': True,
                'delay_other': None,
                'delay_details': 'out of stock',
                'jha_qty': 3,
                'ccc_qty': 1,
                'take5_qty': 1,
                'stop_seek_qty': 0,
                'mobilised_qty': 2,
                'non_manual_qty': 1,
                'manual_qty': 1,
                'subcontractor_qty': 1,
                'incident_qty': 1,
                'near_miss_qty': 1,
                'first_aid_qty': 2,
                'medically_treated_injury_qty': 1,
                'loss_time_injury_qty': 0,
                'is_draft':True,
            },
        ]

        for record_data in records:
            DairyRecord.objects.create(**record_data)

        self.stdout.write(self.style.SUCCESS('Successfully seeded DairyRecord data!'))
