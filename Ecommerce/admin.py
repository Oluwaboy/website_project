from django.contrib import admin

from Ecommerce.models import Category, Product, Customer, Cart, CartProduct, Order, Admin, ProductImage

# Register your models here.

admin.site.register([Category, Product, Customer, Cart, CartProduct, Order, Admin, ProductImage])


