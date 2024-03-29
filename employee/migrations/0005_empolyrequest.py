# Generated by Django 4.0 on 2023-12-03 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('employee', '0004_empolysalary'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmpolyRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('decription', models.CharField(blank=True, max_length=150, null=True)),
                ('action', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('create', models.DateTimeField(auto_now_add=True)),
                ('name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employee.employeedetail')),
                ('request_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]
