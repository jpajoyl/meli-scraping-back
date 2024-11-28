from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Create your models here.

class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]
    
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    state = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.name + ' ' + self.last_name
    
    
class WishListItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='wishlist_items'
    )
    name = models.CharField(max_length=255)
    image = models.URLField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    mercado_libre_url = models.URLField(max_length=500)

    def __str__(self):
        return self.name