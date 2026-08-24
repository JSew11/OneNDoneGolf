from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf_pickem', '0005_season_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='external_id',
            field=models.CharField(max_length=3, default=999),
            preserve_default=False
        )
    ]
