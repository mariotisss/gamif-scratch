# Generated by Django 5.2 on 2025-05-21 13:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('copilot_metrics', '0002_remove_fields'),
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='copilotengagementmetric',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.team'),
        ),
    ]
