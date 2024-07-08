from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    BUYER = 'buyer'
    SELLER = 'seller'
    ROLE_CHOICES = (
        (BUYER, 'Buyer'),
        (SELLER, 'Seller'),
    )
    role = models.CharField(max_length=6, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.username