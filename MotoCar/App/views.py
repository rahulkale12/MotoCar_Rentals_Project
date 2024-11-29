from django.shortcuts import render,redirect
from App.models import Car, Bike,State,City,Cart, Rented_vehicles
from accounts.models import Customer_register
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.contrib import messages
from datetime import date
from django.utils import timezone
from django.conf import settings
import os
from django.core.files.storage import FileSystemStorage


# Create your views here.
def index(request):
    cars = Car.objects.all()[:6]
    bikes = Bike.objects.all()[:6]
    return render(request, "index.html" , {'cars':cars,'bikes':bikes})

def cars(request):
    car_filter = Car.objects.all()
    states = State.objects.all()
    cities = City.objects.all()
    if request.method == "POST":
        state = request.POST['state']
        city = request.POST['city']
        name = request.POST['name']
        company = request.POST['company']
        min_price = request.POST['min_price']
        max_price = request.POST['max_price']
        fuel_type = request.POST['fuel_type']
        gear_type = request.POST['gear_type']

        if state:
            car_filter = car_filter.filter(state__name__icontains= state )
        
        if city:
            car_filter = car_filter.filter(city__name__icontains = city )

        if name:
            car_filter = car_filter.filter(name__icontains=name)

        if company:
            car_filter = car_filter.filter(company__icontains=company)
        
        if min_price:
            car_filter = car_filter.filter(price_per_day__gte=min_price)

        if max_price:
            car_filter = car_filter.filter(price_per_day__lte=max_price)

        if fuel_type:
            car_filter = car_filter.filter(fuel_type__icontains=fuel_type)
        
        if gear_type:
            car_filter = car_filter.filter(gear_type__icontains = gear_type)
        
        return render(request, 'cars.html',{'car_filter':car_filter,'states': states,
        'cities': cities})
    return render(request, 'cars.html',{'car_filter':car_filter,'states': states,
        'cities': cities})
        

def bikes(request):
    bike_filter = Bike.objects.all().order_by('id')
    states = State.objects.all()
    cities = City.objects.all()
    if request.method == "POST":
        state = request.POST['state']
        city = request.POST['city']
        name = request.POST['name']
        company = request.POST['company']
        min_price = request.POST['min_price']
        max_price = request.POST['max_price']
        fuel_type = request.POST['fuel_type']
        

        if state:
            bike_filter = bike_filter.filter(state__name__icontains= state )
        
        if city:
            bike_filter = bike_filter.filter(city__name__icontains = city )

        if name:
            bike_filter = bike_filter.filter(name__icontains=name)

        if company:
            bike_filter = bike_filter.filter(company__icontains=company)
        
        if min_price:
            bike_filter = bike_filter.filter(price_per_day__gte=min_price)

        if max_price:
            bike_filter = bike_filter.filter(price_per_day__lte=max_price)

        if fuel_type:
            bike_filter = bike_filter.filter(fuel_type__icontains=fuel_type)
    
        
        return render(request, 'bikes.html',{'bike_filter':bike_filter,'states': states,
        'cities': cities})
    return render(request, 'bikes.html',{'bike_filter':bike_filter,'states': states,
        'cities': cities})
        
   

def my_rentals(request):
    return render(request, "my_rentals.html")




def add_car_to_cart(request, car_id):
    customer_id = request.session.get('id')
    if not customer_id:
        return redirect('/accounts/login/')
    
    try:
        customer = Customer_register.objects.get(id=customer_id)
    except Customer_register.DoesNotExist:
        return redirect('/cars/')

    try:
        car = Car.objects.get(id=car_id)
    except ObjectDoesNotExist:
        return redirect('/cars/')


    cart_check = Cart.objects.filter(customer=customer, car=car).first()
    if cart_check:
        return redirect('/my_cart/')
    else:
        cart = Cart.objects.create(customer=customer, car=car)

    # Update the session to indicate that the cart is not empty

    request.session['cart_empty'] = False

    return redirect('/my_cart/')



def add_bike_to_cart(request, bike_id):
    customer_id = request.session.get('id')
    if not customer_id:
        return redirect('/accounts/login/')
    
    try:
        customer = Customer_register.objects.get(id=customer_id)
    except Customer_register.DoesNotExist:
        return redirect('/bikes/')

    try:
        bike = Bike.objects.get(id=bike_id)
    except ObjectDoesNotExist:
        return redirect('/bikes/')


    cart_check = Cart.objects.filter(customer=customer, bike=bike).first()
    if cart_check:
        return redirect('/my_cart/')
    else:
        cart = Cart.objects.create(customer=customer, bike=bike)

    # Update the session to indicate that the cart is not empty

    request.session['cart_empty'] = False

    return redirect('/my_cart/')




def my_cart(request):
    customer_id = request.session.get('id')
    if not customer_id:
        return redirect('/accounts/login/')
    
    try:
        customer = Customer_register.objects.get(id = customer_id)
    except Customer_register.DoesNotExist:
        return redirect("/accounts/regsiter/")
    
    carts = Cart.objects.filter(customer = customer)
    # cart_ids = [cart.id for cart in carts]
    return render (request, "my_cart.html",{'carts':carts})







# def checkout(request):
#     customer_id = request.session.get('id')
    
#     if not customer_id:
#         return redirect('/accounts/login/')
    
#     try:
#         customer = Rented_vehicles.objects.get(id=customer_id)
#     except Customer_register.DoesNotExist:
#         return redirect('/accounts/register/')
    
