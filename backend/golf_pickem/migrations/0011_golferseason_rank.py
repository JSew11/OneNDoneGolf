from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf_pickem', '0010_remove_golfer_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='GolferSeason',
            name='rank',
            field=models.PositiveIntegerField(blank=True, null=True)
        )
    ]
