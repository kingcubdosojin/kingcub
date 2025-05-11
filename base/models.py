from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Countries(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name


class Quote(models.Model):
    ship_from = models.CharField(max_length=50)
    ship_to = models.CharField(max_length=50)
    weight = models.IntegerField()
    length = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return f'Quotes from {self.ship_from} to {self.ship_to} for {self.email}'
    
class Company_name(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}'

class Shipper(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    pfp = models.ImageField(upload_to='pfp/', blank=True, null=True)
    location =models.CharField(max_length=30)


    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Receiver(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    address_line = models.TextField()
    address_line2 = models.TextField(blank=True, null=True)
    city_and_zip_code = models.TextField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f'Receiver {self.first_name} {self.last_name}'
    
ORDER_STATUS = [
   ('PE', 'Pending'),
    ('PU', 'Picked up'),
    ('OH', 'On Hold'),
    ('OD', 'Out for delivery'),
    ('IT', 'In-Transit'),
    ('EN', 'Enroute'),
    ('CA', 'Cancelled'),
    ('DE', 'Delivered'),
    ('RE', 'Returned'),
]    

"""Class to track model"""
class Order(models.Model):

    tracking_id = models.CharField(max_length=10)
    screen_width = models.IntegerField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    zoom = models.FloatField(default=0.0)
    current_position = models.CharField(max_length=40)
    expected_date = models.CharField(max_length=20)
    carrier = models.CharField(max_length=20)
    ship_date = models.DateField()
    shipping_service = models.CharField(max_length=20)
    shipped_from = models.CharField(max_length=30)
    shipping_to = models.CharField(max_length=30)
    shipping_cost = models.FloatField()
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Receiver, on_delete=models.CASCADE)
    on_hold = models.BooleanField(default=False)
    comment = models.TextField()
    qty = models.CharField(max_length=10)
    piece_type = models.CharField(max_length=20)
    description = models.TextField()
    length = models.CharField(max_length=10)
    width = models.CharField(max_length=10)
    height = models.CharField(max_length=10)
    weight = models.CharField(max_length=10)
    status =  models.CharField(max_length=2, choices=ORDER_STATUS, default='PE')



    def __str__(self):
        return self.tracking_id

    def get_status(self):
        return dict(ORDER_STATUS).get(self.status, 'Unknown')
    
class MailError(models.Model):
    text = models.TextField()
    mail = models.EmailField()

    def __str__(self):
        return self.mail
    
class TempUser(models.Model):
    user_email = models.EmailField()
    username = models.CharField(max_length=20)
    otp = models.CharField(max_length=7)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=30)
    

    def __str__(self):
        return f'{self.otp} for {self.username}'
