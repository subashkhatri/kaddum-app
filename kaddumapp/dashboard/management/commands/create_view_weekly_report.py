from django.db import connection
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Seeds the database with CostTracking data'

    def handle(self, *args, **kwargs):
        self.create_weekly_statistics_view()

    def create_weekly_statistics_view(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE VIEW weekly_statistics_view AS
                SELECT
                    dr.year_week,
                    dr.project_no,
                    p.project_name,
                    DATE_TRUNC('week', (TO_DATE(dr.year_week, 'IYYYIW') - EXTRACT(DOW FROM TO_DATE(dr.year_week, 'IYYYIW'))::INTEGER * INTERVAL '1 day')) AS start_date_of_week,
                    DATE_TRUNC('week', (TO_DATE(dr.year_week, 'IYYYIW') - EXTRACT(DOW FROM TO_DATE(dr.year_week, 'IYYYIW'))::INTEGER * INTERVAL '1 day')) + INTERVAL '6 days' AS end_date_of_week,
                    COUNT(CASE WHEN NOT dr.is_draft THEN 1 END) AS total_records_of_the_week,
                    SUM(CASE WHEN NOT dr.is_draft THEN dr.jha_qty ELSE 0 END) AS sum_of_jha_qty,
                    SUM(CASE WHEN NOT dr.is_draft THEN dr.ccc_qty ELSE 0 END) AS sum_of_ccc_qty,
                    SUM(CASE WHEN NOT dr.is_draft THEN dr.take5_qty ELSE 0 END) AS sum_of_take5_qty,
                    SUM(CASE WHEN NOT dr.is_draft THEN dr.stop_seek_qty ELSE 0 END) AS sum_of_stop_seek_qty,
                    SUM(CASE WHEN NOT dr.is_draft THEN dr.mobilised_qty ELSE 0 END) AS sum_of_mobilised_qty,
                    SUM(CASE WHEN NOT dr.is_draft THEN dr.non_manual_qty ELSE 0 END) AS sum_of_non_manual_qty,
                    SUM(CASE WHEN NOT dr.is_draft THEN dr.manual_qty ELSE 0 END) AS sum_of_manual_qty,
                    SUM(CASE WHEN NOT dr.is_draft THEN dr.subcontractor_qty ELSE 0 END) AS sum_of_subcontractor_qty,
                    SUM(CASE WHEN NOT dr.is_draft THEN dr.incident_qty ELSE 0 END) AS sum_of_incident_qty,
                    SUM(CASE WHEN NOT dr.is_draft THEN dr.near_miss_qty ELSE 0 END) AS sum_of_near_miss_qty,
                    SUM(CASE WHEN NOT dr.is_draft THEN dr.first_aid_qty ELSE 0 END) AS sum_of_first_aid_qty,
                    SUM(CASE WHEN NOT dr.is_draft THEN dr.medically_treated_injury_qty ELSE 0 END) AS sum_of_medically_treated_injury_qty,
                    SUM(CASE WHEN NOT dr.is_draft THEN dr.loss_time_injury_qty ELSE 0 END) AS sum_of_loss_time_injury_qty,
                    SUM(CASE WHEN NOT ct.is_draft THEN ct.total_hours_employee ELSE 0 END) AS total_hours_employee,
                    SUM(CASE WHEN NOT ct.is_draft THEN ct.total_hours_employee_local ELSE 0 END) AS total_hours_employee_local,
                    SUM(CASE WHEN NOT ct.is_draft THEN ct.total_hours_employee_indigenous ELSE 0 END) AS total_hours_employee_indigenous,
                    SUM(CASE WHEN NOT ct.is_draft THEN ct.total_amount_employee ELSE 0 END) AS total_amount_employee,
                    SUM(CASE WHEN NOT ct.is_draft THEN ct.total_hours_equipment ELSE 0 END) AS total_hours_equipment,
                    SUM(CASE WHEN NOT ct.is_draft THEN ct.total_amount_equipment ELSE 0 END) AS total_amount_equipment
                FROM
                    "dashboard-DairyRecord" dr
                INNER JOIN
                    "dashboard-Project" p ON dr.project_no = p.project_no
                LEFT JOIN
                    "dashboard-CostTracking" ct ON dr.project_no = ct.project_no
                GROUP BY
                    dr.year_week, dr.project_no, p.project_name;
            """)

        self.stdout.write(self.style.SUCCESS('Successfully Create Weekly Report View!'))