#     carts = Rented_vehicles.objects.filter(customer=customer)

#     for cart in carts:
#         if cart.car:
#             cart.pickup_location = cart.car.city.name if cart.car.city else ''
#         elif cart.bike:
#             cart.pickup_location = cart.bike.city.name if cart.bike.city else ''

#     if request.method == "POST":
#         cart_id = request.POST.get('cart_id')

#         if not cart_id:
#             messages.error(request, "Cart ID is required.")
#             return redirect('/cars/')

#         try:
#             cart = Cart.objects.get(id=cart_id)
#         except ObjectDoesNotExist:
#             return redirect('/cars/')
        
#         # Process form fields
#         cart.delivery_type = request.POST.get('delivery_type')
#         pickup_date_str = request.POST.get('pickup_date', '')
#         return_date_str = request.POST.get('return_date', '')
#         pickup_time = request.POST.get('pickup_time', '')
#         delivery_time = request.POST.get('delivery_time', '')
#         return_time = request.POST.get('return_time', '')
#         pickup_location = request.POST.get('pickup_location', '')
#         delivery_location = request.POST.get('delivery_location', '')
#         license_image = request.FILES.get('license_image')
#         delivery_date_str = request.POST.get('delivery_date', '')  # Delivery date field

#         # Get today's date to compare with selected dates
#         today_date = timezone.now().date()

      

#         # If pickup is selected, validate pickup date and times
#         if cart.delivery_type == 'pickup':
#             if not pickup_date_str:
#                 messages.error(request, "Please select a pickup date.")
#                 return render(request, "my_cart.html", {"carts": carts})

#             try:
#                 pickup_date = datetime.strptime(pickup_date_str, '%Y-%m-%d').date()
#                 # Ensure pickup date is not in the past
#                 if pickup_date < today_date:
#                     messages.error(request, "Pickup date cannot be in the past.")
#                     return render(request, "my_cart.html", {"carts": carts})

#                 # Ensure return date is after pickup date
#                 if return_date_str:
#                     return_date = datetime.strptime(return_date_str, '%Y-%m-%d').date()
#                     if return_date <= pickup_date:
#                         messages.error(request, "Return date must be after the pickup date.")
#                         return render(request, "my_cart.html", {"carts": carts})

#                 cart.pickup_date = pickup_date
#                 cart.return_date = return_date if return_date_str else None
#                 # Set delivery date to None when pickup is selected
#                 cart.delivery_date = None

#                 if cart.car:
#                     cart.pickup_location = cart.car.city.name if cart.car.city else ''
#                 elif cart.bike:
#                     cart.pickup_location = cart.bike.city.name if cart.bike.city else ''

#                 pickup_location = cart.pickup_location

#             except ValueError:
#                 messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
#                 return render(request, "my_cart.html", {"carts": carts})

#             # Validate pickup time and return time
#             if not pickup_time or not return_time:
#                 messages.error(request, "Both pickup time and return time are required when pickup is selected.")
#                 return render(request, "my_cart.html", {"carts": carts})

#             try:
#                 # Only parse the time if it's provided, else leave it as None
#                 if pickup_time != "None":
#                     cart.pickup_time = datetime.strptime(pickup_time, '%H:%M').time()

#                 if return_time != "None":
#                     cart.return_time = datetime.strptime(return_time, '%H:%M').time()
#             except ValueError:
#                 messages.error(request, "Invalid time format. Use HH:MM.")
#                 return render(request, "my_cart.html", {"carts": carts})

#             # Validate pickup location (Ensure it is not None or empty string)
#             if not pickup_location or pickup_location.lower() == 'none':
#                 messages.error(request, "Pickup location is required when pickup is selected.")
#                 return render(request, "my_cart.html", {"carts": carts})
            

#         # If delivery is selected, validate delivery date and times
#         elif cart.delivery_type == 'delivery':
#             if not delivery_date_str:
#                 messages.error(request, "Please select a delivery date.")
#                 return render(request, "my_cart.html", {"carts": carts})

#             try:
#                 delivery_date = datetime.strptime(delivery_date_str, '%Y-%m-%d').date()

#                 # Ensure delivery date is not in the past
#                 if delivery_date < today_date:
#                     messages.error(request, "Delivery date cannot be in the past.")
#                     return render(request, "my_cart.html", {"carts": carts})

#                 # Ensure return date is after delivery date
#                 if return_date_str:
#                     return_date = datetime.strptime(return_date_str, '%Y-%m-%d').date()
#                     if return_date <= delivery_date:
#                         messages.error(request, "Return date must be after the delivery date.")
#                         return render(request, "my_cart.html", {"carts": carts})

#                 cart.delivery_date = delivery_date
#                 cart.return_date = return_date if return_date_str else None
#                 # Set pickup date to None when delivery is selected
#                 cart.pickup_date = None

#             except ValueError:
#                 messages.error(request, "Invalid delivery date format.")
#                 return render(request, "my_cart.html", {"carts": carts})

#             # Validate delivery time and return time
#             if not delivery_time or not return_time:
#                 messages.error(request, "Both delivery time and return time are required when delivery is selected.")
#                 return render(request, "my_cart.html", {"carts": carts})

#             try:
#                  # Only parse the time if it's provided, else leave it as None
                # if pickup_time != "None":
                #     cart.pickup_time = datetime.strptime(pickup_time, '%H:%M').time()

