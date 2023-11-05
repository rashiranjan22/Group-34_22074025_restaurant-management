from django import forms
from .models import Customer

# class CustomerInfoForm(forms.ModelForm):
#     class Meta:
#         model = Customer
#         fields = ['phone_no', 'name', 'membership_applied']



class CustomerInfoForm(forms.ModelForm):
    update_existing = forms.BooleanField(initial=False, required=False)

    class Meta:
        model = Customer
        fields = ['phone_no', 'name', 'membership_applied']


from django import forms

class OrderStatusForm(forms.Form):
    status = forms.BooleanField(required=False)
    order_id = forms.IntegerField(widget=forms.HiddenInput())  # Include a hidden input for the order ID