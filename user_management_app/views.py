from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Customer, Owner, Courier
from restaurant_management_app.models import Restaurant
from django.core import serializers

from django.shortcuts import render

from django.contrib.auth.hashers import check_password

import random
import json

def home_login(request):
    return render(request,"login_registration.html")

@require_POST
def register_user(request):
    # Extract registration data from the POST request
    data = json.loads(request.body)
    
    email = data.get('email')
    password = data.get('password')
    user_type = data.get('user_type')  # user_type (e.g., 'customer', 'owner', 'courier')
    
    # print(request.POST)

    if not (email and password and user_type):
        return JsonResponse({'error': 'Incomplete registration data'}, status=400)

    #Random location
    latitude = random.uniform(-90, 90)
    longitude = random.uniform(-180, 180)

    location = f"{latitude}${longitude}"

    try:
        # Create user and related instance based on user type
        if user_type == 'customer':
            name = data.get('name')
            phone = data.get('mobile')
            address = data.get('address')
            subscription = data.get('membership')
            
            print(Customer.create(email=email, password=password, name=name, phone=phone, address=address, location=location, subscription=subscription))

        elif user_type == 'owner':
            restaurant_name = data.get('restaurant')
            restaurant_address = data.get('address')
            restaurant_image = data['image']
            restaurant_location = location
            restaurant_category = data.get('category')
            
            restaurant = Restaurant.create_restaurant(name=restaurant_name, address=restaurant_address, image=restaurant_image, location=restaurant_location, category=restaurant_category)

            Owner.create(email=email, password=password, restaurant=restaurant)
        elif user_type == 'courier':
            name = data.get('name')
            phone = data.get('mobile')
            vehicle_number = data.get('vehicle')
            card_details = data.get('cardNumber') 
            
            Courier.create(email=email, password=password, name=name, phone=phone, vehicle_number=vehicle_number, card_details=card_details, location=location)
        else:
            return JsonResponse({'error': 'Invalid user type'}, status=400)

        return JsonResponse({'message': 'User registered successfully','status':200}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_POST
def login(request):
    data = json.loads(request.body)
    
    email = data.get('email')
    password = data.get('password')

    if not (email and password):
        return JsonResponse({'error': 'Incomplete login data'}, status=400)
    
    customer = Customer.get(email)
    if(customer):
        if(customer.verify_password(password)):
            return JsonResponse({'message': 'Login successful', "status":200,"type":"customer", "user":serializers.serialize('json', [customer])}, status=200)
        else:
            return JsonResponse({'message': 'Wrong password', "status":400})
        
    
    owner = Owner.get(email)
    if(owner):
        if(owner.verify_password(password)):
            return JsonResponse({'message': 'Login successful', "status":200,"type":"owner","user":serializers.serialize('json', [owner])}, status=200)
        else:
            return JsonResponse({'message': 'Wrong password', "status":400})
        
    courier = Courier.get(email)
    if(courier):
        if(courier.verify_password(password)):
            return JsonResponse({'message': 'Login successful', "status":200,"type":"courier","user":serializers.serialize('json', [courier])}, status=200)
        else:
            return JsonResponse({'message': 'Wrong password', "status":400})
    return JsonResponse({'message': 'Invalid User'}, status=400)


    
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

@require_POST
def edit_customer_profile(request):
    email = request.POST.get('email')

    if not email:
        return JsonResponse({'error': 'Email parameter is missing'}, status=400)

    try:
        customer = Customer.objects.get(email=email)

        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        location = request.POST.get('location')
        subscription = request.POST.get('subscription')

        if name:
            customer.name = name
        if phone:
            customer.phone = phone
        if address:
            customer.address = address
        if location:
            customer.location = location
        if subscription:
            customer.subscription = subscription

        customer.save()

        return JsonResponse({'message': 'Customer profile updated successfully'}, status=200)

    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer with the provided email does not exist'}, status=404)
    
