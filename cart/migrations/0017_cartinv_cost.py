# Generated by Django 4.0 on 2023-12-17 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0016_cartname_inv'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartinv',
            name='cost',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
    ]
