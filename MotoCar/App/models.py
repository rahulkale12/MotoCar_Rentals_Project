from django.db import models
from accounts.models import Customer_register


# Create your models here.
class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.state.name}"


class Car(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    fuel_type = models.CharField(max_length=50)
    gear_type = models.CharField(max_length=50)
    price_per_day = models.IntegerField()  
    price_per_hour = models.IntegerField()  
    image = models.ImageField(upload_to='car_images/')
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    

    def __str__(self):
        return f"{self.name} ({self.company})- {self.city}, {self.state}"


class Bike(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    fuel_type = models.CharField(max_length=20)
    price_per_day = models.IntegerField()
    price_per_hour = models.IntegerField()
    image = models.ImageField(upload_to='bike_images/') 
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)



    def __str__(self):
        return f"{self.name} ({self.company})- {self.city}, {self.state}"


class Cart(models.Model):
    customer = models.ForeignKey(Customer_register, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE,  null=True, blank=True)
    
    def __str__(self):

        car_name = self.car.name if self.car else 'No car'
        bike_name = self.bike.name if self.bike else 'No bike'
        return f"Cart for {self.customer.name} - Car: {car_name}, Bike: {bike_name}"
    

class Rented_vehicles(models.Model):
    customer = models.ForeignKey(Customer_register, on_delete=models.CASCADE)
    car = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True , related_name="car_rent")
    bike = models.ForeignKey(Cart, on_delete=models.CASCADE,  null=True, blank=True, related_name="bike_rent")
    delivery_type = models.CharField(max_length=50, choices=[('pickup', 'Self Pickup'),('delivery','Delivery')],null=True, blank=True)
    pickup_date = models.DateField(null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    pickup_time = models.TimeField(null=True, blank=True)
    delivery_time = models.TimeField(null=True, blank=True)
    return_time = models.TimeField(null=True, blank=True)
    pickup_location = models.CharField(max_length=300,blank=True,null=True)
    delivery_location = models.CharField(max_length=300, blank=True, null=True)
    license_file = models.FileField(upload_to='licenceFile/')
    total_price = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)
    payment_id = models.CharField(max_length=200)
    
    def __str__(self):
         return f"Rented Vehicle for {self.customer.name}"







