from django.db import models

# Create your models here.


class DeliveryProfile(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} '


class DeliveryCost(models.Model):
    area = models.CharField(max_length=15, null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.area} '


class DeliveryArea(models.Model):
    name = models.ForeignKey(DeliveryProfile, on_delete=models.CASCADE, null=True, blank=True)
    area = models.ForeignKey(DeliveryCost, on_delete=models.CASCADE, null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.area.area} '

class OrderDelivery(models.Model):
    patch = models.CharField(max_length=100, null=True, blank=True)
    man = models.ForeignKey(DeliveryProfile, on_delete=models.CASCADE, null=True, blank=True)
    area = models.ForeignKey(DeliveryCost, on_delete=models.CASCADE, null=True, blank=True)
    add = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True, default='CREATED')
    date = models.DateTimeField(auto_now_add=True)



class OrderTracking(models.Model):
    patch = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.patch} '