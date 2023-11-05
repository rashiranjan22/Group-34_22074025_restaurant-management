from django.db import models

# Create your models here.
from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_delete
from django.dispatch import receiver



# Create your models here.
# class Employee(models.Model):
#     emp_id = models.AutoField(primary_key=True,default=1)
#     name = models.CharField(max_length=255, default='A')
#     phone_number = models.CharField(max_length=15, default='1234567890')
#     email = models.EmailField(unique=True, default='example@example.com')
#     position = models.CharField(max_length=50, default='Staff')
#     address = models.TextField(default='none')

#     def _str_(self):
#         return self.name

# class CustomUser(AbstractUser):
#     USER_TYPES = (
#         ('employee', 'Employee'),
#         ('chef', 'Chef'),
#         ('manager', 'Manager'),
#         ('receptionist', 'Receptionist'),
#     )

#     name = models.CharField(max_length=255, default='A')
#     employeeid = models.PositiveIntegerField()
#     user_type = models.CharField(max_length=20, choices=USER_TYPES, default='employee')

#     def _str_(self):
#         return f"{self.name} ({self.get_user_type_display()})"

# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class Employee(models.Model):
    emp_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default='A')
    phone_number = models.CharField(max_length=15, default='1234567890')
    email = models.EmailField(unique=True, default='example@example.com')
    position = models.CharField(max_length=50, default='Staff')
    address = models.TextField(default='none')

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    # USER_TYPES = (
    #     ('employee', 'Employee'),
    #     ('chef', 'Chef'),
    #     ('manager', 'Manager'),
    #     ('receptionist', 'Receptionist'),
    # )

    # user_type = models.CharField(max_length=20, choices=USER_TYPES, default='employee')
    name = models.CharField(max_length=255, default='Amy')
    employee_id = models.PositiveIntegerField(unique=True,default=0)
    # employee_profile = models.OneToOneField(Employee, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Set the username based on the employee_id
        if not self.username:
            self.username = str(self.employee_id)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} "



@receiver(pre_delete, sender=Employee)
def delete_user_on_employee_delete(sender, instance, **kwargs):
    try:
        custom_user = CustomUser.objects.get(employee_id=instance.emp_id)
        custom_user.delete()
    except CustomUser.DoesNotExist:
        # The corresponding user does not exist, no need to delete
        pass
