from django.shortcuts import render,redirect
from App.models import Car, Bike,State,City,Cart, Rented_vehicles, Contact_US
from accounts.models import Customer_register
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.contrib import messages
from datetime import date
from django.utils import timezone
from django.conf import settings
import os
from django.core.files.storage import FileSystemStorage
from django.views.decorators.cache import never_cache
from datetime import time as dt_time


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



@never_cache
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







@never_cache
def checkout(request,id):
    customer_id = request.session.get('id')
    # print(f"Customer ID in session in checkout view: {customer_id}")
    if not customer_id:
        return redirect('/accounts/login/')
    try:
         customer = Customer_register.objects.get(id=customer_id)
    except Customer_register.DoesNotExist:
        return redirect('/accounts/register/')
    
    try:

        cart = Cart.objects.get(id=id)
    except Cart.DoesNotExist:
        return redirect('/my_cart/')
    
    

    if cart.car:
    
            pickup_location = cart.car.city.name if cart.car.city else ""
            return render(request, "checkout.html",{"cart":cart, "pickup_location":pickup_location})
    
    elif cart.bike:
            pickup_location = cart.bike.city.name if cart.bike.city else ""
            return render(request, "checkout.html",{"cart":cart, "pickup_location":pickup_location})   
      
            
    return render(request, "checkout.html",{"cart":cart, "pickup_location":pickup_location})





    



##############################################################################################################################################


