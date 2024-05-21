from django.urls import path
from . import views

urlpatterns = [
    
    path("customer_home",views.view_cutomer_homePage, name="View customer Homepage"),
    path("customer_loadhome",views.load_customer_home, name="Fetch all restaurants and load the page"),
    path("customer_loadRestaurant", views.load_restaurant_page, name="Load Restaurant details"),
    path("customer_loadOrders", views.load_customer_ordersPage, name="Load all orders of the customer"),
    
    path("restaurant_home", views.view_restaurant_homePage, name="View restaurant Home"),
    path("restaurant_loadhome", views.load_restaurant_home, name="Fetch Restaurant Home details"),
    path("restaurant_loadOrders", views.load_restaurant_ordersPage, name="Load all orders of the Restaurant"),
    
    path("courier_home", views.view_courier_homepage, name="Courier home page"),
    
    path("add_menu_item", views.create_menu_item, name="Add menu item"),
    path("edit_menu_item", views.edit_or_delete_menu_item, name="Edit/Delete menu item"),
    
    path('fetch_all_restaurants', views.fetch_all_restaurants, name='fetch_all_restaurants'),
    path('fetch_menu_items_by_restaurant_id', views.fetch_menu_items_by_restaurant_id, name='fetch_menu_items_by_restaurant_id'),
    path('create_order', views.create_order, name='create_order'),
    path('fetch_orders_by_customer_email', views.fetch_orders_by_customer_email, name='fetch_orders_by_customer_email'),
    path('fetch_order_details', views.fetch_order_by_orderId, name='fetch_order_by_orderId'),
    path('provide_feedback_to_order', views.provide_feedback_to_order, name='provide_feedback_to_order'),
    path('create_menu_item', views.create_menu_item, name='create_menu_item'),
    path('edit_or_delete_menu_item', views.edit_or_delete_menu_item, name='edit_or_delete_menu_item'),
    path('fetch_orders_by_restaurant_id', views.fetch_orders_by_restaurant_id, name='fetch_orders_by_restaurant_id'),
    path('fetch_orders_by_courier_email', views.fetch_orders_by_courier_email, name='fetch_orders_by_courier_email'),
    path('remove_courier_request', views.remove_courier_request, name='remove_courier_request'),
    
    path('status_update', views.status_update, name='status_update'),

]
