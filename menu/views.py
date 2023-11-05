from django.shortcuts import render,get_object_or_404,redirect
from .models import Product
from orders.models import  Bills, tables, Orders
from math import ceil
from django.http import HttpResponseRedirect
from django.urls import reverse
from  users.decorators import manager_required,receptionist_required,chef_required # Import your custom decorator


# Create your views here.

def index(request):
    all_categories = []
    catprods = Product.objects.values('category', 'product_id')
    categories = {item['category'] for item in catprods}
    
    for category in categories:
        products = Product.objects.filter(category=category)
        n = len(products)
        n_slides = n // 4 + ceil((n / 4) - (n // 4))
        all_categories.append({'category': category, 'products': products, 'slides_range': range(1, n_slides), 'nSlides': n_slides})
    
    context = {'all_categories': all_categories}
    return render(request, 'menu/index.html', context)


# def menu_index_1(request):
#     all_categories = []

#     # Retrieve all distinct categories
#     categories = Product.objects.values('category').distinct()

#     for category in categories:
#         category_data = {
#             'category': category['category'],
#             'products': Product.objects.filter(category=category['category']),
#         }
#         all_categories.append(category_data)

#     # Get the latest order
#     latest_order = Orders.objects.order_by('order_id').last()
#     order_id=Bills.objects.order_by('order_id').last().order_id

#     context = {
#         'all_categories': all_categories,
#         'latest_order': latest_order,
#         'order_id':order_id,
#     }

#     return render(request, 'menu/order_menu_index.html', context)
@receptionist_required
def menu_index(request, order_id):
    all_categories = []

    # Retrieve all distinct categories
    categories = Product.objects.values('category').distinct()

    for category in categories:
        category_data = {
            'category': category['category'],
            'products': Product.objects.filter(category=category['category']),
        }
        all_categories.append(category_data)

    # Get the specified order
    # orders = Orders.objects.select_related('product_id')
    # specified_order = orders.objects.filter(order_id=order_id).last()
    specified_order = Orders.objects.select_related('product_id').filter(order_id=order_id)

    context = {
        'all_categories': all_categories,
        'specified_order': specified_order,
        'order_id':order_id,
    }

    return render(request, 'menu/order_menu_index.html', context)

@receptionist_required
def modify_order(request, product_id):
    # Get the latest order
    latest_order = Bills.objects.order_by('order_id').last()

    # Get the product
    product = get_object_or_404(Product, pk=product_id)

    # Check if the product is already in the order
    order_item = Orders.objects.filter(order_id=latest_order, product_id=product).first()

    # Get the action (add or subtract)
    action = request.POST.get('action')

    if action == 'add':
        if order_item:
            # If the item already exists, increase the quantity
            order_item.Qty += 1
            order_item.save()
        else:
            # If the item doesn't exist, create a new order entry
            order_item = Orders(order_id=latest_order, product_id=product, Qty=1, status=False)
            order_item.save()
    elif action == 'subtract':
        if order_item:
            # If the item exists, decrease the quantity
            order_item.Qty -= 1
            order_item.save()
            # If the quantity becomes 0, delete the item
            if order_item.Qty == 0:
                order_item.delete()

    # Redirect to the same page with the latest order_id
    return redirect('order_menu', order_id=latest_order.order_id)





from django.shortcuts import render
from .models import Product, Recipe


def recipe_list(request):
    products_with_recipes = Product.objects.filter(recipe__isnull=False)
    products_without_recipes = Product.objects.filter(recipe__isnull=True)

    return render(request, 'menu/recipe_list.html', {
        'products_with_recipes': products_with_recipes,
        'products_without_recipes': products_without_recipes,
    })



from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Recipe
from .forms import RecipeForm  # Create this form in forms.py
from django.contrib.auth.decorators import login_required


# @login_required
@chef_required
def edit_recipe(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    recipe, created = Recipe.objects.get_or_create(product_id=product)

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_list')  # Redirect to the recipe list page
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'menu/edit_recipe.html', {
        'product': product,
        'form': form,
    })

# @login_required
@chef_required
def add_recipe(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)

    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.product_id = product
            recipe.save()
            return redirect('recipe_list')  # Redirect to the recipe list page
    else:
        form = RecipeForm()

    return render(request, 'menu/add_recipe.html', {
        'product': product,
        'form': form,
    })


def open_recipe(request,product_id):
    product = get_object_or_404(Product, product_id=product_id)

    return render(request, 'menu/open_recipe.html', {
        'product': product,
    })








