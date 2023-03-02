from django.shortcuts import render, redirect

# this is django class based built-in function 
# TemplateView should be used when you want to present some information on an HTML page, not when the page has forms, creation or update of objects 
# the 'CreateView' allows to create class-based view that displays a form for creating an object, redisplaying the form with validation errors and saving the object into the database
# DetailView should be used when you want to present detail of a single model instance also to display instances of a table in the database, it should not be used when the page has forms and does creation or update of objects
from django.views.generic import TemplateView, View, CreateView, FormView, DetailView, ListView

from Ecommerce.models import Product, Category, Cart, CartProduct, Customer, Order, Admin, ProductImage

from django.urls import reverse_lazy

from Ecommerce.forms import CheckoutForm, CustomerRegisterForm, CustomerLoginForm, ProductCreateForm, CategoryCreateForm

# this is django built-in function for users
from django.contrib.auth.models import User

from django.contrib.auth import login, authenticate, logout

# to search from diferent fields in the database model we will import Q
from django.db.models import Q

# this is django built-in method to enable us paginate our front end website
from django.core.paginator import Paginator

# Create your views here.

# in this class, we want to assign user/customer from the database Customer and User to the cart to know the user/customer that made the order
class EcomMixin(object): # we will add 'EcomMixin' in the class below, which will assign customer/user from the User and Customer database model to know the customer/user that made has the cart and product
    def dispatch(self, request, *args, **kwargs):
        user_cart_id = request.session.get('cart_id')
        if user_cart_id:
            cart_object = Cart.objects.get(id=user_cart_id)
            if request.user.is_authenticated and Customer.objects.filter(user = request.user).exists():
                cart_object.customer = request.user.customer
                cart_object.save()

        return super().dispatch(request, *args, **kwargs)        



class HomeView(EcomMixin, TemplateView):
    #'template_name' must be included in the TemplateView which shows the name of the particular template, which will display whatever in the template
    template_name = 'home.html'

    # to display data/info from the database or the backend we will be using def get_context_data() 
    def get_context_data(self, **kwargs):  # the 'get_context_data()' is used in passing context data variable into the templates from class-based views
        context = super().get_context_data(**kwargs) # 'super()' can be used to easily inherit attributes and methods from a parent template view and customize or extent them as needed. The 'super().get_context_data(**kwargs)' is used to pass data to the template for rendering 
        context['pagename'] = 'This is an ecommerce page' # this is the data we will be displaying in the front end       
        
        # data/details from the database
        # we want to use Paginator from django to paginate the HomeView
        product_paginate = Product.objects.all().order_by('-id')

        # we are using home_paginate variable to create a paginator object with the the django Paginator class   
        home_paginate = Paginator(product_paginate, 4) # am telling the Paginator which was imported from django to paginate the product_paginate in 4, meaning each page will display only 4 products par page

        # page_number variable was created which requests the current page number using the '?page' passed in the template 
        page_number = self.request.GET.get('page') # note that 'page' from the '?page' which is a GET method
        # print(page_number)
        
        # then we combine all of the data using the 'product_list_page' variable
        product_list_page = home_paginate.get_page(page_number)

        # 'product_list' is what we will be showing/displaying in the template
        context['product_list'] = product_list_page   
        # '.order_by()' gives the ordering/arrangement of the products accordingly in the Product model, (-id) means ordering according to the recent products accorded to the Product model id   
        
        return context # without the 'return context' the context won't be displayed in the front page   


class All_ProductView(EcomMixin, TemplateView):
    template_name = 'all_categories.html'
    
    def get_context_data(self, **kwargs):  # the 'get_context_data()' is used in passing context data variable into the templates from class-based views
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        return context

# in the all_categories.html template we are displaying all the categories and their products
# {% for cat in categories %} used in the template means we are fetching all the categories from the Category model database which also has products relating to the Category
# note that the Product model links to the Catagory model using ForeignKey in the category field, therefore to obtain the products relating to the Category database we had to connect it using cat.product_set.all - > product is the Product model database we need to write it in small letter, capitalizing it will give us all error
# '_set.all' will display all the products/informations relating to the individual category


