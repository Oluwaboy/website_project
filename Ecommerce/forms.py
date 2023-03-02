from django import forms

from Ecommerce.models import Order, Customer, Product, Category

# this is django built-in function for users
from django.contrib.auth.models import User


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['ordered_by', 'shipping_address', 'mobile', 'email']



class CustomerRegisterForm(forms.ModelForm):
    # note we created this fields, we will include them in the fields we want to show in the model below
    username = forms.CharField(widget=forms.TextInput())
    # password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Customer
        fields = ['username', 'email', 'password', 'full_name', 'address']


    # this will be for validating the username to avoid inputing the username twice into the database
    def clean_username(self):
        username_clean = self.cleaned_data.get('username') # 'username' is from the username field in the form 
        if User.objects.filter(username=username_clean).exists(): # if the 'username' inputed exist in the User database model
            raise forms.ValidationError('This particular username exist, use another username') # message to display if it exist using the 'ValidationError()'   
        
        return username_clean # without the return, it will give us errror



class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())



class ProductCreateForm(forms.ModelForm):
    more_images = forms.FileField(required=False, widget=forms.FileInput(attrs = {
        'class':'form-control',
        'multiple': True # multiple: True means we can upload many images in this same field  
    }))

    class Meta: 
        model = Product       
        fields = ['title', 'slug', 'category', 'image', 'marked_price', 'selling_price', 'description', 'warranty', 'return_policy']
    
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the product title...',
            }),

            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the product unique slug...',
            }),

            'category': forms.Select(attrs={
                'class': 'form-control',
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),

            'marked_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Marked price of the product...', 
            }),

            'selling_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Selling price of the product...', 
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description of the product...',
                'rows': 5  
            }),

            'warranty': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the product warranty...',  
            }),

            'return_policy': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the product return policy...',  
            }),  
        }   


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'slug']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the category title...'
            }),

            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the category unique slug...'
            }),    
        }  




