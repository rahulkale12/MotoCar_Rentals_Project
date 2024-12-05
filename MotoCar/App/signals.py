from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Rented_vehicles
from django.conf import settings

@receiver(post_save, sender=Rented_vehicles)
def send_success_mail(sender, instance, created, **kwargs):
    if created:
        customer = instance.customer
        vehicle_type = "Car" if instance.car else "Bike"
        vehicle_name = instance.car.name if instance.car else instance.bike.name
        delivery_type = instance.delivery_type
        pickup_date = instance.pickup_date
        pickup_location = instance.pickup_location
        pickup_time = instance.pickup_time
        delivery_date = instance.delivery_date
        delivery_location = instance.delivery_location
        delivery_time = instance.delivery_time
        return_date = instance.return_date
        return_time = instance.return_time
        total_price = instance.total_price

        # Dynamically generate rental details based on delivery type
        if delivery_type.lower() == "delivery":
            rental_details = (
                f"Delivery Location: {delivery_location}\n"
                f"Delivery Date: {delivery_date}\n"
                f"Delivery Time: {delivery_time}\n"
            )
        else:  # Pickup
            rental_details = (
                f"Pickup Location: {pickup_location}\n"
                f"Pickup Date: {pickup_date}\n"
                f"Pickup Time: {pickup_time}\n"
            )

        # Email subject and message
        subject = "Thank You For Renting with MotoCar Rentals"
        message = (
            f"Dear {customer.name},\n\n"
            f"Thank you for renting a {vehicle_type} with us!\n\n"
            f"Here are your rental details:\n"
            f"Vehicle: {vehicle_name}\n"
            f"Delivery Type: {delivery_type.capitalize()}\n"  # Capitalized for readability
            f"{rental_details}"  # Add dynamically generated details
            f"Return Date: {return_date}\n"
            f"Return Time: {return_time}\n"
            f"Total Price: ₹{total_price}\n\n"
            f"We hope you have a great experience!\n"
            f"Happy Renting!!!!\n\n"
            f"Best Regards,\n"
            f"MotoCar Rentals Team"
        )

        # Send email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # Sender's email
            [customer.email],  # Recipient's email
        )
