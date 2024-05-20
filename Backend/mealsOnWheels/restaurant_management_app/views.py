from django.http import JsonResponse
from .models import Restaurant, MenuItem, Order
from user_management_app.models import Customer, Courier, Owner

from django.core.serializers import serialize

from django.shortcuts import render
import json, decimal


def view_cutomer_homePage(request):
    restaurants = fetch_all_restaurants(request)
    return render(request, 'customer_homePage.html', {'restaurants': restaurants})

def load_customer_home(request):
    restaurants = fetch_all_restaurants(request)
    return render(request, 'customer_restaurantsGrid.html', {'restaurants': restaurants})

def view_restaurant_homePage(request):
    id = request.POST.get("id")
    owner = Owner.get(id)
    restaurant = owner.getRestaurant()
    
    restaurant_obj = {"id":restaurant.id,"name":restaurant.name, "rating": restaurant.rating,"image": restaurant.image, "menu": restaurant.menu.all()}
    
    return render(request,'restaurant_homePage.html', {'restaurant':restaurant_obj})

def load_restaurant_page(request):
    restaurant_id = request.POST.get("restaurant_id")
    restaurant = Restaurant.fetch_restaurant_by_id(restaurant_id)

    restaurant_obj = {"id":restaurant.id,"name":restaurant.name, "rating": restaurant.rating,"image": restaurant.image, "menu": restaurant.menu.all()}

    return render(request,'customer_restaurantPage.html', {'restaurant':restaurant_obj})

def load_restaurant_home(request):
    id = request.POST.get("id")
    restaurant_id = request.POST.get("restaurant_id")
    if id:
        owner = Owner.get(id)
        restaurant = owner.getRestaurant()
    else:
        restaurant = Restaurant.fetch_restaurant_by_id()

    restaurant_obj = {"id":restaurant.id,"name":restaurant.name, "rating": restaurant.rating,"image": restaurant.image, "menu": restaurant.menu.all()}

    return render(request,'restaurant_restaurantPage.html', {'restaurant':restaurant_obj})


def load_customer_ordersPage(request):
    email = request.POST.get("email")
    orders = fetch_orders_by_customer_email(email)
    
    return render(request,'customer_ordersPage.html', {'orders':orders})

def view_courier_homepage(request):
    email = request.POST.get("email")
    orders = fetch_orders_by_courier_email(email)
    
    return render(request,'delivery_homePage.html', {'orders':orders})



def load_restaurant_ordersPage(request):
    email = request.POST.get("email")
    owner = Owner.get(email)
    restaurant = owner.getRestaurant()
    orders = fetch_orders_by_restaurant_id(restaurant.id)
    
    return render(request,'restaurant_ordersPage.html', {'orders':orders})






def fetch_all_restaurants(request):
    restaurants = Restaurant.objects.all()
    restaurant_data = list(restaurants.values())
    
    # print(restaurant_data)

    return restaurant_data

def fetch_menu_items_by_restaurant_id(request):
    restaurant_id = request.GET.get("restaurant_id")
    
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        menu_items = restaurant.menu.all()

        menu_items_data = list(menu_items.values())

        return JsonResponse(menu_items_data, safe=False)
    except Restaurant.DoesNotExist:
        return JsonResponse({'error': 'Restaurant with the provided ID does not exist'}, status=404)

def create_order(request):
    restaurant_id = request.POST.get('restaurant_id')
    menu_item_ids = request.POST.getlist('menu_item_ids')
    customer_email = request.POST.get('customer_email')

    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
    except Restaurant.DoesNotExist:
        return JsonResponse({'error': 'Restaurant with the provided ID does not exist'}, status=404)

    menu_item_ids = json.loads(menu_item_ids[0])

    try:
        menu_items = MenuItem.objects.filter(id__in=menu_item_ids)
    except MenuItem.DoesNotExist:
        return JsonResponse({'error': 'One or more menu items do not exist'}, status=404)
    
    try:
        customer = Customer.objects.get(email=customer_email)
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer with the provided email does not exist'}, status=404)

    total_price = sum(menu_item.price for menu_item in menu_items)
        #Service tax and discount calculation
    total_price = total_price + (decimal.Decimal('0.05') * total_price)
    if customer.subscription != "no_subscription":
        total_price = total_price - (decimal.Decimal('0.1') * total_price) #discount
        
    

    order = Order.objects.create(total=total_price, status='placed', restaurant_instance=restaurant)
    order.menu.set(menu_items)
    
    restaurant.orders.add(order)
    customer.orders.add(order)

    return JsonResponse({'message': 'Order created successfully', 'order_id': order.id}, status=201)

