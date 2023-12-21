from django.contrib import admin

from delivery.models import *

# Register your models here.
admin.site.register(DeliveryProfile)
admin.site.register(DeliveryCost)
admin.site.register(DeliveryArea)
admin.site.register(OrderDelivery)
admin.site.register(OrderTracking)