
from django.contrib import admin
from django.urls import path
from . import views as manager_views
from .views import bar_chart_image, pie_chart_image
from django.conf import settings
from django.conf.urls.static import static
from .views import customer_list, billing_history,employee_list,apply_leave,view_leave_requests

urlpatterns = [
    path('manager_dashboard/', manager_views.manager_dashboard, name='manager_dashboard'),
    path('bar_chart_image/', bar_chart_image, name='bar_chart_image'),
    path('pie_chart_image/', pie_chart_image, name='pie_chart_image'),
    path('customers/', customer_list, name='customer_list'),
    path('billing_history/<int:customer_id>/', billing_history, name='billing_history'),
    path('employee-list/', employee_list, name='employee_list'),
    path('apply_leave/<int:emp_id>/', apply_leave, name='apply_leave'),
    path('view_leave_requests/<int:emp_id>/', view_leave_requests, name='view_leave_requests'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

