# Generated by Django 4.0 on 2023-12-18 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0010_advanceacc'),
    ]

    operations = [
        migrations.AddField(
            model_name='empolysalary',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
    ]
