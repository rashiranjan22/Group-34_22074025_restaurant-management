from django.contrib import admin

# Register your models here.

from .models import Product,Recipe   # Import all the models you want to register

admin.site.register(Product)
admin.site.register(Recipe)
