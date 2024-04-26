from django.http import JsonResponse
from .models import Restaurant, MenuItem, Order
from user_management_app.models import Customer, Courier

def fetch_all_restaurants(request):
    restaurants = Restaurant.objects.all()
    restaurant_data = list(restaurants.values())

    return JsonResponse(restaurant_data, safe=False)

def fetch_menu_items_by_restaurant_id(request):
    restaurant_id = request.GET.get("restaurant_id");
    
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        menu_items = restaurant.menu.all()

        menu_items_data = list(menu_items.values())

        return JsonResponse(menu_items_data, safe=False)
    except Restaurant.DoesNotExist:
        return JsonResponse({'error': 'Restaurant with the provided ID does not exist'}, status=404)

def create_order(request):
    restaurant_id = request.POST.get('restaurant_id')
    menu_item_ids = request.POST.getlist('menu_item_ids[]')
    customer_email = request.POST.get('customer_email')

    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
    except Restaurant.DoesNotExist:
        return JsonResponse({'error': 'Restaurant with the provided ID does not exist'}, status=404)

    try:
        menu_items = MenuItem.objects.filter(id__in=menu_item_ids)
    except MenuItem.DoesNotExist:
        return JsonResponse({'error': 'One or more menu items do not exist'}, status=404)
    
    try:
        customer = Customer.objects.get(email=customer_email)
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer with the provided email does not exist'}, status=404)

    total_price = sum(menu_item.price for menu_item in menu_items)

    order = Order.objects.create(total=total_price, status='placed', restaurant=restaurant)
    order.menu.set(menu_items)
    
    restaurant.orders.add(order)
    customer.orders.add(order)

    return JsonResponse({'message': 'Order created successfully', 'order_id': order.id}, status=201)

def fetch_orders_by_customer_email(request):
    email = request.GET.get('email')

    if not email:
        return JsonResponse({'error': 'Email parameter is missing'}, status=400)

    try:
        customer = Customer.objects.get(email=email)
        orders = customer.orders.all()

        # Serialize the orders queryset to JSON format
        orders_data = []
        for order in orders:
            order_info = {
                'id': order.id,
                'total': order.total,
                'status': order.status,
                'feedback': order.feedback,
                'menu': list(order.menu.values()),  # Serialize menu items for each order
            }
            orders_data.append(order_info)

        return JsonResponse(orders_data, safe=False)

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
        restaurant_id = request.POST.get('restaurant_id')
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')

        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return JsonResponse({'error': 'Restaurant with the provided ID does not exist'}, status=404)

        menu_item = MenuItem.objects.create(name=name, description=description, price=price)
        restaurant.menu.add(menu_item)
        restaurant.save()

        return JsonResponse({'message': 'Menu item created and added to the restaurant successfully', 'menu_item_id': menu_item.id}, status=201)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
def edit_or_delete_menu_item(request):
    action = request.POST.get('action')  # 'edit' or 'delete'
    menu_item_id = request.POST.get('menu_item_id')
    restaurant_id = request.POST.get('restaurant_id')

    try:
        menu_item = MenuItem.objects.get(id=menu_item_id)
        restaurant = Restaurant.objects.get(id=restaurant_id)
    except (MenuItem.DoesNotExist, Restaurant.DoesNotExist):
        return JsonResponse({'error': 'Menu item or Restaurant with the provided ID does not exist'}, status=404)

    if action == 'edit':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        if name:
            menu_item.name = name
        if description:
            menu_item.description = description
        if price:
            menu_item.price = price
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
    
def fetch_orders_by_restaurant_id(request):
    restaurant_id = request.GET.get('restaurant_id')

    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
    except Restaurant.DoesNotExist:
        return JsonResponse({'error': 'Restaurant with the provided ID does not exist'}, status=404)

    # Fetch orders associated with the restaurant
    orders = restaurant.orders

    # Serialize the orders queryset to JSON format
    orders_data = []
    for order in orders:
        order_info = {
            'id': order.id,
            'total': order.total,
            'status': order.status,
            'feedback': order.feedback,
            # Add other fields as needed
        }
        orders_data.append(order_info)

    return JsonResponse(orders_data, safe=False)

def fetch_orders_by_courier_email(request):
    email = request.GET.get('email')

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
            }
            orders_data.append(order_info)

        return JsonResponse(orders_data, safe=False)
    
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

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order with the provided ID does not exist'}, status=404)

        if status == "accepted":
            # Restaurant accepts the order
            # Publish the order and move to waiting for courier
            try:
                restaurant_id = request.POST.get('restaurant_id')
                restaurant = Restaurant.objects.get(id=restaurant_id)
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
            courier_email = request.POST.get('courier_email')
            try:
                courier = Courier.objects.get(email=courier_email)
            except Courier.DoesNotExist:
                return JsonResponse({'error': 'Courier with the provided email does not exist'}, status=404)

            # Remove all other delivery requests and add the specific courier
            order.delivery_requests.clear()
            order.delivery_requests.add(courier)
            order.status = status
            order.save()

            return JsonResponse({'message': 'Courier accepted successfully'}, status=200)

        elif status in ["ready_to_dispatch", "rejected", "delivered", "picked_up"]:
            order.status = status
            order.save()
            return JsonResponse({'message': 'Status updated successfully'}, status=200)

        else:
            return JsonResponse({'error': 'Invalid status'}, status=400)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)