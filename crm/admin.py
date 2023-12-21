from django.contrib import admin

from crm.models import *

# Register your models here.

admin.site.register(CustomerDirectory)
admin.site.register(CustomerProfile)
admin.site.register(CustomerDiscount)