#                 if return_time != "None":
#                     cart.return_time = datetime.strptime(return_time, '%H:%M').time()
#             except ValueError:
#                 messages.error(request, "Invalid time format. Use HH:MM.")
#                 return render(request, "my_cart.html", {"carts": carts})
            
            

#             # Validate delivery location (Ensure it is not None or empty string)
#             if not delivery_location or delivery_location.lower() == 'none':
#                 messages.error(request, "Delivery location is required when delivery is selected.")
#                 return render(request, "my_cart.html", {"carts": carts})

#         # Validate return date
#         if return_date_str and not cart.delivery_type:
#             try:
#                 return_date = datetime.strptime(return_date_str, '%Y-%m-%d').date()
#                 # Ensure return date is after pickup or delivery date
#                 if cart.pickup_date and return_date <= cart.pickup_date:
#                     messages.error(request, "Return date must be after the pickup date.")
#                     return render(request, "my_cart.html", {"carts": carts})

#                 if cart.delivery_date and return_date <= cart.delivery_date:
#                     messages.error(request, "Return date must be after the delivery date.")
#                     return render(request, "my_cart.html", {"carts": carts})

#                 cart.return_date = return_date

#             except ValueError:
#                 messages.error(request, "Invalid return date format.")
#                 return render(request, "my_cart.html", {"carts": carts})

#         # Handle locations and license image
#         if cart.delivery_type == 'pickup':
#             cart.delivery_location = None
#             cart.delivery_time = None
#             cart.delivery_date = None
#         elif cart.delivery_type == 'delivery':
#             cart.pickup_location = None
#             cart.pickup_time = None
#             cart.pickup_date = None

#         cart.pickup_location = pickup_location
#         cart.delivery_location = delivery_location
#         cart.license_image = license_image

    
#         if cart.delivery_type == 'pickup' and cart.pickup_date and cart.return_date:
#             rent_duration = (cart.return_date - cart.pickup_date).days
#         elif cart.delivery_type == 'delivery' and cart.delivery_date and cart.return_date:
#             rent_duration = (cart.return_date - cart.delivery_date).days
#         elif cart.delivery_type == 'delivery' and cart.delivery_date:
#             rent_duration = 1  # Default 1 day duration for delivery if return date is not specified
#         else:
#             messages.error(request, "Please enter valid pickup and return dates.")
#             return render(request, "my_cart.html", {"carts": carts})

#         # Ensure rent duration is positive
#         if rent_duration <= 0:
#             messages.error(request, "Please enter valid pickup or delivery and return dates.")
#             return render(request, "my_cart.html", {"carts": carts})
        
#         print(f"Rent Duration: {rent_duration} days")

#         # Calculate total price for car or bike
#         if cart.car:
#             cart.total_price = cart.car.price_per_day * rent_duration
#         elif cart.bike:
#             cart.total_price = cart.bike.price_per_day * rent_duration

#         cart.grand_total_price = cart.total_price
#         cart.save()

#         print(f"Grand Total Price: {cart.grand_total_price}")

        

#         # Only proceed to checkout if everything is valid
#         return redirect('/checkout/')

#     return render(request, "rented_vehicles.html", {"carts": carts})




def checkout(request,id):
    customer_id = request.session.get('id')
    customer = Customer_register.objects.get(id=customer_id)
    cart = Cart.objects.get(id=id)
    if cart.car:
            # print(cart.car.city.name)
            pickup_location = cart.car.city.name if cart.car.city else ""
            return render(request, "checkout.html",{"cart":cart, "pickup_location":pickup_location})
    elif cart.bike:
            pickup_location = cart.bike.city.name if cart.bike.city else ""
            return render(request, "checkout.html",{"cart":cart, "pickup_location":pickup_location})   
      
            
    return render(request, "checkout.html",{"cart":cart, "pickup_location":pickup_location})





    

# def checkouts(request):
#     customer_id = request.session.get('id')
#     customer = Customer_register.objects.get(id=customer_id)
#     carts = Cart.objects.filter(customer = customer)
#     pickup_location = None

#     for cart in carts:
#         # Check if the cart contains both a car and a bike
#         if cart.car and cart.bike:
#             # Both car and bike in the cart
#             if cart.car.city.name != cart.bike.city.name:
#                 # If the cities are different, show an error message and redirect
#                 messages.info(request, "If you want to rent multiple vehicles, please select them from the same city.")
#                 return render(request, "checkouts.html",{"carts":carts})  # Redirect immediately to the cart page
#             pickup_location = cart.car.city.name if cart.car.city else "None"
        
#         elif cart.car:
#             # Only car in the cart
#             pickup_location = cart.car.city.name if cart.car.city else ""
        
#         elif cart.bike:
#             # Only bike in the cart
#             pickup_location = cart.bike.city.name if cart.bike.city else ""
     
        
#     return render(request, "checkouts.html",{"carts":carts, "pickup_location":pickup_location})


##############################################################################################################################################


def checkouts(request):
    customer_id = request.session.get('id')
    customer = Customer_register.objects.get(id=customer_id)
    carts = Cart.objects.filter(customer=customer)
    pickup_location = None

    for cart in carts:
        if cart.car and cart.bike:
 
            if cart.car.city.name != cart.bike.city.name:
                messages.info(request, "If you want to rent multiple vehicles, please select them from the same city .")
                return render(request, "my_cart.html", {"carts": carts})  
        
        elif cart.car:
           
            if pickup_location is None:
                pickup_location = cart.car.city.name if cart.car.city else ""
            elif pickup_location != (cart.car.city.name if cart.car.city else "" ):
                messages.info(request, "If you want to rent multiple vehicles, please select them from the same city so filter out by city.")
                return render(request, "my_cart.html", {"carts": carts})  
            
        
        elif cart.bike:
            
            if pickup_location is None:
                pickup_location = cart.bike.city.name if cart.bike.city else ""
            elif pickup_location != (cart.bike.city.name if cart.bike.city else ""):
                messages.info(request, "If you want to rent multiple vehicles, please select them from the same city so filter out by city.")
                return render(request, "my_cart.html", {"carts": carts})

    return render(request, "checkouts.html", {"carts": carts, "pickup_location": pickup_location})



