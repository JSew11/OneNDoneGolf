# Generated by Django 5.0.6 on 2024-05-26 23:11

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Golfer',
            fields=[
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('^[a-zA-Z]+$')])),
                ('last_name', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('^[a-zA-Z .]+$')])),
                ('country', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('^[a-zA-Z .,]+$')])),
            ],
            options={
                'verbose_name': 'Golfer',
                'verbose_name_plural': 'Golfers',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('alias', models.CharField(max_length=255)),
                ('active', models.BooleanField(default=False)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Season',
                'verbose_name_plural': 'Seasons',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('alias', models.CharField(blank=True, max_length=4, null=True)),
                ('course', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Tournament',
                'verbose_name_plural': 'Tournaments',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='GolferSeason',
            fields=[
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('golfer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seasons', to='golf_pickem.golfer')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='golfers', to='golf_pickem.season')),
            ],
            options={
                'verbose_name': 'Golfer',
                'verbose_name_plural': 'Golfers',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Pick',
            fields=[
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('backup_selection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='backup_selections', to='golf_pickem.golfer')),
                ('primary_selection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='primary_selections', to='golf_pickem.golfer')),
                ('scored_golfer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='picked_by_history', to='golf_pickem.golfer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pick_history', to=settings.AUTH_USER_MODEL)),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pick_history', to='golf_pickem.season')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='picks', to='golf_pickem.tournament')),
            ],
            options={
                'verbose_name': 'Picks',
                'verbose_name_plural': 'Picks',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='TournamentSeason',
            fields=[
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('purse', models.PositiveIntegerField()),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule', to='golf_pickem.season')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seasons', to='golf_pickem.tournament')),
            ],
            options={
                'verbose_name': 'Tournament',
                'verbose_name_plural': 'Tournaments',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='TournamentGolfer',
            fields=[
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('position', models.PositiveSmallIntegerField(null=True)),
                ('prize_money', models.PositiveIntegerField(null=True)),
                ('golfer_season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tournaments', to='golf_pickem.golferseason')),
                ('tournament_season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='field', to='golf_pickem.tournamentseason')),
            ],
            options={
                'verbose_name': 'Tournament',
                'verbose_name_plural': 'Tournaments',
                'ordering': ['created'],
            },
        ),
        migrations.AddConstraint(
            model_name='golferseason',
            constraint=models.UniqueConstraint(condition=models.Q(('deleted__isnull', True)), fields=('golfer', 'season'), name='unique_golfer_season'),
        ),
        migrations.AddConstraint(
            model_name='pick',
            constraint=models.UniqueConstraint(condition=models.Q(('deleted__isnull', True)), fields=('user', 'tournament', 'season'), name='unique_user_tournament_season'),
        ),
        migrations.AddConstraint(
            model_name='pick',
            constraint=models.UniqueConstraint(condition=models.Q(('deleted__isnull', True)), fields=('user', 'scored_golfer', 'season'), name='unique_user_golfer_season'),
        ),
        migrations.AddConstraint(
            model_name='tournamentseason',
            constraint=models.UniqueConstraint(condition=models.Q(('deleted__isnull', True)), fields=('tournament', 'season'), name='unique_tournament_season'),
        ),
        migrations.AddConstraint(
            model_name='tournamentgolfer',
            constraint=models.UniqueConstraint(condition=models.Q(('deleted__isnull', True)), fields=('tournament_season', 'golfer_season'), name='unique_tournament_golfer'),
        ),
    ]
