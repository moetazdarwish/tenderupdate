from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(EmployeeDetail)
admin.site.register(EmpolyAttendence)
admin.site.register(EmpolySalary)
admin.site.register(EmpolyRequest)
admin.site.register(EmpolyAdvance)