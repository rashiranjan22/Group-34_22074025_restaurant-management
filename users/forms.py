from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from .models import Employee

# class CustomUserForm(forms.ModelForm):
#     password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
#     password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

#     class Meta:
#         model = CustomUser
#         fields = ['name', 'employeeid', 'password1', 'password2']

#     def clean_employee_id(self):
#         employee_id = self.cleaned_data.get('employeeid')

#         # Check if the employee with the given emp_id exists
#         if not Employee.objects.filter(emp_id=employee_id).exists():
#             raise forms.ValidationError('No Employee Found')

#         # Check if the user with the given emp_id already exists
#         if CustomUser.objects.filter(employee_id=employee_id).exists():
#             raise forms.ValidationError('Already Registered')

#         # Obtain the employee's position and set it as the user_type
#         employee = Employee.objects.get(emp_id=employee_id)
#         user_type = employee.position

#         # Check if the user_type is chef, manager, or receptionist
#         if user_type not in ['chef', 'manager', 'receptionist']:
#             raise forms.ValidationError('Access Denied')

#         return employee_id

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.user_type = self.cleaned_data.get('user_type')
#         if commit:
#             user.save()
#         return user

# users/forms.py
from django import forms
from .models import CustomUser,Employee
from django.contrib.auth.forms import UserCreationForm

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
