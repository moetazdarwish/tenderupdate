# Generated by Django 4.0 on 2023-12-02 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeedetail',
            name='pwd',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
