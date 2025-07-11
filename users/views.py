from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from orders.models import Orders
from manager.models import LeaveRequest
from  users.decorators import manager_required,receptionist_required,chef_required,employee_required,manager_receptionist_required # Import your custom decorator

from django.shortcuts import render,get_object_or_404
from .forms import CustomUserForm
from .models import Employee
from django import forms

def register_view(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            custom_user = form.save(commit=False)

            # Get employee details based on emp_id
            employee = Employee.objects.get(emp_id=form.cleaned_data['emp_id'])
            if form.cleaned_data['name'] != employee.name:
                form.add_error('name', "Name of the employee doesn't match.")
                return render(request, 'users/register.html', {'form': form})

            # custom_user.name = employee.name // redundant
            custom_user.employee_id = employee.emp_id
            custom_user.employee = employee
            custom_user.save()

            success_message = "Registered successfully"
            return render(request, 'users/register.html', {'form': form, 'success_message': success_message})

    else:
        form = CustomUserForm()

    return render(request, 'users/register.html', {'form': form})


# views.py
def login_view(request):
    message = ""

    if request.method == 'POST':
        user_type = request.POST['user_type']
        username = request.POST['username']
        password = request.POST['password']

        if user_type == 'employee':
            user = authenticate(request, username=username, password=password)
        else:
            # Check if the employee with the given username has the matching position
            try:
                employee = Employee.objects.get(emp_id=username)
                if employee.position == user_type:
                    user = authenticate(request, username=username, password=password)
                else:
                    user = None
                    message = f"The selected user type '{user_type}' does not match the employee's position."
            except Employee.DoesNotExist:
                user = None
                message = 'No such user exists.'

        if user is not None:
            login(request, user)
            if user_type == 'chef':
                return redirect('chef_dashboard')
            elif user_type == 'manager':
                return redirect('manager_dashboard')
            elif user_type == 'receptionist':
                return redirect('receptionist_dashboard')
            elif user_type == 'employee':
                return redirect('employee_profile', emp_id=user.employee_id)
        else:
            if not CustomUser.objects.filter(username=username).exists():
                # No such user with employee code exists
                message= 'No such user exists.'
            else:
                # Password doesn't match
                message= 'Incorrect password.'
    return render(request, 'users/login.html', {'message': message})




@chef_required
def chef_dashboard(request):
    orders = Orders.objects.all()  # You can add filters or ordering as needed
    return render(request, 'users/chef_dashboard.html', {'orders':orders})


@receptionist_required
def receptionist_dashboard(request):
    orders = Orders.objects.all()  # You can add filters or ordering as needed
    return render(request, 'users/receptionist_dashboard.html',{'orders':orders})  # Create templates for receptionist_dashboard


def employee_profile(request, emp_id):
    employee = get_object_or_404(Employee, emp_id=emp_id)
    leave_requests = LeaveRequest.objects.filter(emp_id=emp_id, status__in=['Approved', 'Rejected','Pending'])

    return render(request, 'users/employee_profile.html', {'employee': employee, 'leave_requests': leave_requests})

@manager_required
def manager_employee_profile(request, emp_id):
    employee = get_object_or_404(Employee, emp_id=emp_id)
    leave_requests = LeaveRequest.objects.filter(emp_id=emp_id, status__in=['Approved', 'Rejected','Pending'])

    return render(request, 'users/manager_employee_profile.html', {'employee': employee, 'leave_requests': leave_requests})



from django.contrib.auth import logout
@login_required
def logout_view(request):
    logout(request)
    return render(request,'users/logout.html')

