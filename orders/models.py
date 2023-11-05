from django.db import models
from datetime import datetime
from menu.models import Product

# Create your models here.
# order table
# bill
# customer
# table

class tables(models.Model):
    tid = models.AutoField(primary_key=True)
    status = models.BooleanField()
    last_selected_time = models.DateTimeField(default=datetime.now)  # Add this field


class Customer(models.Model):
    cust_id = models.AutoField(primary_key=True)
    phone_no = models.CharField(unique=True,max_length=15)
    name = models.CharField(max_length=100)
    membership_applied = models.BooleanField(default=False, null=True)

class Bills(models.Model):
    order_id = models.AutoField(primary_key=True)
    table_id = models.IntegerField(default=0)
    # items_json = models.CharField(max_length=5000)
    userId = models.ForeignKey(Customer,on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    status=models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)  # Add this field for the date
    
    def __str__(self):
        return f"Bill {self.order_id} for Table {self.table_id} by {self.userId.name}"



class Orders(models.Model):
    serial=models.AutoField(primary_key=True)
    order_id=models.ForeignKey(Bills,on_delete=models.CASCADE)
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE, default=0)
    Qty=models.IntegerField(default=1)
    status=models.BooleanField(default=False)

    def __str__(self):
        return f"Bill {self.order_id} for product {self.product_id.product_name} in {self.Qty}"