########################################################################################################################################



def validate_form_multiple(request):
    
    customer_id = request.session.get("id")

    if not customer_id:
        return redirect("/accounts/login/")
    
    try:
        customer = Customer_register.objects.get(id=customer_id)
    except Customer_register.DoesNotExist:
        return redirect("/accounts/register/")
    
    carts = Cart.objects.filter(customer=customer)
   


    if request.method == "POST":
        
        delivery_type = request.POST.get("delivery_type")
        pickup_date = request.POST.get("pickup_date")
        delivery_date = request.POST.get("delivery_date")
        return_date = request.POST.get("return_date")
        pickup_time = request.POST.get("pickup_time")
        delivery_time = request.POST.get("delivery_time")
        return_time = request.POST.get("return_time")
        pickup_location = request.POST.get("pickup_location")
        delivery_location = request.POST.get("delivery_location")
        license_image = request.FILES.get("license_image")


        today_date = timezone.now().date()

        if license_image:
            # Save the image to the 'licenceFile' directory inside the 'media' folder
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'licenceFile'))
            filename = fs.save(license_image.name, license_image)
            # license_image_url = fs.url(filename)  # Get the URL of the uploaded image
        else:
            # license_image_url = None
            filename = None

       


        
        # Pickup code


        if delivery_type == "pickup":
            # print("hellorahul",delivery_type)
            if not pickup_date:
                messages.info(request, "Please select Pickup Date")
                return render(request, "checkouts.html", {"carts": carts})
            
            try:
                pickup_date = datetime.strptime(pickup_date , '%Y-%m-%d' ).date()

                if pickup_date < today_date:
                        messages.info(request, "Pickup date cannot be in past.")
                        return render(request, "checkouts.html" ,{"carts":carts})
                
                if return_date:
                    return_date = datetime.strptime(return_date, "%Y-%m-%d").date()

                    if return_date <= pickup_date:
                        messages.info(request, "return date must be after pickup date")
                        return render(request, "checkouts.html",{"carts":carts})
                    
                
                pickup_date = pickup_date
                return_date = return_date    

                delivery_date= None 
   
            except ValueError:
                messages.info(request, "Invalid date format, please date in YY-MM-DD")
                return render(request, "checkouts.html",{"carts":carts})
            
            if not return_date:
                    messages.info(request, "Please select return date")
                    return render(request, "checkouts.html" , {"carts":carts})
                

            if not return_time and pickup_time:
                messages.info(request, "Please select pickup and return time")
                return render(request, "checkouts.html" ,{"carts":carts})
            
            try:
                if pickup_time != "None":
                    pickup_time = datetime.strptime(pickup_time, "%H:%M").time()
            

                if return_time != "None":
                    return_time = datetime.strptime(return_time, "%H:%M").time()
               
                    
            except ValueError:
                messages.info(request, "Invalid date format, please use HH:MM")
                return render(request, "checkouts.html" ,{"carts":carts})
            
            delivery_location = "None"
            delivery_time = "None"
            delivery_date = "None"


            pickup_location = pickup_location if pickup_location else "None"
            license_image = license_image

            
            rent_duration = 0

            if delivery_type == "pickup" and pickup_date and return_date:
                rent_duration += (return_date - pickup_date).days
            else:
                messages.info(request, "please select dates to calculate total_price")
                return render(request, "checkout.html", {"carts":carts})
            
        
            total_price = 0

            for cart in carts:
                if cart.car:
                    total_price  += cart.car.price_per_day * rent_duration 
                elif cart.bike:
                    total_price  += cart.bike.price_per_day * rent_duration
                elif cart.car and cart.bike:
                    total_price  += (cart.car.price_per_day + cart.bike.price_per_day) * rent_duration
            


            cart_ids = ','.join([str(cart.id) for cart in carts])

            return redirect(f"/payment_multiple/{cart_ids}/{total_price}/{delivery_type}/{delivery_location}/{delivery_date}/{delivery_time}/{pickup_date}/{pickup_time}/{pickup_location}/{return_date}/{return_time}/{filename}/")
                                      
       


        elif delivery_type=="delivery":
            # print("king",delivery_type)
            if not delivery_date:
                messages.info(request, "Please select Delivery Date")
                return render(request, "checkouts.html" , {"carts": carts})
            
            try:
                 
                delivery_date = datetime.strptime(delivery_date , '%Y-%m-%d' ).date()

                if delivery_date < today_date:
                    messages.info(request, "Delivery date cannot pe past to preset date")
                    return render(request, "checkouts.html",{"carts":carts})
                
                if return_date:
                    return_date = datetime.strptime(return_date, "%Y-%m-%d").date()

                    if return_date <= delivery_date:
                        messages.info(request, "return date cannot be same as delivery date")
                        return render(request, "checkouts.html",{"carts":carts})
                    
                
                delivery_date = delivery_date if delivery_date else "None"
                return_date = return_date   

                
            except ValueError:
                messages.info(request, "Invalid date format, please date in YY-MM-DD")
                return render(request, "checkouts.html",{"carts":carts})
            
            if not return_date:
                    messages.info(request, "Please select return date")
                    return render(request, "checkouts.html" , {"carts":carts})
                
            

            if not return_time and delivery_time:
                messages.info(request, "Please select pickup and return time") 
                return render(request, "checkouts.html", {"carts":carts})
            
            try:
                if delivery_time != "None":
                    delivery_time = datetime.strptime(delivery_time, "%H:%M").time()

                if return_time != "None":
                    return_time = datetime.strptime(return_time, "%H:%M").time()
                    
            except ValueError:
                messages.info(request, "Invalid date format, please use HH:MM")
                return render(request, "checkouts.html" ,{"carts":carts})
            
            
            if not delivery_location or delivery_location.lower() == 'none':
                messages.error(request, "Delivery location is required when delivery is selected.")
                return render(request, "checkouts.html" , {"carts": carts})
            
           
            pickup_location = "None"
            pickup_time = "None"
            pickup_date = "None"


            delivery_location = delivery_location if delivery_location else "None"
            license_image = license_image


            rent_duration =0

           
            if delivery_type == "delivery" and delivery_date and return_date:
                rent_duration += (return_date - delivery_date).days
            

            total_price = 0

            for cart in carts:
                if cart.car:
                    total_price  += cart.car.price_per_day * rent_duration
                elif cart.bike:
                    total_price  += cart.bike.price_per_day *rent_duration
                elif cart.car and cart.bike:
                    total_price  += (cart.car.price_per_day + cart.bike.price_per_day) * rent_duration


            cart_ids = ','.join([str(cart.id) for cart in carts])

            return redirect(f"/payment_multiple/{cart_ids}/{total_price}/{delivery_type}/{delivery_location}/{delivery_date}/{delivery_time}/{pickup_date}/{pickup_time}/{pickup_location}/{return_date}/{return_time}/{filename}")
     

    return render(request, "checkouts.html" ,{"carts":carts})