def fetch_order_by_orderId(request):
    orderId = request.POST.get('order_id')
    order = Order.objects.get(id = orderId)
    
    order_info = {
                'id': order.id,
                'total': order.total,
                'status': order.status,
                'feedback': order.feedback,
                'menu': list(order.menu.values()), 
                "restaurant": order.restaurant_instance.name
            }
    
    if(order.getStatusIndex() >= 5):
        courier = order.delivery_requests.first()
        delivery_obj = {
            'name': courier.name,
            'mobile': courier.phone
        }
        order_info["courier"] = delivery_obj
    
    return JsonResponse(order_info, safe=False)

def fetch_orders_by_customer_email(email):
    try:
        customer = Customer.objects.get(email=email)
        orders = customer.orders.all()

        # Serialize the orders queryset to JSON format
        orders_data = []
        for order in orders:
            order
            order_info = {
                'id': order.id,
                'total': order.total,
                'status': order.status,
                'feedback': order.feedback,
                'menu': list(order.menu.values()),  # Serialize menu items for each order
                "restaurant": order.restaurant_instance.name
            }
            orders_data.append(order_info)

        return orders_data

    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer with the provided email does not exist'}, status=404)
    
def provide_feedback_to_order(request):
    order_id = request.POST.get('order_id')
    res_rating = request.POST.get('res_rating')
    courier_rating = request.POST.get('courier_rating')

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order with the provided ID does not exist'}, status=404)

    feedback = f"{res_rating}|{courier_rating}"

    if order.feedback:
        order.feedback += f",{feedback}"
    else:
        order.feedback = feedback

    order.save()

    return JsonResponse({'message': 'Feedback added to order successfully'}, status=200)

def create_menu_item(request):
    if request.method == 'POST':
        name = request.POST.get('productName')
        description = request.POST.get('productDescription')
        price = request.POST.get('productPrice')
        image = request.POST.get('productImage')
        
        try:
            owner_id = request.POST.get('owner_id')
            restaurant = Owner.get(owner_id).getRestaurant()
        except Restaurant.DoesNotExist:
            return JsonResponse({'error': 'Restaurant with the provided ID does not exist'}, status=404)

        menu_item = MenuItem.objects.create(name=name, description=description, price=price, image=image)
        restaurant.menu.add(menu_item)
        restaurant.save()

        return JsonResponse({'message': 'Menu item created and added to the restaurant successfully', 'menu_item_id': menu_item.id}, status=201)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
def edit_or_delete_menu_item(request):
    action = request.POST.get('action')  # 'edit' or 'delete'
    menu_item_id = request.POST.get('productId')
    
    try:
        menu_item = MenuItem.objects.get(id=menu_item_id)
        owner_id = request.POST.get('owner_id')
        restaurant = Owner.get(owner_id).getRestaurant()
    except (MenuItem.DoesNotExist, Restaurant.DoesNotExist):
        return JsonResponse({'error': 'Menu item or Restaurant with the provided ID does not exist'}, status=404)

    if action == 'edit':
        name = request.POST.get('productName')
        description = request.POST.get('productDescription')
        price = request.POST.get('productPrice')
        image = request.POST.get('productImage')
        
        if name:
            menu_item.name = name
        if description:
            menu_item.description = description
        if price:
            menu_item.price = price
        if image:
            menu_item.image = image
            
        menu_item.save()

        return JsonResponse({'message': 'Menu item updated successfully'}, status=200)

    elif action == 'delete':
        if menu_item in restaurant.menu.all():
            restaurant.menu.remove(menu_item)
            menu_item.delete()
            return JsonResponse({'message': 'Menu item deleted successfully from the restaurant'}, status=200)
        else:
            return JsonResponse({'error': 'Menu item is not in the menu of the provided restaurant'}, status=400)

    else:
        return JsonResponse({'error': 'Invalid action specified'}, status=400)
    
