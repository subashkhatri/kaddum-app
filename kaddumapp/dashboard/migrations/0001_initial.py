# Generated by Django 5.0.4 on 2024-04-07 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DairyRecord',
            fields=[
                ('diary_record_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('record_date', models.DateField()),
                ('record_shift', models.CharField(max_length=10)),
                ('activity_discussion', models.TextField(blank=True, null=True)),
                ('safety_issue_discussion', models.TextField(blank=True, null=True)),
                ('instruction_from_client', models.TextField(blank=True, null=True)),
                ('visitor_on_site', models.TextField(blank=True, null=True)),
                ('daily_progress_description', models.TextField(blank=True, null=True)),
                ('record_comment', models.TextField(blank=True, null=True)),
                ('handover_note', models.TextField(blank=True, null=True)),
                ('record_created_date', models.DateField(auto_now_add=True)),
                ('record_submitted_date', models.DateField(auto_now=True, null=True)),
            ],
        ),
    ]