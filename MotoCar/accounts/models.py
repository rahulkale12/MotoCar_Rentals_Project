from django.db import models

# Create your models here.
class Customer_register(models.Model):
    name= models.CharField(max_length=100)
    mobile = models.BigIntegerField(unique=True)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.IntegerField()
    address = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class Profile_pic(models.Model):
    profile_image = models.ImageField(upload_to="profileImage/")
    customer = models.ForeignKey(Customer_register,on_delete=models.CASCADE)
    