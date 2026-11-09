from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf_pickem', '0008_season_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='golfer',
            name='external_id',
            field=models.CharField(max_length=16, default=9999999999999999),
            preserve_default=False
        )
    ]
