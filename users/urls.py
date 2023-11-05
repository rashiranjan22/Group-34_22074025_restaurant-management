from django.contrib import admin
from django.urls import path
from . import views as users_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', users_views.register_view, name='register'),
    path('login/', users_views.login_view, name='login'),
    path('chef_dashboard/', users_views.chef_dashboard, name='chef_dashboard'),
    path('receptionist_dashboard/', users_views.receptionist_dashboard, name='receptionist_dashboard'),
    path('employee/<int:emp_id>/', users_views.employee_profile, name='employee_profile'),
    path('memployee/<int:emp_id>/', users_views.manager_employee_profile, name='manager_employee_profile'),
    # path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', users_views.logout_view, name='logout'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)