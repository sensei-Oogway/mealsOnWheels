from django.http import JsonResponse
from .models import Restaurant

def fetch_all_restaurants(request):
    restaurants = Restaurant.objects.all()
    restaurant_data = list(restaurants.values())

    return JsonResponse(restaurant_data, safe=False)


