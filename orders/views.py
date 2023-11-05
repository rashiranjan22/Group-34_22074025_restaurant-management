from django.shortcuts import render, get_object_or_404
from .models import Orders,Bills, Customer,tables
from menu.models import Product
from users.models import Employee
from django.http import JsonResponse
from  users.decorators import manager_required,receptionist_required,chef_required,manager_receptionist_required # Import your custom decorator


  
@manager_receptionist_required  
def Ordersview(request):
    # Fetch data from the database using a queryset that joins the two tables
    orders = Orders.objects.select_related('product_id')

    message=""

    tables_list = tables.objects.all()

    if request.method == 'POST' and 'place_order' in request.POST:
        if all(table.status for table in tables_list):
            message="Alas! there are no tables available right now."
        if message=="":
            return redirect('place_order')


    context = {
        'orders': orders, 'message':message
    }

    return render(request, 'orders/orderview.html', context)

from django.shortcuts import render, redirect
from .models import Customer, Bills, tables
from django.http import HttpResponse

@receptionist_required  
def place_order(request):
    vacant_tables = get_vacant_tables()

    if request.method == 'POST':
        phone_no = request.POST.get('phone_no')
        name = request.POST.get('name')
        membership_applied = request.POST.get('membership_applied')
        selected_table_id = request.POST.get('selected_table_id')

        if membership_applied == 'True':
            membership_applied = True
        else:
            membership_applied = False

        # Check if the phone number already exists
        customer_exists = Customer.objects.filter(phone_no=phone_no).exists()

        if customer_exists:
            existing_customer = Customer.objects.get(phone_no=phone_no)
            return render(request, 'orders/place_order_existing_customer.html', {'existing_customer': existing_customer,'selected_table_id':selected_table_id})
        else:
            # Create a new customer
            new_customer = Customer.objects.create(phone_no=phone_no, name=name, membership_applied=membership_applied)
            cust_id = new_customer.cust_id

            # Check if a table is selected
            if selected_table_id:
                selected_table = tables.objects.filter(tid=selected_table_id).first()
                if selected_table and not selected_table.status:
                    selected_table.status = True
                    selected_table.save()
                    Bills.objects.create(userId_id=cust_id, table_id=selected_table_id)
                    # return HttpResponse("Order placed successfully!")

                    all_categories = []

                    # Retrieve all distinct categories
                    categories = Product.objects.values('category').distinct()

                    for category in categories:
                        category_data = {
                            'category': category['category'],
                            'products': Product.objects.filter(category=category['category']),
                        }
                        all_categories.append(category_data)

                    # Get the latest order
                    latest_order = Orders.objects.order_by('order_id').last()
                    order_id=Bills.objects.order_by('order_id').last().order_id

                    context = {
                        'all_categories': all_categories,
                        'latest_order': latest_order,
                        'order_id':order_id,
                    }

                    return render(request,'menu/order_menu_index.html',context)
                else:
                    return render(request, 'orders/place_order.html', {'vacant_tables': vacant_tables, 'selected_table_id': selected_table_id, 'message': 'Selected table is not vacant.'})
            else:
                return render(request, 'orders/place_order.html', {'vacant_tables': vacant_tables, 'selected_table_id': selected_table_id, 'message': 'Please select a table.'})

    else:
        return render(request, 'orders/place_order.html', {'vacant_tables': vacant_tables, 'selected_table_id': None, 'message': ''})

def process_existing_customer(request):
    if request.method == 'POST':
        cust_id = request.POST.get('cust_id')
        selected_table_id = request.POST.get('selected_table_id')

        # Check if a table is selected
        if selected_table_id:
            selected_table = tables.objects.filter(tid=selected_table_id).first()
            if selected_table and not selected_table.status:
                selected_table.status = True
                selected_table.save()
                Bills.objects.create(userId_id=cust_id, table_id=selected_table_id)

                all_categories = []
                # Retrieve all distinct categories
                categories = Product.objects.values('category').distinct()
                for category in categories:
                    category_data = {
                        'category': category['category'],
                        'products': Product.objects.filter(category=category['category']),
                    }
                    all_categories.append(category_data)
                # Get the latest order
                latest_order = Orders.objects.order_by('order_id').last()
                order_id=Bills.objects.order_by('order_id').last().order_id
                context = {
                    'all_categories': all_categories,
                    'latest_order': latest_order,
                    'order_id':order_id,
                }

                return render(request,'menu/order_menu_index.html',context)
            else:
                return render(request, 'orders/place_order_existing_customer.html', {'existing_customer': Customer.objects.get(cust_id=cust_id), 'message': 'Selected table is not vacant.'})
        else:
            return render(request, 'orders/place_order_existing_customer.html', {'existing_customer': Customer.objects.get(cust_id=cust_id), 'message': 'Please select a table.'})
    else:
        return render(request, 'orders/place_order_existing_customer.html', {'message': 'Invalid request.'})


def get_vacant_tables():
    return tables.objects.filter(status=False)


@manager_receptionist_required  
def view_bills(request):
    bills = Bills.objects.all()
    context = {'bills': bills}
    return render(request, 'orders/bills_list.html', context)


@manager_receptionist_required  
def generate_bill(request, order_id):
    bill = Bills.objects.get(order_id=order_id)
    products = Orders.objects.filter(order_id=bill)
    
    # Calculate subtotal for each product
    for product in products:
        product.subtotal = product.product_id.price * product.Qty

    total_price = sum(product.subtotal for product in products)
        
    total_price = sum(product.subtotal for product in products)
    discounted=0
    if bill.userId.membership_applied:
        discounted=total_price*(0.8)

    bill.amount=total_price-discounted
    bill.save()

    e=Employee.objects.filter(emp_id=request.user.employee_id).first()
    user_type = e.position

    context = {'bill': bill, 'products': products, 'total_price': total_price,'discounted':discounted,'user_type':user_type}
    return render(request, 'orders/bill_details.html', context)




from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from .models import Orders

@require_POST
def change_status(request):
    order_serial = request.POST.get('order_id')
    try:
        order = Orders.objects.get(serial=order_serial)
        order.status = not order.status  # Toggle the status
        order.save()
    except Orders.DoesNotExist:
        # Handle the case where the order doesn't exist
        pass
    
    return redirect('chef_dashboard')  # Replace 'your_view_name' with the actual name of the view rendering the page with the order list


from django.shortcuts import render, redirect
from .models import Bills, tables

def change_order_status(request):
    if request.method == "POST":
        bill_id = request.POST.get("bill_id")
        original_status = request.POST.get("original_status")
        bill = Bills.objects.get(order_id=bill_id)

        print(bill_id)
        print(bill.order_id)

        # Toggle the bill status
        bill.status = True
        bill.save()

        print(bill.status)

        # Update the corresponding table status
        table = tables.objects.get(tid=bill.table_id)
        table.status = False
        table.save()

    # Redirect back to the page where you display bills
    return redirect('view_bills')  # Replace 'your_bills_page' with your actual URL name