def checkouts(request):
    customer_id = request.session.get('id')
    # print(f"customer id retrieved in checkouts: {customer_id}")
    if not customer_id:
        return redirect('/accounts/login/')
    try:

        customer = Customer_register.objects.get(id=customer_id)
    except Customer_register.DoesNotExist:
        return redirect('/accounts/register/')
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

        # if license_image:
        #     # Save the image to the 'licenceFile' directory inside the 'media' folder
        #     fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'licenceFile'))
        #     filename = fs.save(license_image.name, license_image)
        #     encoded_filename = quote(filename)
        #     # license_image_url = fs.url(filename)  # Get the URL of the uploaded image
        # else:
        #     # license_image_url = None
        #     filename = None


        if license_image:
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'licenceFile'))
            filename = fs.save(license_image.name, license_image)
            request.session['license_image'] = filename
            # print(f"licnse image retrievd in validate_multiple {request.session.get('license_image')}")
            
        else:
            messages.info(request, "License file is Mandatory")
            # return render(request,'checkouts.html',{'carts':carts})
            return redirect('/checkouts/')
       


        
        # Pickup code


        if delivery_type == "pickup":
            # print("hellorahul",delivery_type)
            if not pickup_date:
                messages.info(request, "Please select Pickup Date")
                # return render(request, "checkouts.html", {"carts": carts})
                return redirect('/checkouts/')
            
            try:
                pickup_date = datetime.strptime(pickup_date , '%Y-%m-%d' ).date()

                if pickup_date < today_date:
                        messages.info(request, "Pickup date cannot be in past.")
                        # return render(request, "checkouts.html" ,{"carts":carts})
                        return redirect('/checkouts/')
                
                if return_date:
                    return_date = datetime.strptime(return_date, "%Y-%m-%d").date()

                    if return_date <= pickup_date:
                        messages.info(request, "return date must be after pickup date")
                        # return render(request, "checkouts.html",{"carts":carts})
                        return redirect('/checkouts/')
                    
                
                pickup_date = pickup_date
                return_date = return_date    

                delivery_date= None 
   
            except ValueError:
                messages.info(request, "Invalid date format, please date in YY-MM-DD")
                # return render(request, "checkouts.html",{"carts":carts})
                return redirect('/checkouts/')
            
            if not return_date:
                    messages.info(request, "Please select return date")
                    # return render(request, "checkouts.html" , {"carts":carts})
                    return redirect('/checkouts/')
                

            if not return_time and pickup_time:
                messages.info(request, "Please select pickup and return time")
                # return render(request, "checkouts.html" ,{"carts":carts})
                return redirect('/checkouts/')
            
            try:
                if pickup_time != "None":
                    pickup_time = datetime.strptime(pickup_time, "%H:%M").time()
            

                if return_time != "None":
                    return_time = datetime.strptime(return_time, "%H:%M").time()
               
                    
            except ValueError:
                messages.info(request, "Invalid date format, please use HH:MM")
                # return render(request, "checkouts.html" ,{"carts":carts})
                return redirect('/checkouts/')
            
            delivery_location = "None"
            delivery_time = "None"
            delivery_date = "None"


            pickup_location = pickup_location if pickup_location else "None"
            # license_image = license_image

            
            rent_duration = 0

            if delivery_type == "pickup" and pickup_date and return_date:
                rent_duration += (return_date - pickup_date).days
            else:
                messages.info(request, "please select dates to calculate total_price")
                # return render(request, "checkout.html", {"carts":carts})
                return redirect('/checkouts/')
            
        
            total_price = 0

            for cart in carts:
                if cart.car:
                    total_price  += cart.car.price_per_day * rent_duration 
                elif cart.bike:
                    total_price  += cart.bike.price_per_day * rent_duration
                elif cart.car and cart.bike:
                    total_price  += (cart.car.price_per_day + cart.bike.price_per_day) * rent_duration
            


            cart_ids = ','.join([str(cart.id) for cart in carts])

            return redirect(f"/payment_multiple/{cart_ids}/{total_price}/{delivery_type}/{delivery_location}/{delivery_date}/{delivery_time}/{pickup_date}/{pickup_time}/{pickup_location}/{return_date}/{return_time}/")
                                      
       


        elif delivery_type=="delivery":
            # print("king",delivery_type)
            if not delivery_date:
                messages.info(request, "Please select Delivery Date")
                # return render(request, "checkouts.html" , {"carts": carts})
                return redirect('/checkouts/')
            
            try:
                 
                delivery_date = datetime.strptime(delivery_date , '%Y-%m-%d' ).date()

                if delivery_date < today_date:
                    messages.info(request, "Delivery date cannot pe past to preset date")
                    # return render(request, "checkouts.html",{"carts":carts})
                    return redirect('/checkouts/')
                    
                    
                
                if return_date:
                    return_date = datetime.strptime(return_date, "%Y-%m-%d").date()

                    if return_date <= delivery_date:
                        messages.info(request, "return date cannot be same as delivery date")
                        # return render(request, "checkouts.html",{"carts":carts})
                        return redirect('/checkouts/')
                    
                
                delivery_date = delivery_date if delivery_date else "None"
                return_date = return_date   

                
            except ValueError:
                messages.info(request, "Invalid date format, please date in YY-MM-DD")
                # return render(request, "checkouts.html",{"carts":carts})
                return redirect('/checkouts/')
            
            if not return_date:
                    messages.info(request, "Please select return date")
                    # return render(request, "checkouts.html" , {"carts":carts})
                    return redirect('/checkouts/')
                
            

            if not return_time and delivery_time:
                messages.info(request, "Please select pickup and return time") 
                # return render(request, "checkouts.html", {"carts":carts})
                return redirect('/checkouts/')
            
            try:
                if delivery_time != "None":
                    delivery_time = datetime.strptime(delivery_time, "%H:%M").time()

                if return_time != "None":
                    return_time = datetime.strptime(return_time, "%H:%M").time()
                    
            except ValueError:
                messages.info(request, "Invalid date format, please use HH:MM")
                # return render(request, "checkouts.html" ,{"carts":carts})
                return redirect('/checkouts/')
            
            
            if not delivery_location or delivery_location.lower() == 'none':
                messages.error(request, "Delivery location is required when delivery is selected.")
                # return render(request, "checkouts.html" , {"carts": carts})
                return redirect('/checkouts/')
            
           
            pickup_location = "None"
            pickup_time = "None"
            pickup_date = "None"


            delivery_location = delivery_location if delivery_location else "None"
            # license_image = license_image


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

            return redirect(f"/payment_multiple/{cart_ids}/{total_price}/{delivery_type}/{delivery_location}/{delivery_date}/{delivery_time}/{pickup_date}/{pickup_time}/{pickup_location}/{return_date}/{return_time}/")
     

    return render(request, "checkouts.html" ,{"carts":carts})





