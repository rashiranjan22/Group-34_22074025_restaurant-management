from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from .models import Employee

class CustomUserForm(UserCreationForm):
    emp_id = forms.IntegerField(label='Employee ID')

    class Meta:
        model = CustomUser
        fields = ['name', 'emp_id', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        emp_id = cleaned_data.get('emp_id')
        name = cleaned_data.get('name')

        # Check if employee with the given emp_id exists
        if not Employee.objects.filter(emp_id=emp_id).exists():
            raise forms.ValidationError("No employee found with this Employee ID.")

        # Check if the emp_id is already registered
        if CustomUser.objects.filter(employee_id=emp_id).exists():
            raise forms.ValidationError("This Employee ID is already registered. Login instead.")

        # Check if the entered name matches the name in the Employee table
        employee = Employee.objects.get(emp_id=emp_id)
        if name != employee.name:
            raise forms.ValidationError("Name of the employee doesn't match with the existing details.")

        return cleaned_data
