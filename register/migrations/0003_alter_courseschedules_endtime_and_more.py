# Generated by Django 5.0.4 on 2024-04-26 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_day_remove_courseschedules_days_courseschedules_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseschedules',
            name='endTime',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='courseschedules',
            name='startTime',
            field=models.TimeField(null=True),
        ),
    ]
