from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.email
    
    @classmethod
    def create_customer(cls, email, password, name, phone, address, location, subscription):
        user = cls.objects.create(email=email, password=password)
        return Customer.objects.create(user=user, name=name, phone=phone, address=address, location=location, subscription=subscription)

    @classmethod
    def create_owner(cls, email, password, restaurant):
        user = cls.objects.create(email=email, password=password)
        return Owner.objects.create(user=user, restaurant=restaurant)

    @classmethod
    def create_courier(cls, email, password, name, phone, vehicle_number, card_details, location):
        user = cls.objects.create(email=email, password=password)
        return Courier.objects.create(user=user, name=name, phone=phone, vehicle_number=vehicle_number, card_details=card_details, location=location)

    @classmethod
    def update_customer(cls, email, **kwargs):
        customer = cls.get_customer(email)
        if customer:
            for key, value in kwargs.items():
                setattr(customer, key, value)
            customer.save()

    @classmethod
    def update_owner(cls, email, **kwargs):
        owner = cls.get_owner(email)
        if owner:
            for key, value in kwargs.items():
                setattr(owner, key, value)
            owner.save()

    @classmethod
    def update_courier(cls, email, **kwargs):
        courier = cls.get_courier(email)
        if courier:
            for key, value in kwargs.items():
                setattr(courier, key, value)
            courier.save()
    
    @classmethod
    def verify_password(self, password):
        return self.password == password

    @classmethod
    def get_customer(cls, email):
        return cls.objects.filter(email=email, customer__isnull=False).first()

    @classmethod
    def get_owner(cls, email):
        return cls.objects.filter(email=email, owner__isnull=False).first()

    @classmethod
    def get_courier(cls, email):
        return cls.objects.filter(email=email, courier__isnull=False).first()

class Customer(User):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    location = models.CharField(max_length=100) 
    SUBSCRIPTION_CHOICES = [
        ('monthly', 'Monthly'),
        ('annual', 'Annual'),
        ('no_subscription', 'No Subscription')
    ]
    subscription = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES)
    # Array to hold Orders (assuming a ManyToMany relationship)
    orders = models.ManyToManyField('restaurant_management_app.Order', blank=True)

class Owner(User):
    # Assuming Restaurant is a model in restaurant_management_app
    restaurant = models.ForeignKey('restaurant_management_app.Restaurant', on_delete=models.CASCADE)
    # Array to hold Orders (assuming a ManyToMany relationship)
    orders = models.ManyToManyField('restaurant_management_app.Order', blank=True)

class Courier(User):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    vehicle_number = models.CharField(max_length=20)
    card_details = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    rating = models.FloatField(default=3.5)
    # Array to hold Orders (assuming a ManyToMany relationship)
    orders = models.ManyToManyField('restaurant_management_app.Order', blank=True)
