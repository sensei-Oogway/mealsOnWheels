from django.http import JsonResponse
from .models import Restaurant, MenuItem, Order

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
    if request.method == 'POST':
        restaurant_id = request.POST.get('restaurant_id')
        menu_item_ids = request.POST.getlist('menu_item_ids[]')

        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return JsonResponse({'error': 'Restaurant with the provided ID does not exist'}, status=404)

        try:
            menu_items = MenuItem.objects.filter(id__in=menu_item_ids)
        except MenuItem.DoesNotExist:
            return JsonResponse({'error': 'One or more menu items do not exist'}, status=404)

        total_price = sum(menu_item.price for menu_item in menu_items)

        order = Order.objects.create(total=total_price, status='placed', restaurant=restaurant)
        order.menu.set(menu_items)
        
        restaurant.orders.add(order)

        return JsonResponse({'message': 'Order created successfully', 'order_id': order.id}, status=201)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)