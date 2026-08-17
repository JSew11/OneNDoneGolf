from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf_pickem', '0004_season_registration_cutoff'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='year',
            field=models.SmallIntegerField(default=2026),
            preserve_default=False
        ),
        migrations.RemoveField(
            model_name='season',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='season',
            name='end_date',
        ),
    ]
