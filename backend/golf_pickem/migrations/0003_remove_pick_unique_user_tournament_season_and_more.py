# Generated by Django 5.0.6 on 2024-08-22 23:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf_pickem', '0002_userseason_userseason_unique_user_season'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='pick',
            name='unique_user_tournament_season',
        ),
        migrations.RemoveConstraint(
            model_name='pick',
            name='unique_user_golfer_season',
        ),
        migrations.RemoveField(
            model_name='pick',
            name='season',
        ),
        migrations.RemoveField(
            model_name='pick',
            name='user',
        ),
        migrations.AddField(
            model_name='pick',
            name='user_season',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='pick_history', to='golf_pickem.userseason'),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='pick',
            constraint=models.UniqueConstraint(condition=models.Q(('deleted__isnull', True)), fields=('user_season', 'tournament'), name='unique_user_tournament_season'),
        ),
        migrations.AddConstraint(
            model_name='pick',
            constraint=models.UniqueConstraint(condition=models.Q(('deleted__isnull', True)), fields=('user_season', 'scored_golfer'), name='unique_user_golfer_season'),
        ),
    ]