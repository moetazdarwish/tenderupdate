# Generated by Django 4.0 on 2023-12-19 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_inventorytask'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventorytask',
            name='status',
            field=models.CharField(blank=True, default='PENDING', max_length=50, null=True),
        ),
    ]