##########################################################################################################################################################



def validate_form_single(request,id):
    
    customer_id = request.session.get("id")
    print(f"Customer ID in session in validate_form_single view view: {customer_id}")
    

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
        max_allowed_time = dt_time(23,0)

        
      
        # if license_image:
        #     # Save the image to the 'licenceFile' directory inside the 'media' folder
        #     fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'licenceFile'))
        #     filename = fs.save(license_image.name, license_image)
        #     # license_image_url = fs.url(filename)  # Get the URL of the uploaded image
        # else:
        #     # license_image_url = None
        #     filename = None

         # Save the license image and store in session
        if license_image:
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'licenceFile'))
            filename = fs.save(license_image.name, license_image)
            request.session['license_image'] = filename
           
        else:
            messages.info(request, "License file is Mandatory")
            # return render(request,'checkout.html',{'cart':cart})
            return redirect(f'/checkout/{cart.id}/')

        
         # Pickup code

         


        if delivery_type == "pickup":
            if not pickup_date:
                messages.info(request, "Please select Pickup Date")
                # return render(request, "checkout.html", {"cart": cart})
                return redirect(f'/checkout/{cart.id}/')
            
            try:
                pickup_date = datetime.strptime(pickup_date , '%Y-%m-%d' ).date()

                if pickup_date < today_date:
                        messages.info(request, "Pickup date cannot be in past.")
                        # return render(request, "checkout.html" ,{"cart":cart})
                        return redirect(f'/checkout/{cart.id}/')
                
                if return_date:
                    return_date = datetime.strptime(return_date, "%Y-%m-%d").date()

                    if (return_date <= pickup_date):
                        messages.info(request, "return date must be after pickup date")
                        # return render(request, "checkout.html",{"cart":cart})
                        return redirect(f'/checkout/{cart.id}/')
                    
                
                pickup_date = pickup_date
                return_date = return_date    

                delivery_date= None 
   
            except ValueError:
                messages.info(request, "Invalid date format, please date in YY-MM-DD")
                # return render(request, "checkout.html",{"cart":cart})
                return redirect(f'/checkout/{cart.id}/')
            
            if not return_date:
                    messages.info(request, "Please select return date")
                    # return render(request, "checkout.html" , {"cart":cart})
                    return redirect(f'/checkout/{cart.id}/')
            
                
            

            if not return_time and pickup_time:
                messages.info(request, "Please select pickup and return time")
                # return render(request, "checkout.html" ,{"cart":cart})
                return redirect(f'/checkout/{cart.id}/')
            
            try:
                if pickup_time != "None":
                    pickup_time = datetime.strptime(pickup_time, "%H:%M").time()
                if pickup_time>max_allowed_time:                                                 #made changes just now
                    messages.info(request, "Pickup time should be on or before 11:00 PM.")
                    return redirect(f'/checkout/{cart.id}/')
                

                if return_time != "None":
                    return_time = datetime.strptime(return_time, "%H:%M").time()
                if return_time > max_allowed_time:                                                    #made changes just now
                    messages.info(request, "Return time should be on or before 11:00 PM.")
                    return redirect(f'/checkout/{cart.id}/')
                    
            except ValueError:
                messages.info(request, "Invalid date format, please use HH:MM")
                # return render(request, "checkout.html" ,{"cart":cart})
                return redirect(f'/checkout/{cart.id}/')
            
         
            delivery_location = "None"
            delivery_time = "None"
            delivery_date = "None"
           
            pickup_location = pickup_location if pickup_location else "None"



            # rent_duration = 0

            # if delivery_type == "pickup" and pickup_date and return_date:
            #     rent_duration = (return_date - pickup_date).days
            # else:
            #     messages.info(request, "please select dates to calculate total_price")
            #     # return render(request, "checkout.html", {"cart":cart})
            #     return redirect(f'/checkout/{cart.id}/')
            if delivery_type == "pickup" and pickup_date and return_date:
                rent_duration = (return_date - pickup_date).days                                     #changes made just now
            if rent_duration > 7:
                messages.info(request, "You can only rent the vehicle for up to 7 days.")
                return redirect(f'/checkout/{cart.id}/')

        
            total_price = 0

            
            if cart.car:
                total_price += cart.car.price_per_day * rent_duration
            elif cart.bike:
                total_price += cart.bike.price_per_day *rent_duration
            # elif cart.car and cart.bike:
            #     total_price = (cart.car.price_per_day + cart.bike.price_per_day) * rent_duration
            # total_price = round(total_price, 2)
            
            
            return redirect(f"/payment/{cart.id}/{total_price}/{delivery_type}/{delivery_location}/{delivery_date}/{delivery_time}/{pickup_date}/{pickup_time}/{pickup_location}/{return_date}/{return_time}/")
        
       

