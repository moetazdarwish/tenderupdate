# Generated by Django 4.0 on 2023-12-17 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0018_invoiceref'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='invoice',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
