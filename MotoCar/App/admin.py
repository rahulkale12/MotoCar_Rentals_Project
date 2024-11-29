from django.contrib import admin
from App.models import Car,Bike,State,City,Rented_vehicles

# Register your models here.
admin.site.register(Car)
admin.site.register(Bike)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Rented_vehicles)