class Product_detailView(EcomMixin, TemplateView):
    template_name = 'product_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_product_slug = self.kwargs['product_slug'] # 'product_slug' is from the urls.py, we used self.kwargs[''] to obtain the slug which is passed in the urls.py then assigned it a variable known as url_product_slug
        # print('slug', 76843)
   
        product_slug_get = Product.objects.get(slug=url_product_slug) # slug is the field in the Product model
        product_slug_get.view_count += 1 # this means anytime the detail page is loaded or viewed by the customer, the view_count increases to 1 
        # note that 'product_slug_get' fetching the data from the Product model databse and the Product model has view_count field that is why we wrote product_slug_get.view_count 
        product_slug_get.save() # this will save all the changes/ the code we inputed
        
        context['get_product_slug'] = product_slug_get 

        return context



class Add_to_cart(EcomMixin, TemplateView):
    template_name = 'add_to_cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 1. get the product id from the requested url in the urls.py file
        url_product_id = self.kwargs['cart_product_id']  # 'cart_product_id' is from the urls.py having <int:cart_product_id>
        # print(url_product_id) 
        
        # 2. get the product from the Product model using the .get() method
        product_item = Product.objects.get(id=url_product_id)
        # print(product_item)

        cart_product_id = self.request.session.get('cart_id', None) # 'cart_id' now becomes the session that will be stored in the server/system otherwise 'None'
        # print( cart_product_id) # this will display 'None' since their is no session yet

        if cart_product_id:  # 'cart_product_id' is the variable storing the session as seen above, this means we have session
            # print('Their is session')
            cart_item = Cart.objects.get(id=cart_product_id) # we want to get from the Cart model if cart_product_id exist 
       
            product_in_cart = cart_item.cartproduct_set.filter(product=product_item)
            # item/product already exist in cart
            if product_in_cart.exists():
                cartproduct = product_in_cart.last() # the '.last()' returns the last item of an object, cartproduct is a CartProduct database model
                cartproduct.quantity += 1
                cartproduct.subtotal += product_item.selling_price # product_item is defined as above, which is from the Product model database
                cartproduct.save()

                cart_item.total += product_item.selling_price   
                cart_item.save()
            
            # item/product does not exist in cart, we want to add them
            else: 
                cartproduct = CartProduct.objects.create(cart=cart_item, product=product_item, rate=product_item.selling_price, quantity=1, subtotal=product_item.selling_price)
                
                cart_item.total += product_item.selling_price   
                cart_item.save()

        else: # we dont have session
            # print('No session')
            cart_item = Cart.objects.create(total=0) # we must supply total=0 since it is the default value in the Cart model  
            self.request.session['cart_id'] = cart_item.id # we are noe creating a session and assigning it the value cart_item.id from the Cart database model
            
            cartproduct = CartProduct.objects.create(cart=cart_item, product=product_item, rate=product_item.selling_price, quantity=1, subtotal=product_item.selling_price)               
            cart_item.total += product_item.selling_price   
            cart_item.save()
 
        return context 



class MyCartView(EcomMixin, TemplateView):
    template_name = 'my_cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart_session_id = self.request.session.get('cart_id', None) # note that 'cart_id' is used to store and get the session as seen in 'class Add_to_cart(TemplateView)' above        
        if cart_session_id:
            # print('Session exist')
            cart_session = Cart.objects.get(id=cart_session_id)
        else:
            # print('Session does not exist')
            cart_session = None 

        context['cart_product'] = cart_session 
        # print(cart_session)      

        return context 

# the '{{ forloop.counter }}' used in the my_cart.html helps to arrange the loops serially from 1 to rather than the id in the database model 



