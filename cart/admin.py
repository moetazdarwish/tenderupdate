from django.contrib import admin

# Register your models here.
from cart.models import *

admin.site.register(CartName)
admin.site.register(CartInv)
admin.site.register(CartCash)
admin.site.register(Cart)
admin.site.register(CartProducts)
admin.site.register(CartSubProducts)
admin.site.register(POSTask)