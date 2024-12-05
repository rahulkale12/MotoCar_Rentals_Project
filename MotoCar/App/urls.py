from django.urls import path, re_path
from .import views



urlpatterns = [
    path('', views.index , name='index'),
    path('cars/',views.cars, name='cars'),
    path('bikes/',views.bikes, name='bikes'),
    path('add_to_cart/car/<int:car_id>/', views.add_car_to_cart, name='add_car_to_cart'),
    path('add_to_cart/bike/<int:bike_id>/', views.add_bike_to_cart, name='add_bike_to_cart'),
    path('my_cart/',views.my_cart, name="my_cart"),
    path('remove_from_cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/<int:id>/', views.checkout, name='checkout'),
    path('checkouts/', views.checkouts, name='checkouts'),
    path('validate_form_multiple/',views.validate_form_multiple, name= "validate_form_mutliple"),
    path('validate_form_single/<int:id>/',views.validate_form_single, name= "validate_form_single"),
    # path('payment/<int:cart>/<int:total_price>/<str:delivery_type>/<str:delivery_location>/<int:delivery_date>/<int:delivery_time>/<int:pickup_date>/<int:pickup_time>/<str:pickup_location>/<int:return_date>/<int:return_time>/',views.payment, name="payment"),
    path('payment/<int:cart_id>/<int:total_price>/<str:delivery_type>/<str:delivery_location>/<str:delivery_date>/<str:delivery_time>/<str:pickup_date>/<str:pickup_time>/<str:pickup_location>/<str:return_date>/<str:return_time>/', views.payment, name='payment'),
    
    path('payment_multiple/<str:cart_ids>/<int:total_price>/<str:delivery_type>/<str:delivery_location>/<str:delivery_date>/<str:delivery_time>/<str:pickup_date>/<str:pickup_time>/<str:pickup_location>/<str:return_date>/<str:return_time>/', views.payment_multiple, name='payment_multiple'),
    
    

    path('success_single/<int:cart_id>/<str:delivery_type>/<str:pickup_location>/<str:pickup_time>/<str:pickup_date>/<str:delivery_location>/<str:delivery_time>/<str:delivery_date>/<str:return_date>/<str:return_time>/<int:payment>/<str:payment_id>/', views.success_single, name='success_single'),
    path('success_multiple/<str:cart_ids>/<str:delivery_type>/<str:pickup_location>/<str:pickup_time>/<str:pickup_date>/<str:delivery_location>/<str:delivery_time>/<str:delivery_date>/<str:return_date>/<str:return_time>/<int:payment>/<str:payment_id>/', views.success_multiple, name='success_multiple'),
    # re_path(r'^success_single/(?P<cart_id>\d+)/(?P<delivery_type>\w+)/(?P<pickup_location>[^/]+)/(?P<pickup_time>[^/]+)/(?P<pickup_date>[^/]+)/(?P<delivery_location>[^/]+)/(?P<delivery_time>[^/]+)/(?P<delivery_date>[^/]+)/(?P<return_date>[^/]+)/(?P<return_time>[^/]+)/(?P<license_image>[^/]+)/(?P<payment>\d+)/(?P<payment_id>[^/]+)/$', views.success_single, name='success_single'),

    path("my_rentals/",views.my_rentals, name="my_rentals"),

    path('contact/', views.contact, name="contact"),


]