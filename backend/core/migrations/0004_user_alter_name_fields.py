from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_user_payment_method_user_referred_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=50, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=50, blank=True, null=True),
        ),
    ]