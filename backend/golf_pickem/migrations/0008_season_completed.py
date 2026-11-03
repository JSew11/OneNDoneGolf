from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf_pickem', '0007_alter_season_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='completed',
            field=models.BooleanField(default=False),
            preserve_default=True
        )
    ]
