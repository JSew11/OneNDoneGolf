# Generated by Django 5.0.1 on 2024-02-25 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='payment_method',
            field=models.CharField(choices=[('venmo', 'Venmo'), ('cash_app', 'Cash App'), ('paypal', 'PayPal'), ('zelle', 'Zelle')], default='venmo', max_length=16),
        ),
        migrations.AddField(
            model_name='user',
            name='referred_by',
            field=models.CharField(choices=[('other', 'Other')], default='other', max_length=32),
        ),
    ]
