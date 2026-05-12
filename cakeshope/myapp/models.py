from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Create your models here.
class CustomeUser(AbstractUser):
    u_mobile=models.CharField(max_length=10)
    u_address=models.TextField()
    u_pincode=models.CharField(max_length=6)
    def __str__(self):
        return self.username
    
class Categories(models.Model):
    category_name=models.CharField(max_length=50)
    def __str__(self):
        return self.category_name

class Flavour(models.Model):
    flavour_name=models.CharField(max_length=50)
    def __str__(self):
        return self.flavour_name
    
class Product(models.Model):
    category=models.ForeignKey(Categories,on_delete=models.CASCADE)
    flavour=models.ForeignKey(Flavour,on_delete=models.CASCADE)
    p_name=models.CharField(max_length=50)
    p_weight=models.FloatField()
    p_price=models.FloatField()
    p_desc=models.TextField()
    p_img=models.ImageField(upload_to='products/')
    def __str__(self):
        return str(self.id)
   

class Order(models.Model):
    u_id=models.ForeignKey(CustomeUser,on_delete=models.CASCADE)
    o_date=models.DateField(auto_now_add=True)
    total_amount=models.FloatField()
    o_status=models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)
    
    # 1 1 12/10/2025 200 false 1 2 3 if o_id not in 
    # 2 1 13/10/205 300 false 2 1 2
    #3 1 13/10/205 500 false 3 
class Order_details(models.Model):
    o_id=models.ForeignKey(Order,on_delete=models.CASCADE)
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    # def __str__(self):
    #     return tuple(str(self.o_id),str(self.product_id),self.quantity)

class Payment(models.Model):
    u_id=models.ForeignKey(CustomeUser,on_delete=models.CASCADE)
    o_id=models.ForeignKey(Order,on_delete=models.CASCADE)
    payment_type=models.CharField(max_length=10)
    transition_id=models.CharField(null=True,max_length=50)
    payment_date=models.DateField(auto_now_add=True)
    payment_status=models.CharField(max_length=10)
    payment_amount=models.FloatField()

class Feedback(models.Model):
    u_id=models.ForeignKey(CustomeUser,on_delete=models.CASCADE)
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    feedback_date=models.DateField(auto_now_add=True)
    feedback_details=models.TextField()
    feedback_star=models.IntegerField()

class Gallery(models.Model):
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE,unique=True)
    img_p1=models.ImageField(upload_to='product_gallery/img1/')
    img_p2=models.ImageField(upload_to='product_gallery/img2/')
    img_p3=models.ImageField(upload_to='product_gallery/img3/')

class Cart(models.Model):
    user=models.ForeignKey(CustomeUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username

class Cartitem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
        


    
    
        
    
    



