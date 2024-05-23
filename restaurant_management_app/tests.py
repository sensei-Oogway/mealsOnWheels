from django.test import TestCase
from decimal import Decimal
import json
from django.core.exceptions import ValidationError
from .models import Restaurant, MenuItem, Order
from django.core.serializers import serialize

class RestaurantTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            address="Test Address",
            image="Test Image",
            location="Test Location",
            category="fast_food"
        )

        self.menu_item = MenuItem.objects.create(
            name="Test Item",
            image="Test Image",
            description="Test Description",
            price=10.99
        )

    def test_create_restaurant(self):
        
        self.assertEqual(self.restaurant.name, "Test Restaurant")
        self.assertEqual(self.restaurant.address, "Test Address")
        self.assertEqual(self.restaurant.image, "Test Image")
        self.assertEqual(self.restaurant.location, "Test Location")
        self.assertEqual(self.restaurant.category, "fast_food")

    def test_update_restaurant(self):
        self.restaurant.update_restaurant(name="Updated Restaurant")
        self.restaurant.refresh_from_db()
        self.assertEqual(self.restaurant.name, "Updated Restaurant")

    def test_add_menu_item(self):
        self.restaurant.add_menu_item(self.menu_item)
        self.assertIn(self.menu_item, self.restaurant.menu.all())

    def test_remove_menu_item(self):
        self.restaurant.add_menu_item(self.menu_item)
        self.assertIn(self.menu_item, self.restaurant.menu.all())

        self.restaurant.remove_menu_item(self.menu_item)
        self.assertNotIn(self.menu_item, self.restaurant.menu.all())

    def test_fetch_restaurant_json(self):
        expected_json = serialize('json', [self.restaurant])
        self.assertEqual(self.restaurant.fetch_restaurant_json(), expected_json)

    def test_fetch_restaurant_by_id(self):
        fetched_restaurant = Restaurant.fetch_restaurant_by_id(self.restaurant.id)
        self.assertEqual(fetched_restaurant.id, self.restaurant.id)

    def test_fetch_all_restaurants(self):
        Restaurant.objects.create(
            name="Restaurant 2",
            address="Address 2",
            image="Image 2",
            location="Location 2",
            category="cafe"
        )
        Restaurant.objects.create(
            name="Restaurant 3",
            address="Address 3",
            image="Image 3",
            location="Location 3",
            category="asian"
        )

        # Fetch all restaurants
        all_restaurants = Restaurant.fetch_all_restaurants()
        all_restaurants = json.loads(all_restaurants)
        self.assertEqual(len(all_restaurants), 3)
 
class MenuItemTestCase(TestCase):
    def setUp(self):
        self.menu_item = MenuItem.objects.create(
            name="Test Item",
            image="Test Image",
            description="Test Description",
            price=10.99
        )

    def test_create_menu_item(self):
        self.assertEqual(self.menu_item.name, "Test Item")
        self.assertEqual(self.menu_item.image, "Test Image")
        self.assertEqual(self.menu_item.description, "Test Description")
        self.assertEqual(self.menu_item.price, 10.99)

    def test_update_menu_item(self):
        self.menu_item.update_menu_item(name="Updated Item")
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.name, "Updated Item")
        
    def fetch_menu_item_by_id(self):
        fetched_menu_item = MenuItem.fetch_menu_item_by_id(self.id)
        self.assertEqual(self.id,fetched_menu_item)

class OrderTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            address="Test Address",
            image="Test Image",
            location="Test Location",
            category="fast_food"
        )

        self.order = Order.objects.create(
            total=20.99,
            status="placed",
            restaurant_instance=self.restaurant
        )

    def test_create_order(self):
        self.assertEqual(self.order.total, 20.99)
        self.assertEqual(self.order.status, "placed")

    def test_update_order(self):
        self.order.update_order(total=Decimal('30.99'))
        self.order.refresh_from_db()
        self.assertEqual(self.order.total, Decimal('30.99'))

    def test_fetch_order_by_id(self):
        fetched_order_json = Order.fetch_order_by_id(self.order.id)
        fetched_order = json.loads(fetched_order_json)[0]
        fetched_order_id = fetched_order['pk']  # 'pk' is used for the primary key in serialized data
        self.assertEqual(fetched_order_id, self.order.id)