########## delievery type code  #########################

        elif delivery_type=="delivery":
            if not delivery_date:
                messages.info(request, "Please select Delivery Date")
                # return render(request, "checkout.html" , {"cart": cart})
                return redirect(f'/checkout/{cart.id}/')
            
            try:
                 
                delivery_date = datetime.strptime(delivery_date , '%Y-%m-%d' ).date()

                if delivery_date < today_date:
                    messages.info(request, "Delivery date cannot pe past to preset date")
                    # return render(request, "checkout.html",{"cart":cart})
                    return redirect(f'/checkout/{cart.id}/')
                
                if return_date:
                    return_date = datetime.strptime(return_date, "%Y-%m-%d").date()

                    if return_date <= delivery_date:
                        messages.info(request, "return date cannot be same as delivery date")
                        # return render(request, "checkout.html",{"cart":cart})
                        return redirect(f'/checkout/{cart.id}/')
                    
                
                delivery_date = delivery_date if delivery_date else "None"
                return_date = return_date if return_date else "None"

                

            except ValueError:
                messages.info(request, "Invalid date format, please date in YY-MM-DD")
                # return render(request, "checkout.html",{"cart":cart})
                return redirect(f'/checkout/{cart.id}/')
            
            if not return_date:
                    messages.info(request, "Please select return date")
                    # return render(request, "checkout.html" , {"cart":cart})
                    return redirect(f'/checkout/{cart.id}/')
                
            

            if not return_time and delivery_time:
                messages.info(request, "Please select pickup and return time") 
                # return render(request, "checkout.html", {"cart":cart})
                return redirect(f'/checkout/{cart.id}/')
            
            try:
                if delivery_time != "None":
                    delivery_time = datetime.strptime(delivery_time, "%H:%M").time()
                if delivery_time>max_allowed_time:                                                    #changes made just now
                    messages.info(request, "Delivery time should be on or before 11:00 PM.")
                    return redirect(f'/checkout/{cart.id}/')

                if return_time != "None":
                    return_time = datetime.strptime(return_time, "%H:%M").time()
                if return_time > max_allowed_time:                                                       #changes made just now
                    messages.info(request, "Return time should be on or before 11:00 PM.")
                    return redirect(f'/checkout/{cart.id}/')
                    
            except ValueError:
                messages.info(request, "Both Delivery time and Return time is required.")
                # return render(request, "checkout.html" ,{"cart":cart})
                return redirect(f'/checkout/{cart.id}/')
            
            
            if not delivery_location or delivery_location.lower() == 'none':
                messages.error(request, "Delivery location is required when delivery is selected.")
                # return render(request, "checkout.html" , {"cart": cart})
                return redirect(f'/checkout/{cart.id}/')
            
            pickup_location = "None"
            pickup_time = "None"
            pickup_date = "None"
        

            delivery_location = delivery_location if delivery_location else "None"
            # license_image = license_image


            # rent_duration = 0

            # if delivery_type == "delivery" and delivery_date and return_date:
            #     rent_duration = (return_date - delivery_date).days
            # else:
            #     messages.info(request, "please select dates to calculate total_price")
            #     # return render(request, "checkout.html",{"cart":cart})
            #     return redirect(f'/checkout/{cart.id}/')
            
            if delivery_type == "delivery" and delivery_date and return_date:         #changes made just now
                rent_duration = (return_date - delivery_date).days
            if rent_duration > 7:
                messages.info(request, "You can only rent the vehicle for up to 7 days.")
                return redirect(f'/checkout/{cart.id}/')

            total_price = 0

           
            if cart.car:
                total_price += cart.car.price_per_day * rent_duration
            elif cart.bike:
                total_price += cart.bike.price_per_day *rent_duration
            elif cart.car and cart.bike:
                total_price = (cart.car.price_per_day + cart.bike.price_per_day) * rent_duration
            # total_price = round(total_price, 2)
            


            return redirect(f"/payment/{cart.id}/{total_price}/{delivery_type}/{delivery_location}/{delivery_date}/{delivery_time}/{pickup_date}/{pickup_time}/{pickup_location}/{return_date}/{return_time}/")
            
     

    return render(request, "checkout.html" ,{"cart":cart , "pickup_location":pickup_location})



