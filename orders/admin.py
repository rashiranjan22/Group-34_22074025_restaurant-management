from django.contrib import admin
# In your app's admin.py file

from .models import Customer,Bills,Orders,tables   # Import all the models you want to register

admin.site.register(Customer)
admin.site.register(Bills)
admin.site.register(Orders)
admin.site.register(tables)
