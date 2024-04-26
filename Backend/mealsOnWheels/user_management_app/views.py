from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import User, Customer, Owner, Courier
from restaurant_management_app.models import Restaurant

import random

@require_POST
def register_user(request):
    # Extract registration data from the POST request
    email = request.POST.get('email')
    password = request.POST.get('password')
    user_type = request.POST.get('user_type')  # user_type (e.g., 'customer', 'owner', 'courier')

    if not (email and password and user_type):
        return JsonResponse({'error': 'Incomplete registration data'}, status=400)

    #Random location
    latitude = random.uniform(-90, 90)
    longitude = random.uniform(-180, 180)

    location = f"{latitude}${longitude}"

    try:
        # Create user and related instance based on user type
        if user_type == 'customer':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            subscription = request.POST.get('subscription')
            
            Customer.create_customer(email=email, password=password, name=name, phone=phone, address=address, location=location, subscription=subscription)
        elif user_type == 'owner':
            restaurant_name = request.POST.get('restaurant_name')
            restaurant_address = request.POST.get('restaurant_address')
            restaurant_image = request.FILES.get('restaurant_image')
            restaurant_location = location
            restaurant_category = request.POST.get('restaurant_category')

            restaurant = Restaurant.create_restaurant(name=restaurant_name, address=restaurant_address, image=restaurant_image, location=restaurant_location, category=restaurant_category)

            Owner.create_owner(email=email, password=password, restaurant=restaurant)
        elif user_type == 'courier':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            vehicle_number = request.POST.get('vehicle_number')
            card_details = request.POST.get('card_details')
            Courier.create_courier(email=email, password=password, name=name, phone=phone, vehicle_number=vehicle_number, card_details=card_details, location=location)
        else:
            return JsonResponse({'error': 'Invalid user type'}, status=400)

        return JsonResponse({'message': 'User registered successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
