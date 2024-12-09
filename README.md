# MotoCar Rentals 🚗🏍️

Welcome to **MotoCar Rentals**, the finest website in India that offers car and bike rental services in one place! This Django-powered platform provides users with a seamless experience to rent vehicles based on their preferences, budget, and location.

## Features 🌟

- **Rent Cars and Bikes**: Choose vehicles by price, rental duration (hour/day), fuel type, and company.
- **Search by Location**: Use state, city, or district filters to find nearby rentals.
- **Dynamic Pricing**: Rentals available at affordable and adjustable pricing.
- **Secure Payments**: Integrated payment gateway.
- **User Notifications**:
  - Email on registration and bookings.
- **Delivery and Pickup Options**:
  - Delivery: Additional fields for location.
  - Pickup: Auto-populated options based on selected vehicle's city.
- **Driving License Upload**: Users can upload their license once per session to rent a vehicle.

## Tech Stack 🛠️

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL

## How It Works 🔧

1. **Browse Vehicles**: Explore cars and bikes listed with images, specifications, and pricing.
2. **Filter and Select**: Apply filters for vehicle type, location, and more.
3. **Add to Cart**: Rent multiple vehicles in one session.
4. **Upload Driving License**: Ensure eligibility for rentals.
5. **Checkout**: Fill in details for pickup/delivery and proceed to secure payment.
6. **Confirmation**: Receive booking confirmation via email.

## Setup Instructions 🖥️

1. Clone the repository:
   git clone https://github.com/your-username/motocar-rentals.git
2. Navigate to the project directory:
  cd motocar-rentals
3. Create and activate a virtual environment:
   python -m venv myenv
  source myenv/bin/activate
4. Install dependencies:
   pip install -r requirements.txt
5. Apply migrations:
   python manage.py migrate
6. Start the development server:
   python manage.py runserver
