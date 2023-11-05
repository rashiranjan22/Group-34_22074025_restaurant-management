from django.urls import path
from . import views

urlpatterns = [
    path('index',views.index , name='menulist'),
    path('ordermenu/<int:order_id>/', views.menu_index, name='order_menu'),
    path('modify_order/<int:product_id>/', views.modify_order, name='modify_order'),
    path('recipe_list/', views.recipe_list, name='recipe_list'),
    path('edit_recipe/<int:product_id>/', views.edit_recipe, name='edit_recipe'),
    path('add_recipe/<int:product_id>/', views.add_recipe, name='add_recipe'),
    path('open_recipe/<int:product_id>/', views.open_recipe, name='open_recipe'),

]

