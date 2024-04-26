from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import User, Customer, Owner, Courier
from restaurant_management_app.models import Restaurant

from django.contrib.auth.hashers import check_password

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

@require_POST
def login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    if not (email and password):
        return JsonResponse({'error': 'Incomplete login data'}, status=400)

    try:
        user = User.objects.get(email=email)
        
        if check_password(password, user.password):
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'error': 'Incorrect password'}, status=400)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'}, status=400)
    
def fetch_customer_profile_by_email(request):
    email = request.GET.get('email')

    if not email:
        return JsonResponse({'error': 'Email parameter is missing'}, status=400)

    try:
        customer = Customer.objects.get(email=email)
        
        # Serialize the customer object to JSON format
        customer_data = {
            'id': customer.id,
            'email': customer.email,
            'name': customer.name,
            'phone': customer.phone,
            'address': customer.address,
            'location': customer.location,
            'subscription': customer.subscription,
        }
        
        return JsonResponse(customer_data, status=200)
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer with the provided email does not exist'}, status=404)