##########################################################################################################################################################



def validate_form_single(request,id):
    
    customer_id = request.session.get("id")

    if not customer_id:
        return redirect("/accounts/login/")
    
    try:
        customer = Customer_register.objects.get(id=customer_id)
    except Customer_register.DoesNotExist:
        return redirect("/accounts/register/")
    
    cart = Cart.objects.get(id=id)
   


    if request.method == "POST":
        
        delivery_type = request.POST.get("delivery_type")
        pickup_date = request.POST.get("pickup_date")
        delivery_date = request.POST.get("delivery_date")
        return_date = request.POST.get("return_date")
        pickup_time = request.POST.get("pickup_time")
        delivery_time = request.POST.get("delivery_time")
        return_time = request.POST.get("return_time")
        pickup_location = request.POST.get("pickup_location")
        delivery_location = request.POST.get("delivery_location")
        license_image = request.FILES.get("license_image")
       


        today_date = timezone.now().date()

      
        if license_image:
            # Save the image to the 'licenceFile' directory inside the 'media' folder
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'licenceFile'))
            filename = fs.save(license_image.name, license_image)
            # license_image_url = fs.url(filename)  # Get the URL of the uploaded image
        else:
            # license_image_url = None
            filename = None

        
         # Pickup code


        if delivery_type == "pickup":
            # print("hellorahul",delivery_type)
            if not pickup_date:
                messages.info(request, "Please select Pickup Date")
                return render(request, "checkout.html", {"cart": cart})
            
            try:
                pickup_date = datetime.strptime(pickup_date , '%Y-%m-%d' ).date()

                if pickup_date < today_date:
                        messages.info(request, "Pickup date cannot be in past.")
                        return render(request, "checkout.html" ,{"cart":cart})
                
                if return_date:
                    return_date = datetime.strptime(return_date, "%Y-%m-%d").date()

                    if return_date <= pickup_date:
                        messages.info(request, "return date must be after pickup date")
                        return render(request, "checkout.html",{"cart":cart})
                    
                
                pickup_date = pickup_date
                return_date = return_date    

                delivery_date= None 
   
            except ValueError:
                messages.info(request, "Invalid date format, please date in YY-MM-DD")
                return render(request, "checkout.html",{"cart":cart})
            
            if not return_date:
                    messages.info(request, "Please select return date")
                    return render(request, "checkout.html" , {"cart":cart})
                
            

            if not return_time and pickup_time:
                messages.info(request, "Please select pickup and return time")
                return render(request, "checkout.html" ,{"cart":cart})
            
            try:
                if pickup_time != "None":
                    pickup_time = datetime.strptime(pickup_time, "%H:%M").time()
                

                if return_time != "None":
                    return_time = datetime.strptime(return_time, "%H:%M").time()
                    
            except ValueError:
                messages.info(request, "Invalid date format, please use HH:MM")
                return render(request, "checkout.html" ,{"cart":cart})
            
         
            delivery_location = "None"
            delivery_time = "None"
            delivery_date = "None"
           
            pickup_location = pickup_location if pickup_location else "None"
          
            # license_image = license_image
            
            
            

            rent_duration = 0

            if delivery_type == "pickup" and pickup_date and return_date:
                rent_duration = (return_date - pickup_date).days
            else:
                messages.info(request, "please select dates to calculate total_price")
                return render(request, "checkout.html", {"cart":cart})
            
        
            total_price = 0

            
            if cart.car:
                total_price = cart.car.price_per_day * rent_duration
            elif cart.bike:
                total_price = cart.bike.price_per_day *rent_duration
            # elif cart.car and cart.bike:
            #     total_price = (cart.car.price_per_day + cart.bike.price_per_day) * rent_duration
           
            
            
            return redirect(f"/payment/{cart.id}/{total_price}/{delivery_type}/{delivery_location}/{delivery_date}/{delivery_time}/{pickup_date}/{pickup_time}/{pickup_location}/{return_date}/{return_time}/{filename}/")
        
       



        elif delivery_type=="delivery":
            print("king",delivery_type)
            if not delivery_date:
                messages.info(request, "Please select Delivery Date")
                return render(request, "checkout.html" , {"cart": cart})
            
            try:
                 
                delivery_date = datetime.strptime(delivery_date , '%Y-%m-%d' ).date()

                if delivery_date < today_date:
                    messages.info(request, "Delivery date cannot pe past to preset date")
                    return render(request, "checkout.html",{"cart":cart})
                
                if return_date:
                    return_date = datetime.strptime(return_date, "%Y-%m-%d").date()

                    if return_date <= delivery_date:
                        messages.info(request, "return date cannot be same as delivery date")
                        return render(request, "checkout.html",{"cart":cart})
                    
                
                delivery_date = delivery_date if delivery_date else "None"
                return_date = return_date if return_date else "None"

                


                
            except ValueError:
                messages.info(request, "Invalid date format, please date in YY-MM-DD")
                return render(request, "checkout.html",{"cart":cart})
            
            if not return_date:
                    messages.info(request, "Please select return date")
                    return render(request, "checkout.html" , {"cart":cart})
                
            

            if not return_time and delivery_time:
                messages.info(request, "Please select pickup and return time") 
                return render(request, "checkout.html", {"cart":cart})
            
            try:
                if delivery_time != "None":
                    delivery_time = datetime.strptime(delivery_time, "%H:%M").time()

                if return_time != "None":
                    return_time = datetime.strptime(return_time, "%H:%M").time()
                    
            except ValueError:
                messages.info(request, "Both Delivery time and Return time is required.")
                return render(request, "checkout.html" ,{"cart":cart})
            
            
            if not delivery_location or delivery_location.lower() == 'none':
                messages.error(request, "Delivery location is required when delivery is selected.")
                return render(request, "checkout.html" , {"cart": cart})
            
            pickup_location = "None"
            pickup_time = "None"
            pickup_date = "None"
        

            delivery_location = delivery_location if delivery_location else "None"
            # license_image = license_image


            rent_duration = 0

            if delivery_type == "delivery" and delivery_date and return_date:
                rent_duration = (return_date - delivery_date).days
            else:
                messages.info(request, "please select dates to calculate total_price")
                return render(request, "checkout.html",{"cart":cart})
            

            total_price = 0

           
            if cart.car:
                total_price = cart.car.price_per_day * rent_duration
            elif cart.bike:
                total_price = cart.bike.price_per_day *rent_duration
            elif cart.car and cart.bike:
                total_price = (cart.car.price_per_day + cart.bike.price_per_day) * rent_duration
            


            return redirect(f"/payment/{cart.id}/{total_price}/{delivery_type}/{delivery_location}/{delivery_date}/{delivery_time}/{pickup_date}/{pickup_time}/{pickup_location}/{return_date}/{return_time}/{filename}/")
            
     

    return render(request, "checkout.html" ,{"cart":cart , "pickup_location":pickup_location})



