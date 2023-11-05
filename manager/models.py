from django.db import models

# Create your models here.
class LeaveRequest(models.Model):
    emp_id = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, default='Pending')  # Status can be 'Pending', 'Approved', or 'Rejected'