class ManageCartView(EcomMixin, View): # we can also either use 'TemplateView' inside the ()
    def get(self, request, *args, **kwargs):  # note that we are using 'get(self, request, *args, **kwargs)' since it is a get method as seen in the my_cart.html, we are getting the 'increase, decrease and remove' when the button is clicked,  we are not obtaining anything from the database  
        # print('This is manage cart section')

        cart_select_id = self.kwargs['cart_functions'] 
        # print(cart_select_id) 
        cart_action_get = request.GET.get('cart_action') # note that 'cart_action' is from the my_cart.html buttons which is a get method, therefore we are using .get() to fetch/get the data     
        # print(cart_action_get)
        
        cartproduct_obj = CartProduct.objects.get(id=cart_select_id)
        # print(cartproduct_obj)
        cart_obj = cartproduct_obj.cart 
        # print(cart_obj)

        if cart_action_get == 'increase':  # this means if the +/increase button is clicked  
            # print('Cart quantity increased')
            cartproduct_obj.quantity += 1  # the product quantity from the CartProduct database model will increase automatically by 1  
            # print(cartproduct_obj.quantity)                       
            cartproduct_obj.subtotal += cartproduct_obj.rate
            # print(cartproduct_obj.subtotal)
            cartproduct_obj.save() #  this will save the changes

            cart_obj.total += cartproduct_obj.rate
            # print(cart_obj.total)
            cart_obj.save()

        elif cart_action_get == 'decrease':  # this means if the -/decrease button is clicked
            # print('Cart quantity decreased')
            cartproduct_obj.quantity -= 1  
            cartproduct_obj.subtotal -= cartproduct_obj.rate
            cartproduct_obj.save()

            cart_obj.total -= cartproduct_obj.rate
            cart_obj.save()

            if cartproduct_obj.quantity == 0: # this means if the quantity in our cart is 0
                # print('Qunatity is 0') 
                cartproduct_obj.delete() # this will delete the product from the cart 

        elif cart_action_get == 'remove':  # this means if the x/remove button is clicked
            # print('Cart quantity removed')
            cart_obj.total -= cartproduct_obj.rate
            # print(cart_obj.total)
            cart_obj.save() # save the changes 
            cartproduct_obj.delete() # then delete the product from the cart

        else:
            pass

        return redirect('Ecommerce:my_cart') 
        
       

class EmptyCartView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        cart_session_get = request.session.get('cart_id', None)
        # print(cart_session_get)
        
        if cart_session_get:
            # print('We have cart')
            cart_session_exist = Cart.objects.get(id=cart_session_get) # we want to obtain the session
            cart_session_exist.cartproduct_set.all().delete() # we want to delete the session
            cart_session_exist.total = 0 # note that the default value from out Cart database model is = 0, therefore we are setting it to '0' after deleting 
            cart_session_exist.save() # save the changes

        return redirect('Ecommerce:my_cart') 



class CheckoutView(EcomMixin, CreateView):
    template_name = 'checkout.html' # this is the html that will be displaying to the front end
    form_class = CheckoutForm # this is the form we will be using for creating and inputing data into the database, which will be displaying using 'form_class'
    success_url = reverse_lazy('Ecommerce:homepage')
    # 'success_url' is the target url that django will redirect to once a task is created successfully, we redirect to the 'homepage' using the reverse_lazy() function, the reverse_lazy() accepts a view name and returns an URL 

    # the dispatch method takes in the request and ultimately returns the response, it simply decides what method in the class(e.g get(), post() etc) should be used(i.e dispatched) based on the HTTP method used in the request
    def dispatch(self, request, *args, **kwargs): 
        # print('This is dispatch method')

        # we want the dispatch() method to ensure that user is login and in the user Customer database model before anything can be done on the checkout
        if request.user.is_authenticated and Customer.objects.filter(user = request.user).exists(): # this means the user is authenticated and is also present in the Customer database model, '.customer' is the Customer database model
            # print('User is login')
            pass
        else: # the use is not authenticated
            #print('User is not log in')
            return redirect('/login/?next=/checkout/')  # note that '?next' was passed in the customer_login.html

        return super().dispatch(request, *args, **kwargs) # you need to return this for it to function properly and to avoid error


    # to display the products from the database into our front page
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart_session_get = self.request.session.get('cart_id', None) # writing only 'request.session.get('cart_id', None)' will give an error reason for putting 'self'
        # print(cart_session_get)
        if cart_session_get:
            cart_object = Cart.objects.get(id=cart_session_get)
        else:
            cart_object = None

        context['cart_front'] = cart_object 
        return context

    # to add logics and functionality to our form
    def form_valid(self, form): # form_valid() is a form of POST method since we are using 'CreateView', it is also a mrthod called once the form is posted successfully 
        cart_form_session = self.request.session.get('cart_id', None)  # this is the cart stored using session
        if cart_form_session:  # if we have cart in the session
            cart_object = Cart.objects.get(id=cart_form_session)
            form.instance.cart = cart_object  # .cart is from the Order database model
            form.instance.subtotal = cart_object.total  # '.subtotal' from the Order database model is assigned 'cart_object.total' which is inheriting from the Cart database model   
            form.instance.discount = 0 # discount is assigned 0
            form.instance.total = cart_object.total # .total from the Order database model is assigned 'cart_object.total' note that Order has field 'cart' having forignkey relating to the Cart database model
            form.instance.order_status = 'Order Received'
            del self.request.session['cart_id'] # this will delete the cart after the check out form has been submitted into the Order database, meaning after the order has been placed, immediately the cart details will be deleted 

        else: # if we do not have cart in the session
            return redirect('Ecommerce:homepage')

        return super().form_valid(form) # without returning 'super().form_valid(form)' we will encounter error