###############################################################################################################################################



def payment(request, cart_id, total_price, delivery_type, delivery_location, delivery_date,delivery_time, pickup_date, pickup_time,pickup_location, return_date, return_time,filename ):


    # delivery_date = None if delivery_date == "None" else datetime.strptime(delivery_date, "%Y-%m-%d").date() if delivery_date != "None" else None
    # delivery_time = None if delivery_time == "None" else datetime.strptime(delivery_time, "%H:%M:%S").time() if delivery_time != "None" else None
    # pickup_date = None if pickup_date == "None" else datetime.strptime(pickup_date, "%Y-%m-%d").date() if pickup_date != "None" else None
    # pickup_time = None if pickup_time == "None" else datetime.strptime(pickup_time, "%H:%M:%S").time() if pickup_time != "None" else None
    # pickup_location = None if pickup_location == "None" else pickup_location
    # return_date = None if return_date == "None" else datetime.strptime(return_date, "%Y-%m-%d").date() if return_date != "None" else None
    # return_time = None if return_time == "None" else datetime.strptime(return_time, "%H:%M:%S").time() if return_time != "None" else None
   
    
    if delivery_date == "None":
        delivery_date = None
    else:
        delivery_date = datetime.strptime(delivery_date, "%Y-%m-%d").date()

    if delivery_time == "None":
        delivery_time = None
    else:
        delivery_time = datetime.strptime(delivery_time, "%H:%M:%S").time()

    if delivery_location == "None":
        delivery_location = None
    else:
        delivery_location = delivery_location

    if pickup_date == "None":
        pickup_date = None
    else:
        pickup_date = datetime.strptime(pickup_date, "%Y-%m-%d").date()

    if pickup_time == "None":
        pickup_time = None
    else:
        pickup_time = datetime.strptime(pickup_time, "%H:%M:%S").time()

    if pickup_location == "None":
        pickup_location = None
    else:
        pickup_location = pickup_location

    if return_date == "None":
        return_date = None
    else:
        return_date = datetime.strptime(return_date, "%Y-%m-%d").date()

    if return_time == "None":
        return_time = None
    else:
        return_time = datetime.strptime(return_time, "%H:%M:%S").time()




    try:
        cart = Cart.objects.get(id=cart_id)
    except Cart.DoesNotExist:
        return redirect("/cars/")

    


    context =  {"cart":cart, 
                           "total_price":total_price, 
                           "delivery_type":delivery_type,
                           "delivery_location": delivery_location, 
                           "delivery_date":delivery_date,
                           "delivery_time":delivery_time,
                           "pickup_date":pickup_date,
                           "pickup_time":pickup_time,
                           "pickup_location":pickup_location,
                           "return_date":return_date,
                           "return_time":return_time, 
                        #    "license_image":license_image_url 
                            "filename":filename
                            
                           }
            
     
    
    return render(request, "payment.html" , context)   




