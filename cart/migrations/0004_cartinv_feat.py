# Generated by Django 4.0 on 2023-12-11 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0012_kitchenjobsassign_feat'),
        ('cart', '0003_cartsubproducts'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartinv',
            name='feat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kitchen.recipefeatuers'),
        ),
    ]
