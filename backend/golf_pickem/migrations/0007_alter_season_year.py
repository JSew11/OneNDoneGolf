from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('golf_pickem', '0006_tournament_external_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='season',
            name='year',
            field=models.SmallIntegerField(unique=True),
        ),
    ]
