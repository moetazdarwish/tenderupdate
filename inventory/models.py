from django.db import models
from django.db.models.signals import post_save

# Create your models here.
from employee.models import EmployeeDetail


class InvCategory(models.Model):
    cate = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.cate} '

class RawProducts(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    category = models.ForeignKey(InvCategory, on_delete=models.CASCADE, null=True, blank=True)
    unit = models.CharField(max_length=10, null=True, blank=True)
    qty = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    min_level = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    def __str__(self):
        return f'{self.name} '

class RawSuppliers(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    add = models.CharField(max_length=150, null=True, blank=True)
    delivery = models.BooleanField(default=False, null=True, blank=True)
    pym = models.CharField(max_length=20, null=True, blank=True)
    days = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'

class SuppliersProdList(models.Model):
    name = models.ForeignKey(RawSuppliers, on_delete=models.CASCADE, max_length=100, null=True, blank=True)
    product = models.ForeignKey(RawProducts, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name.name} '

class InventoryTask(models.Model):
    task = models.CharField(max_length=100, null=True, blank=True)
    product = models.ForeignKey(RawProducts, on_delete=models.CASCADE, null=True, blank=True)
    msg = models.CharField(max_length=250, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True,default='PENDING')
    date = models.DateTimeField(auto_now_add=True)

def JournalInventoryTask(sender, instance, *args, **kwargs):
    if instance.task is None:
            instance.task = 'INV-{0}'.format(instance.id)
            instance.save()
post_save.connect(JournalInventoryTask, sender=InventoryTask)
class Inventory(models.Model):
    entry =  models.ForeignKey(EmployeeDetail, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(RawProducts, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(RawSuppliers, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(InvCategory, on_delete=models.CASCADE, null=True, blank=True)
    patch = models.CharField(max_length=100, null=True, blank=True)
    q_in = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    q_out = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    unt_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    ext_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    avg_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    action = models.CharField(max_length=10, null=True, blank=True)
    fnsh = models.BooleanField(null=True, blank=True, default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.patch} '


class InventoryPO(models.Model):
    task = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True,default='PENDING')
    date = models.DateTimeField(auto_now_add=True)

def JournalInventoryPO(sender, instance, *args, **kwargs):
    if instance.task is None:
            instance.task = 'PO-{0}'.format(instance.id)
            instance.save()
post_save.connect(JournalInventoryPO, sender=InventoryPO)

class InventoryPOSub(models.Model):
    po = models.ForeignKey(InventoryPO, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(RawProducts, on_delete=models.CASCADE, null=True, blank=True)
    unit = models.CharField(max_length=100, null=True, blank=True)
    qty = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
