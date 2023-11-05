from django.contrib import admin

# Register your models here.
from .models import LeaveRequest  # Import all the models you want to register

admin.site.register(LeaveRequest)