# Generated by Django 5.0.1 on 2024-02-03 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf_pickem', '0002_remove_season_year_season_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournamentseason',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tournamentseason',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]