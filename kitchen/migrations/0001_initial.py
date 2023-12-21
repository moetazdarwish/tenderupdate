# Generated by Django 4.0 on 2023-12-05 07:59

from django.db import migrations, models
import django.db.models.deletion
import kitchen.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employee', '0007_employeedetail_owner_alter_empolyrequest_request_by'),
        ('inventory', '0002_inventory_avg_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('receipt', models.TextField(blank=True, null=True)),
                ('quantity', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('unit', models.CharField(blank=True, max_length=10, null=True)),
                ('min_level', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='KitCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cate', models.CharField(blank=True, max_length=100, null=True)),
                ('photo', models.FileField(blank=True, default='dePhoto.png', null=True, upload_to=kitchen.models.Kitchen_Products_path)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='KitchenRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('s_descrip', models.TextField(blank=True, null=True)),
                ('l_descrip', models.TextField(blank=True, null=True)),
                ('quantity', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('unit', models.CharField(blank=True, max_length=10, null=True)),
                ('min_level', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('pause', models.BooleanField(blank=True, default=False, null=True)),
                ('photo', models.FileField(blank=True, default='dePhoto.png', null=True, upload_to=kitchen.models.Kitchen_Products_path)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('cate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kitchen.kitcategory')),
            ],
        ),
        migrations.CreateModel(
            name='SubKitchenRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('ingredient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kitchen.ingredients')),
                ('raw', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.rawproducts')),
                ('sub', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kitchen.kitchenrecipe')),
            ],
        ),
        migrations.CreateModel(
            name='SubIngredients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('ingre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ingre', to='kitchen.ingredients')),
                ('items', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.rawproducts')),
                ('sub', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub', to='kitchen.ingredients')),
            ],
        ),
        migrations.CreateModel(
            name='KitchenJobsAssign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patch', models.CharField(blank=True, max_length=100, null=True)),
                ('quantity', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('descrp', models.TextField(blank=True, null=True)),
                ('ord_id', models.IntegerField(blank=True, default=0, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('duration', models.DurationField(blank=True, null=True)),
                ('j_stat', models.BooleanField(blank=True, default=False, null=True)),
                ('j_end', models.BooleanField(blank=True, default=False, null=True)),
                ('sale', models.BooleanField(blank=True, default=False, null=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('emply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employee.employeedetail')),
                ('ingrd', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kitchen.ingredients')),
                ('recipe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kitchen.kitchenrecipe')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='KitchenInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patch', models.CharField(blank=True, max_length=100, null=True)),
                ('cost', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('vrb_cost', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('q_in', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('q_out', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('fnsh', models.BooleanField(blank=True, default=False, null=True)),
                ('p_return', models.BooleanField(blank=True, default=False, null=True)),
                ('status', models.CharField(blank=True, max_length=10, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('cate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kitchen.kitcategory')),
                ('name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kitchen.kitchenrecipe')),
            ],
        ),
    ]