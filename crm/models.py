from django.db import models

# Create your models here.

class CustomerDirectory(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)

class CustomerProfile(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    uuid = models.CharField(max_length=250, null=True, blank=True)
    direct = models.ForeignKey(CustomerDirectory, on_delete=models.CASCADE, null=True, blank=True)
    addres_0 = models.TextField(null=True, blank=True)
    addres_1 = models.TextField(null=True, blank=True)
    addres_2 = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    mail = models.CharField(max_length=150, null=True, blank=True)
    know_us = models.CharField(max_length=150, null=True, blank=True)
    code = models.CharField(max_length=50, null=True, blank=True)
    i_date = models.DateField( null=True, blank=True)
    vip = models.BooleanField(null=True, blank=True, default=False)
    famly = models.BooleanField(null=True, blank=True, default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} '

class CustomerDiscount(models.Model):
    name = models.CharField(null=True, blank=True, max_length=50)
    direct = models.ForeignKey(CustomerDirectory, on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(null=True, blank=True, max_length=15)
    vip = models.BooleanField(null=True, blank=True, default=False)
    famly = models.BooleanField(null=True, blank=True, default=False)
    new = models.BooleanField(null=True, blank=True, default=False)
    all = models.BooleanField(null=True, blank=True, default=False)
    site = models.BooleanField(null=True, blank=True, default=False)
    area_ds = models.BooleanField(null=True, blank=True, default=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    flat = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    close_date = models.DateField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)