class CustomerRegisterView(CreateView):
    template_name = 'customer_register.html'
    form_class = CustomerRegisterForm
    success_url = reverse_lazy('Ecommerce:homepage')

    def form_valid(self, form):
        cust_username = form.cleaned_data.get('username')
        cust_password = form.cleaned_data.get('password')
        cus_email = form.cleaned_data.get('email')

        customer_create = User.objects.create_user(cust_username, cus_email, cust_password,) # note that django uses 'create_user()' function to create users using the django User database model, the 'cust_username, cust_password, cus_email' inside the () is from the form  
        # note that as seen above, we must arrange it well like username, email, password in the create_user() -> not arranging it will give us an error when we want to log in

        form.instance.user = customer_create  # note that .user is from the Customer database model which is a OneToOneField, which is assigned to 'customer_create'
        # print(form.instance.user) # this will give us the username of the customer
        
        login(self.request, customer_create) # the 'login()' function is a django built in function which logs in the user after authenticating the user, but here immediately the user has registered, then the customer_user is logined in

        return super().form_valid(form)


    def get_success_url(self):  # note that 'get_success_url()' will override the 'success_url' from above 
        if 'next' in self.request.GET:  # note that 'next' is from the get_success_urlwhich is a GET method
            next_url = self.request.GET.get('next') # we want to obtain the 'next' from the get_success_url therfore we use '.get()' 
            # print(next_url)
            return next_url
        else:
            return self.success_url         



class CustomerLogoutView(View):
    def get(self, request): # always include 'self' else we will get an error
        logout(request) # 'logout()' function is a function in django that automatically logs out a user
        return redirect('Ecommerce:homepage')  



class CustomerLoginView(FormView):
    template_name = 'customer_login.html'
    form_class = CustomerLoginForm
    success_url = reverse_lazy('Ecommerce:homepage')

    def form_valid(self, form):
        user_username = form.cleaned_data['username'] # we can also use 'form.cleaned_data.get('username')' its the same thing 
        # print(user_username)
        user_password = form.cleaned_data['password']
        # print(user_password)

        user_confirm = authenticate(username=user_username, password=user_password) # note that 'authenticate()' function is django properties for checking if the user data is contained in the database 
        if user_confirm is not None and user_confirm.customer: # this means that we have user in the User database and also we have same user in the Customer database model. note that '.customer' is the Customer database model which has user field with OneToOnekey linking the djabgo User
            # print('We have user')
            login(self.request, user_confirm) # since we have user in the database, then we are login the user in through the login() function
        else:
            # print('We do not have user')
            return render(self.request, self.template_name, {'form': self.form_class, 'error_form': 'Invalid credentials'})
                
        return super().form_valid(form)


    def get_success_url(self):  # note that 'get_success_url()' will override the 'success_url' from above 
        if 'next' in self.request.GET:  # note that 'next' is from the get_success_urlwhich is a GET method
            next_url = self.request.GET.get('next') # we want to obtain the 'next' from the get_success_url therfore we use '.get()' 
            # print(next_url)
            return next_url
        else:
            return self.success_url      




