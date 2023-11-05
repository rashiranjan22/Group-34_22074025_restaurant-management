from django.urls import path
from . import views

urlpatterns = [
    path('',views.Ordersview , name='Orders'),
]


urlpatterns += [
    path('place_order/', views.place_order, name='place_order'),
    path('process_existing_customer/', views.process_existing_customer, name='process_existing_customer'),
    path('bills/', views.view_bills, name='view_bills'),
    path('generate_bill/<int:order_id>/', views.generate_bill, name='generate_bill'),
    path('change_status/', views.change_status, name='change_status'),
    path('change_order_status/', views.change_order_status, name='change_order_status'),


]
