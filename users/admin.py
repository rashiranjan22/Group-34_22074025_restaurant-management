from django.contrib import admin
from .models import Employee,CustomUser

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('emp_id', 'name', 'position', 'email','address')  # columns to show in the list
    search_fields = ('name', 'position')                    # add search bar
    list_filter = ('position',)                             # add filters on right side
    ordering = ('emp_id',)       

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'employee_id', 'password')  # columns to show in the list
    search_fields = ('name', 'employee_id')                    # add search bar
    ordering = ('employee_id',)       

    
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
