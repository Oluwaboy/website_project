from django.urls import path

from Ecommerce.views import *  # '*' means we are importing everything from views.py in the Ecommerce app

app_name = 'Ecommerce' # this will make the linking of pages easier and faster


# note that we are using '.as_view()' since it is django generic class function as seen in the views.py page
urlpatterns = [
    # Products and category related urls
    path('', HomeView.as_view(), name='homepage'),
    path('all-product/', All_ProductView.as_view(), name='all_products'),
    path('product/<slug:product_slug>', Product_detailView.as_view(), name='product_detail'), # <slug> can be used to get the details of the specific product same way <int> can be used to obtain the details of the specific product
    
    path('about/', AboutView.as_view(), name='aboutpage'),
    path('contact/', ContactView.as_view(), name='contactpage'),

    # cart related urls
    path('add-to-cart/<int:cart_product_id>/', Add_to_cart.as_view(), name='add_to_cart'), # 'int' is an integer meaning cart_product_id should be in integer for this url to be functional in the front/html page
    path('my-cart/', MyCartView.as_view(), name='my_cart'),
    path('manage-cart/<int:cart_functions>/', ManageCartView.as_view(), name='manage_cart'),
    path('empty-cart/', EmptyCartView.as_view(), name='empty_cart'),

    path('checkout/', CheckoutView.as_view(), name='checkout'),

    # user details
    path('register/', CustomerRegisterView.as_view(), name='user_register'),
    path('login/', CustomerLoginView.as_view(), name='user_login'),
    path('logout/', CustomerLogoutView.as_view(), name='user_logout'),

    path('profile/', CustomerProfileView.as_view(), name='customer_profile'),
    path('profile/order-<int:pk>/', CustomerOrderDetailView.as_view(), name='customer_orderdetail'),

    path('search-product/', ProductSearchView.as_view(), name='search_product'),

    # admin details
    path('admin-home/', AdminHomeView.as_view(), name='admin_home'),

    path('admin-form/', AdminLoginFormView.as_view(), name='admin_create_form'), # this is the form for admin to login

    path('admin-order/<int:pk>/', AdminOrderDetailView.as_view(), name='admin_order_detail'), 

    path('admin-order/<int:order_status_pk>-change/', AdminOrderStatusChangeView.as_view(), name='admin_order_change'),

    path('admin-order-list/', AdminAllOrderList.as_view(), name='admin_all_order_list'),

    path('create-product/', ProductCreateFormView.as_view(), name='product_create'),

    path('all-product-create/', AllProductListView.as_view(), name='all_product_create'),

    path('category-create/', CategoryCreateFormView.as_view(), name='category_create'),

    path('category-lists/', AllCategoryListView.as_view(), name='categories_list'),

]

