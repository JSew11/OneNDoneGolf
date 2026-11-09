from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('golf_pickem', '0009_golfer_external_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='golfer',
            name='country',
        ),
    ]
