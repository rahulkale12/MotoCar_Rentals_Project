from django.urls import path
from .import views

urlpatterns = [
    path('register/',views.register,name="register"),
    path('login/',views.login,name="login"),
    path('customer_profile/', views.customer_profile, name='customer_profile'),
    path('customer_logout/',views.customer_logout,name="customer_logout"),
    path('profile_picture/<int:id>/',views.profile_picture,name="profile_picture"),
    path('delete_image/<int:id>/',views.delete_image,name="delete_image"),
    path('edit_customer/<int:id>/',views.edit_customer,name="edit_customer"),
    path('update_customer/<int:id>/',views.update_customer,name='update_customer'),
    path('delete_customer/<int:id>/',views.delete_customer,name='delete_customer'),
    
]
