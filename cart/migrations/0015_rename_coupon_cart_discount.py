# Generated by Django 4.0 on 2023-12-13 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0014_cart_customer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='coupon',
            new_name='discount',
        ),
    ]
