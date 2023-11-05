from django.contrib import admin
from .models import Employee,CustomUser

# Register your models here.
# admin.site.register(Employee)
admin.site.register(CustomUser)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('emp_id', 'name', 'phone_number', 'email', 'position', 'address')

admin.site.register(Employee, EmployeeAdmin)