###########################################################################################################################################



def payment_multiple(request, cart_ids, total_price, delivery_type, delivery_location, delivery_date,delivery_time, pickup_date, pickup_time,pickup_location, return_date, return_time,filename ):


   
    if delivery_date == "None":
        delivery_date = None
    else:
        delivery_date = datetime.strptime(delivery_date, "%Y-%m-%d").date()

    if delivery_time == "None":
        delivery_time = None
    else:
        delivery_time = datetime.strptime(delivery_time, "%H:%M:%S").time()

    if delivery_location == "None":
        delivery_location = None
    else:
        delivery_location = delivery_location

    if pickup_date == "None":
        pickup_date = None
    else:
        pickup_date = datetime.strptime(pickup_date, "%Y-%m-%d").date()

    if pickup_time == "None":
        pickup_time = None
    else:
        pickup_time = datetime.strptime(pickup_time, "%H:%M:%S").time()

    if pickup_location == "None":
        pickup_location = None
    else:
        pickup_location = pickup_location

    if return_date == "None":
        return_date = None
    else:
        return_date = datetime.strptime(return_date, "%Y-%m-%d").date()

    if return_time == "None":
        return_time = None
    else:
        return_time = datetime.strptime(return_time, "%H:%M:%S").time()

    

    


    try:
        cart_ids_list = [int(cart_id) for cart_id in cart_ids.split(",") ]
        print(f"Cart IDs List: {cart_ids_list}")
        carts = Cart.objects.filter(id__in=cart_ids_list)
        
        print(f"Carts: {carts}")
    except Cart.DoesNotExist:
        return redirect("/cars/")

    cart_ids_str = ",".join([str(cart_id) for cart_id in cart_ids_list])


    context =  {"carts":carts, 
                           "total_price":total_price, 
                           "delivery_type":delivery_type,
                           "delivery_location": delivery_location, 
                           "delivery_date":delivery_date,
                           "delivery_time":delivery_time,
                           "pickup_date":pickup_date,
                           "pickup_time":pickup_time,
                           "pickup_location":pickup_location,
                           "return_date":return_date,
                           "return_time":return_time, 
                           "filename":filename,
                           "cart_ids":cart_ids_str  
                         }
            
     
    
    return render(request, "payment_multiple.html" , context)  




#################################################################################################################################################


def success_single(request,cart_id, delivery_type, pickup_location, pickup_time, pickup_date, delivery_location, delivery_time, delivery_date, return_date, return_time, license_image, payment,payment_id):
  
    if license_image:
        # Reconstruct the full URL to the image stored in 'media/licenceFile'
        license_image = os.path.join(settings.MEDIA_URL, 'licenceFile', license_image)
    else:
        license_image = None
    
  

   
    if delivery_date == "None":
        delivery_date = None
    else:
        delivery_date = datetime.strptime(delivery_date, "%Y-%m-%d").date()


    if pickup_date == "None":
        pickup_date = None
    else:
        pickup_date = datetime.strptime(pickup_date, "%Y-%m-%d").date()

    
    return_date = datetime.strptime(return_date, "%Y-%m-%d").date()


    if delivery_time == "None":
        delivery_time = None
    else:
        delivery_time = datetime.strptime(delivery_time, "%H:%M").time()


    if pickup_time == "None":
        pickup_time = None
    else:
        pickup_time = datetime.strptime(pickup_time, "%H:%M").time()

    return_time = datetime.strptime(return_time, "%H:%M").time()


    if pickup_location == "None":
        pickup_location = None
    else:
        pickup_location = pickup_location

    if delivery_location == "None":
        delivery_location = None
    else:
        delivery_location = delivery_location



    customer_id = request.session.get('id')
   
    if not customer_id:
        return redirect("/accounts/login/")
    
    try:
        customer = Customer_register.objects.get(id=customer_id)
    except Customer_register.DoesNotExist:
        return redirect("/accounts/login/")
    

    try:
        cart = Cart.objects.get(id = cart_id)
    except Cart.DoesNotExist:
        return redirect("my_cart")
    

   
    if cart.car:
        
        final_detail = Rented_vehicles.objects.create(customer=customer, car=cart.car, delivery_type = delivery_type ,pickup_date = pickup_date, delivery_date = delivery_date, return_date = return_date, pickup_time = pickup_time, delivery_time = delivery_time, return_time = return_time, pickup_location = pickup_location, delivery_location = delivery_location, license_file = license_image, total_price = payment, payment_id = payment_id  )

        final_detail.save()
        
        return redirect('/my_rentals/')

    elif cart.bike:

        final_detail = Rented_vehicles.objects.create(customer=customer, bike=cart.bike, delivery_type = delivery_type ,pickup_date = pickup_date, delivery_date = delivery_date, return_date = return_date, pickup_time = pickup_time, delivery_time = delivery_time, return_time = return_time, pickup_location = pickup_location, delivery_location = delivery_location, license_file = license_image, total_price = payment, payment_id = payment_id  )

        final_detail.save()

        return redirect('/my_rentals/')
    
    return render(request,"payment.html")
    



