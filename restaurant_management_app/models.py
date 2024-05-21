from django.db import models
from django.core import serializers
import random

class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    image = models.TextField()
    location = models.CharField(max_length=100)
    menu = models.ManyToManyField('MenuItem')
    orders = models.ManyToManyField('Order')
    rating = models.FloatField(default=3.5)
    
    distance = models.IntegerField(default=random.randint(1, 12))
    CATEGORY_CHOICES = [
        ('cafe', 'Cafe'),
        ('asian', 'Asian'),
        ('club', 'Club'),
        ('fast_food', 'Fast Food'),
        ('indian', 'Indian')
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    @classmethod
    def create_restaurant(cls, name, address, image, location, category):
        return cls.objects.create(name=name, address=address, image=image, location=location, category=category)

    @classmethod
    def fetch_all_restaurants(cls):
        return serializers.serialize('json', cls.objects.all())

    def update_restaurant(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    def add_menu_item(self, menu_item):
        self.menu.add(menu_item)

    def remove_menu_item(self, menu_item):
        self.menu.remove(menu_item)

    def fetch_restaurant_json(self):
        return serializers.serialize('json', [self])
    
    @classmethod
    def fetch_restaurant_by_id(cls, restaurant_id):
        try:
            restaurant = cls.objects.get(id=restaurant_id)
            return restaurant
        except cls.DoesNotExist:
            return None

class MenuItem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    image = models.TextField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @classmethod
    def create_menu_item(cls, name, image, description, price):
        return cls.objects.create(name=name, image=image, description=description, price=price)

    def update_menu_item(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    def fetch_menu_item_json(self):
        return serializers.serialize('json', [self])
    
    @classmethod
    def fetch_menu_item_by_id(cls, menu_item_id):
        try:
            menu_item = cls.objects.get(id=menu_item_id)
            return serializers.serialize('json', [menu_item])
        except cls.DoesNotExist:
            return None

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    menu = models.ManyToManyField('MenuItem')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    feedback = models.TextField(blank=True)
    delivery_requests = models.ManyToManyField('user_management_app.Courier')
    
    restaurant_instance  = models.ForeignKey('Restaurant', on_delete=models.CASCADE, default=None)

    STATUS_CHOICES = [
        ('placed', 'Placed'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
        ('ready_to_dispatch', 'Ready to Dispatch'),
        ('waiting_for_courier', 'Waiting for Courier'),
        ('courier_accepted', 'Courier Accepted'),
        ('picked_up', 'Picked Up'),
        ('delivered', 'Delivered')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    @classmethod
    def create_order(cls, menu, total, restaurant):
        return cls.objects.create(menu=menu, total=total, restaurant=restaurant)

    def update_order(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    def update_order_status(self, status):
        self.status = status
        self.save()

    def fetch_order_json(self):
        return serializers.serialize('json', [self])
    
    @classmethod
    def fetch_order_by_id(cls, order_id):
        try:
            order = cls.objects.get(id=order_id)
            return serializers.serialize('json', [order])
        except cls.DoesNotExist:
            return None
        
    def getStatusIndex(self):
        status_index = None
        
        for index, (value, label) in enumerate(self.STATUS_CHOICES):
            if value == self.status:
                status_index = index
                break
            
        return status_index
