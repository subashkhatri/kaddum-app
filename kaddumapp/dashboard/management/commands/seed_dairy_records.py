# kaddumapp/management/commands/seed_dairy_records.py
from django.core.management.base import BaseCommand
from dashboard.models import DairyRecord
from datetime import date

class Command(BaseCommand):
    help = 'Seeds the database with DairyRecord data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding DairyRecord data...')

        records = [
            {
                'diary_record_id': 'REC001',
                'record_date': date.today(),
                'record_shift': 'Morning',
                'activity_discussion': 'Discussed daily activities.',
                'safety_issue_discussion': 'No safety issues.',
                'instruction_from_client': 'Follow the plan.',
                'visitor_on_site': 'No visitors.',
                'daily_progress_description': 'Good progress.',
                'record_comment': 'No comments.',
                'handover_note': 'Handed over to next shift.',
            },
             {
                'diary_record_id': 'REC002',
                'record_date': date.today(),
                'record_shift': 'afternoon',
                'activity_discussion': 'Discussed daily activities.',
                'safety_issue_discussion': 'No safety issues.',
                'instruction_from_client': 'Follow the plan.',
                'visitor_on_site': '4 visitors.',
                'daily_progress_description': 'Best progress.',
                'record_comment': 'Add supervisor.',
                'handover_note': 'Handed over to next shift.',
            },
        ]

        for record_data in records:
            DairyRecord.objects.create(**record_data)

        self.stdout.write(self.style.SUCCESS('Successfully seeded DairyRecord data!'))