###############################################################################################################################################



def payment(request, cart_id, total_price, delivery_type, delivery_location, delivery_date,delivery_time, pickup_date, pickup_time,pickup_location, return_date, return_time):

    

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

    customer_id = request.session.get('id')
    print(f"user id Retrieved from Session in payemnt view: {customer_id}")
  
    license_image = request.session.get('license_image')
    customer_id = request.session.get('id')

    
    
  
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
                            # "filename":filename,
                            'customer_id' :customer_id,
                            'license_image':license_image,
                            
                            
                           }
            
     
    
    return render(request, "payment.html" , context)   




###########################################################################################################################################


def payment_multiple(request, cart_ids, total_price, delivery_type, delivery_location, delivery_date,delivery_time, pickup_date, pickup_time,pickup_location, return_date, return_time ):

    # print("Session Data:", request.session.items())     #to debug whether getting session and item or not.

   
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


    customer_id = request.session.get('id')
    print(f"customer id retirved in payemnt_multiple: {customer_id}")
    license_image = request.session.get('license_image')
    print(f"license_image retrived in payemnt_multiple :{license_image}")

    


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
                           "license_image":license_image,
                           "cart_ids":cart_ids_str  
                         }
            
     
    
    return render(request, "payment_multiple.html" , context)  




#################################################################################################################################################
from urllib.parse import unquote

