from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import Customer, Owner, Courier
from restaurant_management_app.models import Restaurant

class CustomerTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            email="customer@example.com",
            password="password",
            name="Customer Name",
            phone="1234567890",
            address="Customer Address",
            location="Customer Location",
            subscription="monthly"
        )

    def test_create_customer(self):
        self.assertEqual(self.customer.email, "customer@example.com")
        self.assertEqual(self.customer.password, "password")
        self.assertEqual(self.customer.name, "Customer Name")
        self.assertEqual(self.customer.phone, "1234567890")
        self.assertEqual(self.customer.address, "Customer Address")
        self.assertEqual(self.customer.location, "Customer Location")
        self.assertEqual(self.customer.subscription, "monthly")

    def test_update_customer(self):
        self.customer.update(name="Updated Name")
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.name, "Updated Name")

    def test_verify_password(self):
        self.assertTrue(self.customer.verify_password("password"))
        self.assertFalse(self.customer.verify_password("incorrect_password"))

    def test_get_customer(self):
        fetched_customer = Customer.get("customer@example.com")
        self.assertEqual(fetched_customer.email, "customer@example.com")

class OwnerTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            address="Test Address",
            image="Test Image",
            location="Test Location",
            category="fast_food"
        )
        
        self.owner = Owner.objects.create(
            email="owner@example.com",
            password="password",
            restaurant = self.restaurant
        )

    def test_create_owner(self):
        self.assertEqual(self.owner.email, "owner@example.com")
        self.assertEqual(self.owner.password, "password")
        self.assertEqual(self.owner.restaurant_id, 1)

    def test_update_owner(self):
        self.owner.update(password="new_password")
        self.owner.refresh_from_db()
        self.assertEqual(self.owner.password, "new_password")

    def test_verify_password(self):
        self.assertTrue(self.owner.verify_password("password"))
        self.assertFalse(self.owner.verify_password("incorrect_password"))

    def test_get_owner(self):
        fetched_owner = Owner.get("owner@example.com")
        self.assertEqual(fetched_owner.email, "owner@example.com")

class CourierTestCase(TestCase):
    def setUp(self):
        self.courier = Courier.objects.create(
            email="courier@example.com",
            password="password",
            name="Courier Name",
            phone="1234567890",
            vehicle_number="ABC123",
            card_details="1234 5678 9012 3456",
            location="Courier Location"
        )

    def test_create_courier(self):
        self.assertEqual(self.courier.email, "courier@example.com")
        self.assertEqual(self.courier.password, "password")
        self.assertEqual(self.courier.name, "Courier Name")
        self.assertEqual(self.courier.phone, "1234567890")
        self.assertEqual(self.courier.vehicle_number, "ABC123")
        self.assertEqual(self.courier.card_details, "1234 5678 9012 3456")
        self.assertEqual(self.courier.location, "Courier Location")

    def test_update_courier(self):
        self.courier.update(name="Updated Name")
        self.courier.refresh_from_db()
        self.assertEqual(self.courier.name, "Updated Name")

    def test_verify_password(self):
        self.assertTrue(self.courier.verify_password("password"))
        self.assertFalse(self.courier.verify_password("incorrect_password"))

    def test_get_courier(self):
        fetched_courier = Courier.get("courier@example.com")
        self.assertEqual(fetched_courier.email, "courier@example.com")