def fetch_orders_by_restaurant_id(res_id):
    restaurant_id = res_id

    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
    except Restaurant.DoesNotExist:
        return JsonResponse({'error': 'Restaurant with the provided ID does not exist'}, status=404)

    orders = restaurant.orders.all()

    # Serialize the orders queryset to JSON format
    orders_data = []
    for order in orders:
        order_info = {
            'id': order.id,
            'total': order.total,
            'status': order.status,
            'feedback': order.feedback,
        }
        orders_data.append(order_info)
        

        if(order.getStatusIndex() >= 5):
                courier = order.delivery_requests.first()
                delivery_obj = {
                    'name': courier.name,
                    'mobile': courier.phone
                }
                order_info["courier"] = delivery_obj
    
    return orders_data

def fetch_orders_by_courier_email(email):
    if not email:
        return JsonResponse({'error': 'Email parameter is missing'}, status=400)

    try:
        courier = Courier.objects.get(email=email)
        orders = courier.orders.all()

        # Serialize the orders queryset to JSON format
        orders_data = []
        for order in orders:
            order_info = {
                'id': order.id,
                'total': order.total,
                'status': order.status,
                'feedback': order.feedback,
                'menu': list(order.menu.values()),  # Serialize menu items for each order
                "restaurant": order.restaurant_instance.name
            }
            orders_data.append(order_info)

        return orders_data
    
    except Courier.DoesNotExist:
        return JsonResponse({'error': 'Courier with the provided email does not exist'}, status=404)
    
def remove_courier_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        order_id = request.POST.get('order_id')

        try:
            courier = Courier.objects.get(email=email)
            order = Order.objects.get(id=order_id)
        except Courier.DoesNotExist:
            return JsonResponse({'error': 'Courier with the provided email does not exist'}, status=404)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order with the provided ID does not exist'}, status=404)

        order.delivery_requests.remove(courier)
        courier.orders.remove(order)

        return JsonResponse({'message': 'Courier request removed from order successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
            
def status_update(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        order_id = request.POST.get('order_id')
        user_id = request.POST.get('user_id')

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order with the provided ID does not exist'}, status=404)

        if status == "accepted":
            # Restaurant accepts the order
            # Publish the order and move to waiting for courier
            try:
                owner = Owner.get(user_id)
                restaurant = owner.getRestaurant()
            except Restaurant.DoesNotExist:
                return JsonResponse({'error': 'Restaurant with the provided ID does not exist'}, status=404)

            # Add the order to all couriers' delivery requests
            couriers = Courier.objects.all()
            for courier in couriers:
                order.delivery_requests.add(courier)
                courier.orders.add(order)
                courier.save()

            order.status = "waiting_for_courier"
            order.save()

            return JsonResponse({'message': 'Restaurant accepted successfully'}, status=200)

        elif status == "courier_accepted":
            courier_email = user_id
            try:
                courier = Courier.objects.get(email=courier_email)
            except Courier.DoesNotExist:
                return JsonResponse({'error': 'Courier with the provided email does not exist'}, status=404)

            # Remove all other delivery requests and add the specific courier
            couriers = Courier.objects.filter(orders=order)  # Filter couriers who have the order
            for courier in couriers:
                courier.orders.remove(order)  # Remove the order from the courier's orders
                courier.save()
            
            order.delivery_requests.clear()
            order.delivery_requests.add(courier)
            order.status = status
            order.save()

            return JsonResponse({'message': 'Courier accepted successfully'}, status=200)
        
        elif status == "courier_rejected":
            courier_email = user_id
            try:
                courier = Courier.objects.get(email=courier_email)
            except Courier.DoesNotExist:
                return JsonResponse({'error': 'Courier with the provided email does not exist'}, status=404)
            
            order.delivery_requests.remove(courier)
            courier.orders.remove(order)
            
            courier.save()
            order.save()

        elif status in ["ready_to_dispatch","rejected", "delivered", "picked_up"]:
            order.status = status
            order.save()
            return JsonResponse({'message': 'Status updated successfully'}, status=200)

        else:
            return JsonResponse({'error': 'Invalid status'}, status=400)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)