class CustomerProfileView(TemplateView):
    template_name = 'customerprofile.html'

    # we want to ensure that the user/customer is login before accessing this page
    def dispatch(self, request, *args, **kwargs):
        # this is to check if the user is authenticated and the user is in the Customer database model exist
        if request.user.is_authenticated and Customer.objects.filter(user = request.user).exists():
            # print(request.user)
            pass
        else:
            # print('not user available')
            return redirect('/login/?next=/profile/')

        return super().dispatch(request, *args, **kwargs)

    # once we are sure the user is log in and in the Customer database model, then we want to display the orders made by the particular customer
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_customer = self.request.user.customer # '.customer' is the database Customer model which has user field chaving foreignkey
        # print(user_customer)
        context['customer_data'] = user_customer
        
        # we want to obtain the order made by this particular user/customer
        customer_order = Order.objects.filter(cart__customer = user_customer).order_by('-id') # '-id' will give us the latest order made by the customer
        # note that Order database has cart field which has foriegnkey relating the Cart database model, also the Cart database has field of customer relating the Customer database model
        context['order_customer'] = customer_order 

        return context

# note that in the 'customerprofile.html' we used '{{ customer_data.user.username }}' same as email and username -> this is because .useris the field in the Customer database model with foreignkey relating to the User database model which has username, email
# {{ order.created_at| timesince }} not that the 'timesince' used will give us long long the order was made


class CustomerOrderDetailView(DetailView):
    template_name = 'customer_order_detail.html'
    model = Order
    context_object_name = 'customer_order_detail'
    # 'context_object_name' specifies the variable name of the model list in the template, it shows the name we want to display into the template(front end) with details/data from the model
    
    # we want to ensure that the user/customer is login before accessing this page
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user = request.user).exists():
            # print(request.user) 

            # we want to stop/restrict the customer/user from viewing orders not his/her own
            customer_order_id = self.kwargs['pk'] # 'pk' is from the url while self.kwargs[''] is used to obtain it 
            # print(customer_order_id)
            customer_order = Order.objects.get(id=customer_order_id)
            # we want to know if the customer/user is the orderer of the product
            if request.user.customer != customer_order.cart.customer:
                return redirect('Ecommerce:customer_profile')

        else:
            return redirect('/login/?next=/profile/') 

        return super().dispatch(request, *args, **kwargs)    

# note that the 'intcomma' is from the django humanize, it is used to converts an integer or a float to a string containing commas every three digits e.g 1000000 becomes 1,000,000


class ProductSearchView(TemplateView):
    template_name = 'search_product.html'
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_product_get = self.request.GET.get('product_search')
        # note that we are using 'request.GET' because it is a GET method not a POST method while we used .get() to obtain the name from the form input which has 'product-search' in the name
        # print(search_product_get)
        search_product_result = Product.objects.filter(Q(title__icontains = search_product_get) | Q(description__icontains = search_product_get) | Q(return_policy__icontains = search_product_get))
        # print(search_product_result) 
        context['search_product_display'] = search_product_result

        return context 

# note that django template filters are defined by using a pipe '|'
# trancatechars filter trancate the value if it is longer than the specified number of characters, same also as trancatewords


# admin pages code

class AdminLoginFormView(FormView):
    template_name = 'admin-pages/admin_create_form.html'
    form_class = CustomerLoginForm # am using the same form i used in creating for the Customer/user
    success_url = reverse_lazy('Ecommerce:admin_home')

    def form_valid(self, form):
        # print('Form is submitted')
        admin_username = form.cleaned_data.get('username')
        # print(admin_username)
        admin_password = form.cleaned_data.get('password') 
        # print(admin_password)

        # authenticate the user; note that the django has built-in User model where i have both my users/customers
        admin_user = authenticate(username = admin_username, password = admin_password)
        if admin_user is not None and Admin.objects.filter(user = admin_user).exists():
            # print('We have user')
            login(self.request, admin_user)
        else:
            # print('We dont have user')
            return render(self.request, self.template_name, {'form': self.form_class, 'error': 'Invalid credentials'})

        return super().form_valid(form)




