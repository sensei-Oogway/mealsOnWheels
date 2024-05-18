from django.urls import path
from . import views

urlpatterns = [
    path('fetch_all_restaurants', views.fetch_all_restaurants, name='fetch_all_restaurants'),
    path('fetch_menu_items_by_restaurant_id', views.fetch_menu_items_by_restaurant_id, name='fetch_menu_items_by_restaurant_id'),
    path('create_order', views.create_order, name='create_order'),
    path('fetch_orders_by_customer_email', views.fetch_orders_by_customer_email, name='fetch_orders_by_customer_email'),
    path('provide_feedback_to_order', views.provide_feedback_to_order, name='provide_feedback_to_order'),
    path('create_menu_item', views.create_menu_item, name='create_menu_item'),
    path('edit_or_delete_menu_item', views.edit_or_delete_menu_item, name='edit_or_delete_menu_item'),
    path('fetch_orders_by_restaurant_id', views.fetch_orders_by_restaurant_id, name='fetch_orders_by_restaurant_id'),
    path('fetch_orders_by_courier_email', views.fetch_orders_by_courier_email, name='fetch_orders_by_courier_email'),
    path('remove_courier_request', views.remove_courier_request, name='remove_courier_request'),
    path('status_update', views.status_update, name='status_update'),
]