#############################################################################################################################


def success_multiple(request,cart_ids, delivery_type, pickup_location, pickup_time, pickup_date, delivery_location, delivery_time, delivery_date, return_date, return_time, license_image, payment,payment_id):
    if license_image:
        license_image = os.path.join(settings.MEDIA_URL, "licenceFile", license_image)
    else:
        license_image = None

    
    
    if delivery_date == "None":
        delivery_date = None
    else:
        delivery_date = datetime.strptime(delivery_date, "%Y-%m-%d").date()


    if pickup_date == "None":
        pickup_date = None
    else:
        pickup_date = datetime.strptime(pickup_date, "%Y-%m-%d").date()

    
    return_date = datetime.strptime(return_date, "%Y-%m-%d").date()


    if delivery_time == "None":
        delivery_time = None
    else:
        delivery_time = datetime.strptime(delivery_time, "%H:%M").time()


    if pickup_time == "None":
        pickup_time = None
    else:
        pickup_time = datetime.strptime(pickup_time, "%H:%M").time()

    return_time = datetime.strptime(return_time, "%H:%M").time()


    if pickup_location == "None":
        pickup_location = None
    else:
        pickup_location = pickup_location

    if delivery_location == "None":
        delivery_location = None
    else:
        delivery_location = delivery_location

      
    cart_ids_list = [int(cart_id) for cart_id in cart_ids.split(",") ]
    # print(f"Cart IDs List: {cart_ids_list}")

    try:
        carts = Cart.objects.filter(id__in=cart_ids_list)
        print(f"Carts: {carts}")
    except Cart.DoesNotExist:
        return redirect("/cars/")
    


    customer_id = request.session.get('id')
   
    if not customer_id:
        return redirect("/accounts/login/")
    
    try:
        customer = Customer_register.objects.get(id=customer_id)
    except Customer_register.DoesNotExist:
        return redirect("/accounts/login/")
    

  
    for cart in carts:


        # If only a bike is selected, create a rental record for the bike
        if cart.bike:
            final_detail_bike = Rented_vehicles.objects.create(
                customer=customer,
                bike=cart.bike,  # Assign Bike instance
                delivery_type=delivery_type,
                pickup_date=pickup_date,
                delivery_date=delivery_date,
                return_date=return_date,
                pickup_time=pickup_time,
                delivery_time=delivery_time,
                return_time=return_time,
                pickup_location=pickup_location,
                delivery_location=delivery_location,
                license_file=license_image,
                total_price=payment,
                payment_id=payment_id
            )
            final_detail_bike.save()
            print(f"Bike saved: {cart.bike}")

        # If only a car is selected, create a rental record for the car
        elif cart.car:
            final_detail_car = Rented_vehicles.objects.create(
                customer=customer,
                car=cart.car,  # Assign Car instance
                delivery_type=delivery_type,
                pickup_date=pickup_date,
                delivery_date=delivery_date,
                return_date=return_date,
                pickup_time=pickup_time,
                delivery_time=delivery_time,
                return_time=return_time,
                pickup_location=pickup_location,
                delivery_location=delivery_location,
                license_file=license_image,
                total_price=payment,
                payment_id=payment_id
            )
            final_detail_car.save()
            print(f"Car saved: {cart.car}")

    return redirect('/my_rentals/')


    




def my_rentals(request):
    return render(request, "my_rentals.html")




##############################################################################################################################

def remove_from_cart(request, id):
    customer_id = request.session.get('id')

    if not customer_id:
        return redirect("/accounts/login/")  

 
    cart_items = Cart.objects.filter(id=id, customer=customer_id)

    if not cart_items.exists():
        messages.error(request, "Item not found in cart.")
        return redirect("/my_cart/") 


    cart_items[0].delete()

    if not Cart.objects.filter(customer=customer_id).exists():
        request.session['cart_empty'] = True  # Set flag if cart is empty
    else:
        request.session['cart_empty'] = False  # Reset flag if cart is not empty

        messages.info(request, "Item removed successfully.")

    return redirect("/my_cart/")


  


# def remove_from_rented_vehicle(request, id):
#     try:
#         # Try to get the rented vehicle with the given ID
#         rented_vehicle = Rented_vehicles.objects.get(id=id)
        
#         # Check if the logged-in user is the one who rented this vehicle (optional)
#         if rented_vehicle.customer != request.user:
#             messages.error(request, "You are not authorized to delete this rented vehicle.")
#             return redirect('/my_rentals/')
        
#         # If found, delete the rented vehicle
#         rented_vehicle.delete()
        
#         # Add a success message
#         messages.success(request, "Rented vehicle removed successfully.")
#     except Rented_vehicles.DoesNotExist:
#         # If the rented vehicle doesn't exist, show an error message
#         messages.error(request, "Rented vehicle not found.")
    
#     # Redirect to the my_cart page or any other page you'd prefer
#     return redirect('/my_cart/')  # You can redirect to another page if needed
        












