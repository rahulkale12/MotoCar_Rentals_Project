from django.shortcuts import render,redirect
from accounts.models import Customer_register, Profile_pic
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from django.views.decorators.cache import never_cache
from django.core.validators import validate_email

# Create your views here.
def register(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        address = request.POST['address']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email format. Please enter a valid email.")
            return render(request, "customer_register.html")
        

        if password == confirm_password :
            if Customer_register.objects.filter(email=email).exists():
                messages.info(request, "Email Exists, Please try with new email")
                return redirect('/accounts/register/')
            elif Customer_register.objects.filter(mobile = mobile).exists():
                messages.info(request, "Mobile Number Exists, Please try with new number")
                return redirect('/accounts/register/')
            else:
                password = make_password(password)
                new_customer = Customer_register.objects.create(name=name, email=email, mobile=mobile, city=city, state=state, pincode=pincode, address=address,password=password)
                new_customer.save()
                return redirect('/accounts/login/')
        else:
            messages.info(request, "Password did'nt match")
            return redirect('/accounts/register/')

    return render(request,'customer_register.html')



def login(request):
    if request.method == "POST":
        mobile = request.POST['mobile']
        password = request.POST['password']

        try:
            customer = Customer_register.objects.get(mobile=mobile)
            if customer.mobile == int(mobile) and check_password(password, customer.password):
                request.session['id'] = customer.id
                return redirect('/accounts/customer_profile/')
            else: 
                messages.info(request, "Invalid Credentials")
                return redirect('/accounts/login/')
        except ObjectDoesNotExist:
            messages.info(request, "Mobile Does Not Exist, Please register.")
            return redirect('/accounts/login/')
        
    return render(request, 'customer_login.html')


def profile_picture(request,id):
    if request.method == "POST":
        user_pic = request.FILES.get('profile_pic')
        user_id = request.session.get('id')
        try:
            user = Customer_register.objects.get(id=user_id)
            if Profile_pic.objects.filter(customer = user).exists():
                image = Profile_pic.objects.get(customer = user)
                image.profile_image = user_pic
                image.save()
                return redirect('/accounts/customer_profile/')
            else:
                new_create = Profile_pic.objects.create(customer = user,profile_image = user_pic)
                new_create.save()
                return redirect('/accounts/customer_profile/')
        except Customer_register.DoesNotExist:
            return redirect('/accounts/customer_profile/')
    return render(request, "customer_profile.html")

@never_cache
def customer_profile(request):
    user_id= request.session.get('id')
    if not user_id:                               #i faced an error Customer.Doesnotexist so keeping in try except to test the templates and views
        return redirect('/accounts/login/')
    try:
        user = Customer_register.objects.get(id = user_id)

    except Customer_register.DoesNotExist:
        return redirect('/accounts/login/')
    
    try:
        profile_pic = Profile_pic.objects.get(customer = user)
        return render(request, "customer_profile.html", {'user':user,'profile_pic':profile_pic})
    except Profile_pic.DoesNotExist:
        return render(request, "customer_profile.html", {'user':user})
    
def delete_image(request,id):
    profile_pic = Profile_pic.objects.get(id=id)
    profile_pic.delete()
    return redirect('/accounts/customer_profile/')



def update_customer(request,id):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        address = request.POST['address']
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email format. Please enter a valid email.")
            return render(request, "edit_customer.html")
        
        get_customer = Customer_register.objects.get(id=id)
        get_customer.name = name
        get_customer.email = email
        get_customer.mobile = mobile
        get_customer.city = city
        get_customer.state = state
        get_customer.pincode = pincode
        get_customer.address = address
        get_customer.save()
        return redirect('/accounts/customer_profile/')
    return render(request,"edit_customer/id/")


def edit_customer(request, id):
    edit_data = Customer_register.objects.get(id=id)
    return render(request ,"customer_edit.html", {'edit_data':edit_data})

def delete_customer(request,id):
    user = Customer_register.objects.get(id=id)
    user.delete()
    return redirect('/accounts/login/')


def customer_logout(request):
    customer = request.session.get('id')
    request.session.flush()
    return redirect('/accounts/login/')
