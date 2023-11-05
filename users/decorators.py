from django.http import HttpResponseForbidden
from .models import CustomUser,Employee
def manager_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            e=Employee.objects.filter(emp_id=request.user.employee_id).first()
            print(e)
            user_type = e.position
            if user_type =='manager':
                return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You don't have permission to access this page.")
    return _wrapped_view

def receptionist_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            e=Employee.objects.filter(emp_id=request.user.employee_id).first()
            print(e)
            user_type = e.position
            if user_type =='receptionist':
                return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You don't have permission to access this page.")
    return _wrapped_view
    
def manager_receptionist_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            e=Employee.objects.filter(emp_id=request.user.employee_id).first()
            print(e)
            user_type = e.position
            if user_type in ('receptionist','manager'):
                return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You don't have permission to access this page.")
    return _wrapped_view

def chef_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            e=Employee.objects.filter(emp_id=request.user.employee_id).first()
            print(e)
            user_type = e.position
            if user_type =='chef':
                return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You don't have permission to access this page.")
    return _wrapped_view

def employee_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            e=Employee.objects.filter(emp_id=request.user.employee_id).first()
            print(e)
            user_type = e.position
            if user_type =='employee':
                return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You don't have permission to access this page.")
    return _wrapped_view