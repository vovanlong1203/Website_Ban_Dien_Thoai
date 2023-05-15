from django.db import models
import datetime
import os
import uuid
from django.contrib.auth.models import User
# Create your models here.

def get_file_path(request,filename):
    original_filename = filename
    nowTime = datetime.datetime.now().strftime("%Y-%m-%d%H:%M:%S")
    filename = "%s%s" % (nowTime, original_filename)
    return os.path.join('uploads/',filename)

class Category(models.Model):
    name = models.CharField(max_length=255,null=False, blank=True)
    image = models.ImageField(upload_to=get_file_path,null=True,blank=True)
    description = models.TextField(max_length=500,null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=255,null=False, blank=True)
    image = models.ImageField(upload_to=get_file_path,null=True,blank=True)
    quantity = models.IntegerField(null=False, blank=False)
    description = models.TextField(max_length=1000,null=False, blank=False)
    original_price = models.FloatField(null=False, blank=False)
    selling_price = models.FloatField(null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    trending = models.BooleanField(default=False,help_text="0=default, 1=Trending")
    created_at = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.name

class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    completed = models.BooleanField(default=False) 

    def __str__(self):
        return str(self.id)
    
    @property
    def total_price(self):
        cartitems = self.cartitems.all()
        total = sum([item.price for item in cartitems])
        return total
    
    @property
    def num_of_items(self):
        cartitems = self.cartitems.all()
        quantity = sum([item.quantity for item in cartitems])
        return quantity
    @property
    def num_of_product(self):
        cartitems = self.cartitems.all()
        lst = set()
        for item in cartitems:
            lst.add(item.product.name)
        return len(lst)

    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    cart = models.ForeignKey(Cart, on_delete= models.CASCADE, related_name="cartitems")
    quantity = models.IntegerField(default=0)
    
    def __str__(self):
        return self.product.name+" " + self.cart.user.username +""
    
    @property
    def price(self):
        new_price = self.product.selling_price * self.quantity
        return new_price
    
class Review(models.Model):
    user = models.ForeignKey(User,models.CASCADE)
    product = models.ForeignKey(Product,models.CASCADE)
    comment = models.TextField(max_length=255)
    rate = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)
    
    @property
    def getIdProduct(self):
        return self.product.id


class Order(models.Model):
    STATUS =(
        ('Pending','Pending'),
        ('Order Confirmed','Order Confirmed'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,null=True,choices=STATUS, default='Pending')
    total = models.FloatField()

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE, related_name='oderitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,)
    price = models.FloatField()
    quantity = models.IntegerField()
    total_price = models.FloatField()


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField(max_length=1000)
    