# will be creating class based function here, to avoid repeting the dispatch code, and include it in the codes belew
class AdminRequiredMixin(object):
    # this will ensure the admin is log in to avoid hacking/authorize access to the page
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user = request.user).exists():
            pass
        else:
            return redirect('/admin-form/')

        return super().dispatch(request, *args, **kwargs)

        

class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = 'admin-pages/admin_home.html'
    
    # we want to display all the orders by the user/customer based on status of 'Order Received'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_orders'] = Order.objects.filter(order_status='Order Received').order_by('-id')

        return context



class AdminOrderDetailView(AdminRequiredMixin, DetailView):
    template_name = 'admin-pages/admin-order-detail.html'
    model = Order
    context_object_name = 'order_object'
    
    def get_context_data(self, **kwargs):
        # i had to get this from the Order database model else, i will have an error of 'ORDER_STATUS' not being defined
        ORDER_STATUS = (
        ('Order Received', 'Order Received'),
        ('Order Processing', 'Order Processing'),
        ('On The Way', 'On The Way'),
        ('Order Completed', 'Order Completed'),
        ('Order Canceled', 'Order Canceled')
        )

        context = super().get_context_data(**kwargs)
        context['all_status'] = ORDER_STATUS

        return context



class AdminOrderStatusChangeView(AdminRequiredMixin, View):
    def post(self, request, *args, **kwargs): # note that we are using 'def post(self, request, *args, **kwargs)' because our form is post method not get method 
        order_id = self.kwargs['order_status_pk']
        # print(order_id)
        order_object = Order.objects.get(id=order_id)

        new_order_status = request.POST.get('select_order')
        # print(new_order_status) 
        order_object.order_status = new_order_status # note that 'order_object' was defined above with the Order database model, we are now relating it to the order_status of the Order model using order_objects.order_status then assigning it to the mew_order_status
        order_object.save() # then save the changes

        return redirect(reverse_lazy('Ecommerce:admin_order_detail', kwargs={'pk': order_id})) 
        # 'pk' is from the url of 'admin_order_detail' which has <int:pk> while order_id is a variable which is defined above 
        # this will return it back to the particular order detail page with the particular pk 



class AdminAllOrderList(AdminRequiredMixin, ListView):
    template_name = 'admin-pages/admin_all_order.html'
    queryset = Order.objects.all().order_by('-id') # a queryset is a collection of data from a database, it represents a collection of objects from the database
    context_object_name = 'all_orders'
    


class ProductCreateFormView(AdminRequiredMixin, CreateView):
    template_name = 'admin-pages/create_product_list.html'
    form_class = ProductCreateForm
    success_url = reverse_lazy('Ecommerce:all_product_create')

    def form_valid(self, form): # once the form is filled/valid
        product_data = form.save() # we are saving the form once filled

        # to get more images once the 'more_image' filed is clicked to save it to the ProductImage database model
        images_more = self.request.FILES.getlist('more_images') # note that we are using .getlist() because we want to get all the images uploaded through this filed, since we added 'multiple': True in the forms.py 
        # we want to loop through all the images we want to upload using the for loop
        for product_images in images_more: # we want to save it in the ProductImage database model
            ProductImage.objects.create(product = product_data, image = product_images)

        return super().form_valid(form)



class AllProductListView(AdminRequiredMixin, ListView):
    template_name = 'admin-pages/all_product_list.html'
    queryset = Product.objects.all().order_by('-id')
    context_object_name = 'all_products'
    


class CategoryCreateFormView(AdminRequiredMixin, CreateView):
    template_name = 'admin-pages/category_create.html'
    form_class = CategoryCreateForm
    success_url = reverse_lazy('Ecommerce:categories_list')

    def form_valid(self, form):
        form.save()

        return super().form_valid(form) 



class AllCategoryListView(AdminRequiredMixin, ListView):
    template_name = 'admin-pages/all_category_list.html'
    queryset = Category.objects.all().order_by('-id')
    context_object_name = 'all_categories'




class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'

