from django.http import JsonResponse
from .models import Restaurant, MenuItem

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
