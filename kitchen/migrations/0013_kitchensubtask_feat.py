# Generated by Django 4.0 on 2023-12-17 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0012_kitchenjobsassign_feat'),
    ]

    operations = [
        migrations.AddField(
            model_name='kitchensubtask',
            name='feat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kitchen.recipefeatuers'),
        ),
    ]