# Generated by Django 5.0.4 on 2024-04-20 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_dairyrecord_client_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dairyrecord',
            name='is_draft',
            field=models.BooleanField(default=True),
        ),
    ]
