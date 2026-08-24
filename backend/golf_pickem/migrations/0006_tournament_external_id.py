from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf_pickem', '0006_tournament_external_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='external_id',
            field=models.CharField(max_length=3, default=999),
            preserve_default=False
        )
    ]
