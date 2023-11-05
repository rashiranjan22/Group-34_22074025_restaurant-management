from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
# views.py
from django.shortcuts import render
from django.db.models import Count, Sum
from users.models import Employee
from orders.models import Bills,Orders,Customer
from menu.models import Product
import matplotlib.pyplot as plt
from django.http import HttpResponse
import os
import calendar
from io import BytesIO

def get_month_name(month_number):
    return calendar.month_abbr[month_number]

def bar_chart_image(request):
    # Serve the bar chart image
    path = os.path.join('media', 'bar_chart.png')
    with open(path, 'rb') as f:
        return HttpResponse(f.read(), content_type='image/png')

def pie_chart_image(request):
    # Serve the pie chart image
    path = os.path.join('media', 'pie_chart.png')
    with open(path, 'rb') as f:
        return HttpResponse(f.read(), content_type='image/png')

@login_required
def manager_dashboard(request):
    # Sales month-wise
    sales_data = Bills.objects.filter(status=True).values('date__month').annotate(monthly_sales=Sum('amount'))

    # Orders category-wise
    orders_data = Orders.objects.values('product_id__category').annotate(order_count=Count('product_id'))

    # Number of employees, customers, orders
    num_employees = Employee.objects.count()
    num_customers = Customer.objects.count()
    num_orders = Orders.objects.count()

    # Total sales
    total_sales = Bills.objects.filter(status=True).aggregate(total_sales=Sum('amount'))['total_sales'] or 0

    # Data for charts
    all_months = range(1, 13)
    months = [entry['date__month'] for entry in sales_data]
    sales_values = [entry['monthly_sales'] for entry in sales_data]
    categories = [entry['product_id__category'] for entry in orders_data]
    order_counts = [entry['order_count'] for entry in orders_data]

    # Fill in missing months with zero sales
    for month in all_months:
        if month not in months:
            months.append(month)
            sales_values.append(0)

    # Sort data by month
    data = sorted(zip(months, sales_values), key=lambda x: x[0])
    months, sales_values = zip(*data)

    # Bar Chart (Total Sales Month-wise)
    plt.figure(figsize=(8, 5))
    plt.bar(months, sales_values, color='skyblue')
    plt.xlabel('Month')
    plt.ylabel('Total Sales')
    plt.title('Total Sales Month-wise')
    plt.xticks(months, [get_month_name(month) for month in months])

    # Save the figure to a BytesIO object
    bar_chart_image = BytesIO()
    plt.savefig(bar_chart_image, format='png')
    plt.close()

    # Pie Chart (Orders Category-wise)
    plt.figure(figsize=(8, 5))
    plt.pie(order_counts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Orders Category-wise')

    # Save the figure to a BytesIO object
    pie_chart_image = BytesIO()
    plt.savefig(pie_chart_image, format='png')
    plt.close()

    # Save the chart images to the media directory
    media_dir = 'media'
    bar_chart_path = os.path.join(media_dir, 'bar_chart.png')
    pie_chart_path = os.path.join(media_dir, 'pie_chart.png')

    plt.figure(figsize=(8, 5))
    plt.bar(months, sales_values, color='skyblue')
    plt.xlabel('Month')
    plt.ylabel('Total Sales')
    plt.title('Total Sales Month-wise')
    plt.xticks(months, [get_month_name(month) for month in months])
    plt.savefig(bar_chart_path)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.pie(order_counts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Orders Category-wise')
    plt.savefig(pie_chart_path)
    plt.close()

    most_ordered_product = Orders.objects.values('product_id__product_name').annotate(order_count=Count('product_id')).order_by('-order_count').first()
    mop=Product.objects.filter(product_name=most_ordered_product['product_id__product_name']).first()

    # Render the dashboard template with chart data
    return render(request, 'manager/manager_dashboard.html', {
        'num_employees': num_employees,
        'num_customers': num_customers,
        'num_orders': num_orders,
        'total_sales': total_sales,
        'bar_chart_image_data': bar_chart_path,
        'pie_chart_image_data': pie_chart_path,
        'most_ordered_product': most_ordered_product,
        'mop':mop,
    })

# manager_views.py
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from orders.models import Customer, Bills

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'manager/customer_list.html', {'customers': customers})

def billing_history(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    bills = Bills.objects.filter(userId=customer)
    return render(request, 'manager/billing_history.html', {'customer': customer, 'bills': bills})


from users.models import Employee

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'manager/employee_list.html', {'employees': employees})

from django.shortcuts import render, redirect, get_object_or_404
from .models import LeaveRequest
from users.models import Employee
from django.contrib import messages

def apply_leave(request, emp_id):
    employee = get_object_or_404(Employee, emp_id=emp_id)

    if request.method == 'POST':
        emp_id = request.POST.get('emp_id')
        start_date = request.POST.get('start_date')

        if not start_date:
            return render(request, 'manager/apply_leave.html', {'employee': employee, 'error_message': 'Start date is required'})

        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')

        LeaveRequest.objects.create(emp_id=emp_id, start_date=start_date, end_date=end_date, reason=reason)

        # Add a success message
        messages.success(request, 'Leave applied successfully')

        return redirect('apply_leave', emp_id=emp_id)

    return render(request, 'manager/apply_leave.html', {'employee': employee})


# views.py

def view_leave_requests(request, emp_id):
    employee = get_object_or_404(Employee, emp_id=emp_id)
    leave_requests = LeaveRequest.objects.filter(emp_id=emp_id)
    
    if request.method == 'POST':
        # Handle approval or rejection
        leave_request_id = request.POST.get('leave_request_id')
        action = request.POST.get('action')

        if action == 'approve':
            LeaveRequest.objects.filter(id=leave_request_id).update(status='Approved')
        elif action == 'reject':
            LeaveRequest.objects.filter(id=leave_request_id).update(status='Rejected')

        return redirect('view_leave_requests', emp_id=emp_id)

    return render(request, 'manager/view_leave_requests.html', {'employee': employee, 'leave_requests': leave_requests})
