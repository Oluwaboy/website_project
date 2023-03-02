from django.db import models

# this is django built-in function for users
from django.contrib.auth.models import User

# from django.utils import timezone

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True) # 'unique=True' means this field must be unique throughout the table i.e once entered a value in a field, the same value cannot be entered in any other instance of that model in any manner 
    # note that to fill the slug fiels always use hyphen(-) e.g instead of light food use light-food etc else we will have an error

    def __str__(self):
        return self.title  
        # note that 'self' will inherit and also display the attributes/properties of the specific class
        # 'self.title' will display/show the Category model according to the title not according to django format


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # foreignkey is a process through which the fields of one table can be used in another table flexibly, it helps in linking different tables/models to another
    # ForeignKey can be used to define many-to-one relationship; many-to-one relationship is used when one record of a model A is related to multiple records of another model B. 
    # 'many-to-one' relationship e.g a model Song has many-to-one relationship with model Album i.e, an album can have many songs, but one song cannot be part of multiple albums
    # it is good practice to name the many-to-one field with the same name as the related model in lowercase
    # one Category can have many products, but one product cannot have many category an example of many-to-one relationship 
    # 'on_delete=models.CASCADE' is the default value, it automatically deletes all the related records when a record is deleted e.g when a Category record is deleted, all the products records related to it will be deleted

    image = models.ImageField(upload_to = 'product_images') # 'upload_to' is the directory we want the image to to be stored which is assigned 'product_images' meaning that 'product_images' is the folder that will store the uploaded images
    marked_price = models.PositiveIntegerField() # 'PositiveIntegerField()' is an integer number represented in python by a int instance, it must be either positive or zero(0) it cannot be negative
    selling_price = models.PositiveIntegerField()
    description = models.TextField()
    warranty = models.CharField(max_length=300, null=True, blank=True) # 'null=True, blank=True' means the field can be left blank and null without filling 
    return_policy = models.CharField(max_length=300, null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0) # default=0 means the default value in this field is 0
 
    def __str__(self):
        return self.title  



# we want to add multiple images to the products
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    image = models.ImageField(upload_to='product/images')

    def __str__(self):
        return self.product.title





class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # One-To-One Field is used when one record of a model A is related to exactly one record of another model B. It is good practice to name the one-to-one field with the same name as that of the related model in lowercase
    # One-To-One Field example e.g a model Car has one-to-one relationship with a model Vehicle i.e a car is a vehicle 
    # also the user field above, the user is the same as the User(django built-in function)
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=300, null=True, blank=True)
    joined_on = models.DateTimeField(auto_now_add=True) # 'auto_now_add' will automatically add the exact time the customer joined if it is set =True but if False it wont add the time

    def __str__(self):
        return self.full_name 



class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    # on_delete=models.SET_NULL assigns NULL to the relational field when a record is deleted, provided null = True 
    # on_delete=models.SET_NULL -> means if we delete the referenced object, it will set the referred object(child object instance) as NULL e.g if a user profile has done a project, if we delete the user profile then the projects done by that user will be set to NULL 
    # also, if a post is deleted without deleting associated comments and set to be NULL
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Cart: ' + str(self.id) # self.id will display the id number of the Cart model


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField() 

    def __str__(self):
        return 'Cart: ' + str(self.cart.id) + ' CartProduct ' + str(self.id)  # cart.id is from the cart field having ForeignKey(Cart) in the CartProduct model with id numbers while self.id is the id of the CartProduct model



# this will be used in our database model according to the choices in the order_status field
ORDER_STATUS = (
    ('Order Received', 'Order Received'),
    ('Order Processing', 'Order Processing'),
    ('On The Way', 'On The Way'),
    ('Order Completed', 'Order Completed'),
    ('Order Canceled', 'Order Canceled')
)

# now = timezone.now()


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveIntegerField()  
    discount = models.PositiveIntegerField() 
    total = models.PositiveIntegerField() 
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    # created_at = models.DateTimeField(default = timezone.now) # default = timezone.now
    created_at = models.DateTimeField(auto_now_add=True) 
    # choices limits the input from the user to the particular values specified in the models, it also gives different options/alternatives

    def __str__(self):
        return 'Order: ' + str(self.id)



class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='admin_images')
    mobile = models.CharField(max_length=30)

    def __str__(self):
        return self.user.username  # user is the field in the Damin which has 'OneToOneField' relating the User database model having username, email and password 


