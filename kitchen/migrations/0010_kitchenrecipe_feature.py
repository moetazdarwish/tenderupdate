# Generated by Django 4.0 on 2023-12-09 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0009_featuersprice_pause_recipeprice_pause'),
    ]

    operations = [
        migrations.AddField(
            model_name='kitchenrecipe',
            name='feature',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
