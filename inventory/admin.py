from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(InvCategory)
admin.site.register(RawProducts)
admin.site.register(RawSuppliers)
admin.site.register(SuppliersProdList)
admin.site.register(Inventory)
admin.site.register(InventoryTask)
admin.site.register(InventoryPO)
admin.site.register(InventoryPOSub)