def success_single(request,cart_id,customer_id, license_image,delivery_type, pickup_location, pickup_time, pickup_date, delivery_location, delivery_time, delivery_date, return_date, return_time, payment,payment_id):
  

    if not request.session.get('id'):
        request.session['id'] = customer_id
    new_id = request.session.get('id')
    
    # print(f"Session Data: {request.session.items()}")
    license_image = unquote(license_image)
   
    # if not request.session.get('license_image'):
    #     request.session['license_image'] = license_image
    # new_license = request.session.get('license_image')

        
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


    # customer_id = request.session.get('id')    
   
    # if not customer_id:
    #     print("Session expired or customer_id is missing.")
    #     return redirect("/accounts/login/")

   
    
    try:
        # customer = Customer_register.objects.get(id=customer_id)
        customer = Customer_register.objects.get(id= new_id)
    except Customer_register.DoesNotExist:
        # print(f"Customer with ID {customer_id} does not exist.")
        return redirect("/accounts/login/")
    

    try:
        cart = Cart.objects.get(id = cart_id)
        print(f"Cart success view: {cart}")
    except Cart.DoesNotExist:
        return redirect("my_cart")
    

   
    if cart.car:
        
        final_detail = Rented_vehicles.objects.create(customer=customer, 
                                                      car=cart.car, 
                                                      delivery_type = delivery_type ,
                                                      pickup_date = pickup_date, 
                                                      delivery_date = delivery_date, 
                                                      return_date = return_date, 
                                                      pickup_time = pickup_time, 
                                                      delivery_time = delivery_time, 
                                                      return_time = return_time, 
                                                      pickup_location = pickup_location, 
                                                      delivery_location = delivery_location, 
                                                      license_file = license_image, 
                                                      total_price = payment, 
                                                      payment_id = payment_id  )

        final_detail.save()
        cart.delete()
        print(f"Cart ID bike: {cart_id} deleted.")
        
        return redirect('/my_rentals/')

    elif cart.bike:

        final_detail = Rented_vehicles.objects.create(customer=customer, 
                                                      bike=cart.bike, 
                                                      delivery_type = delivery_type ,
                                                      pickup_date = pickup_date, 
                                                      delivery_date = delivery_date, 
                                                      return_date = return_date, 
                                                      pickup_time = pickup_time, 
                                                      delivery_time = delivery_time, 
                                                      return_time = return_time, 
                                                      pickup_location = pickup_location, 
                                                      delivery_location = delivery_location, 
                                                      license_file = license_image, 
                                                      total_price = payment, 
                                                      payment_id = payment_id  )

        final_detail.save()
        cart.delete()
        print(f"Cart ID car: {cart_id} deleted.")

        return redirect('/my_rentals/')
    
    
    return render(request,"payment.html")
    



#############################################################################################################################
# from urllib.parse import unquote

def success_multiple(request,cart_ids,customer_id,license_image,delivery_type, pickup_location, pickup_time, pickup_date, delivery_location, delivery_time, delivery_date, return_date, return_time, payment,payment_id):

    print("Session Data:", request.session.items())


    # license_image = unquote(license_image)
    # print("Decoded License Image Path:", license_image)
    # license_image = request.session.get('license_image', None)

    if not request.session.get('license_image'):
        request.session['license_image'] = license_image
    new_license = request.session.get('license_image')

    if new_license:
        # Reconstruct the full URL to the image stored in 'media/licenceFile'
        license_image = os.path.join(settings.MEDIA_URL, 'licenceFile', new_license)
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

    ### converting cart_id into int data type and many ids into list so we can iterate over.
    cart_ids_list = [int(cart_id) for cart_id in cart_ids.split(",") ]
    

    try:
        carts = Cart.objects.filter(id__in=cart_ids_list)
        print(f"Carts: {carts}")
    except Cart.DoesNotExist:
        return redirect("/cars/")
    
    if not request.session.get('id'):  # If session ID is missing
        request.session['id'] = customer_id

    new_id = request.session.get('id')

    # customer_id = request.session.get('id')
    # print(f"customer id retrieved in success_multiple {customer_id}")
   
    # if not customer_id:
    #     return redirect("/accounts/login/")
    
    try:
        customer = Customer_register.objects.get(id=new_id)
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

        cart.delete()

    return redirect('/my_rentals/')


### My rentals view #############################################################################################################  

@never_cache
def my_rentals(request):
    cutsomer_id = request.session.get('id')
    if not cutsomer_id:
        return redirect('/accounts/login/')
    try:
        customer = Customer_register.objects.get(id = cutsomer_id)
    except Customer_register.DoesNotExist:
        return redirect('/accounts/register/')
    
    rentals = Rented_vehicles.objects.filter(customer=customer)
    return render(request, "my_rentals.html",{'rentals':rentals})




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





#####Contact View##############################################################################################

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        try:
            validate_email(email)
        except ValidationError:
            messages.info(request, "Please Enter valid Email")
            return redirect('/contact/')

        try:
            Contact_US.objects.create(name=name, email=email, subject=subject, message=message)
            messages.info(request, "Thank you for Contacting MotoCar Rentals, we have recieved your message, will shortly get back to you, till than Happy Renting!!")
            return redirect('/contact/')
        except:
            messages.info(request, "Cannot send message , Please try again after some time.")
            return redirect('/contact/')
           
    return render(request, "contact.html")















