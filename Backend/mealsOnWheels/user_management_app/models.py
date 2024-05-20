from django.db import models

class Customer(models.Model):
    email = models.EmailField(unique=True,default=None,primary_key=True)
    password = models.CharField(max_length=128,default=None)
    name = models.CharField(max_length=100,default=None)
    phone = models.CharField(max_length=15,default=None)
    address = models.CharField(max_length=255,default=None)
    location = models.CharField(max_length=100,default=None) 
    SUBSCRIPTION_CHOICES = [
        ('monthly', 'Monthly'),
        ('annual', 'Annual'),
        ('no_subscription', 'No Subscription')
    ]
    subscription = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES, default="no_subscription")
    # Array to hold Orders (assuming a ManyToMany relationship)
    orders = models.ManyToManyField('restaurant_management_app.Order', blank=True)

    @classmethod
    def create(cls, email, password, name, phone, address, location, subscription):
        customer = cls.objects.create(email=email, password=password, name=name, phone=phone, address=address, location=location, subscription=subscription)
        return customer

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    def verify_password(self, password):
        return self.password == password

    @classmethod
    def get(cls, email):
        return cls.objects.filter(email=email).first()

class Owner(models.Model):
    email = models.EmailField(unique=True,default=None,primary_key=True)
    password = models.CharField(max_length=128,default=None)
    # Assuming Restaurant is a model in restaurant_management_app
    restaurant = models.ForeignKey('restaurant_management_app.Restaurant', on_delete=models.CASCADE)
    # Array to hold Orders (assuming a ManyToMany relationship)
    orders = models.ManyToManyField('restaurant_management_app.Order', blank=True)

    @classmethod
    def create(cls, email, password, restaurant):
        owner = cls.objects.create(email=email, password=password, restaurant=restaurant)
        return owner

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    def verify_password(self, password):
        return self.password == password
    
    def getRestaurant(self):
        return self.restaurant

    @classmethod
    def get(cls, email):
        return cls.objects.filter(email=email).first()

class Courier(models.Model):
    email = models.EmailField(unique=True, default=None,primary_key=True)
    password = models.CharField(max_length=128,default=None)
    name = models.CharField(max_length=100,default=None)
    phone = models.CharField(max_length=15,default=None)
    vehicle_number = models.CharField(max_length=20,default=None)
    card_details = models.CharField(max_length=100,default=None)
    location = models.CharField(max_length=100,default=None)
    rating = models.FloatField(default=3.5)
    # Array to hold Orders (assuming a ManyToMany relationship)
    orders = models.ManyToManyField('restaurant_management_app.Order', blank=True)

    @classmethod
    def create(cls, email, password, name, phone, vehicle_number, card_details, location):
        courier = cls.objects.create(email=email, password=password, name=name, phone=phone, vehicle_number=vehicle_number, card_details=card_details, location=location)
        return courier

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    def verify_password(self, password):
        return self.password == password

    @classmethod
    def get(cls, email):
        return cls.objects.filter(email=email).first()
