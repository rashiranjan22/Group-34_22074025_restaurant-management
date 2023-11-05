from django.db import models
from django.utils import timezone


# Create your models here.

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    # subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=200)
    # pub_date = models.DateField()
    image = models.ImageField(upload_to="product_images", default="")

    def _str_(self):
        return self.product_name
    

class Recipe(models.Model):
    product_id = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    recipe = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.product_id.product_name  # Access the related Product's product_name field

    


